from django.utils.translation import gettext as _
from dal.autocomplete import ListSelect2

from crispy_forms.helper import FormHelper
from django import forms

from django.urls import reverse_lazy
from dal import autocomplete

from django.contrib.auth import get_user_model
from core.models import Flow

approvers_widget = autocomplete.ModelSelect2Multiple(url=reverse_lazy('api:autocomplete', kwargs={'to_field': 'pk', 'app': get_user_model()._meta.app_label, 'model': get_user_model()._meta.model_name}))
approvers = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.all(), widget=approvers_widget)

class InlineForm(forms.Form):
    class Meta:
        fields = '__all__'

    def __init__(self, args, kwargs):
        super(InlineForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class InlineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InlineFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.template = 'bootstrap5/table_inline_formset.html'

def form_factory(model, fields):
    attrs = {'models': model}
    if fields: attrs['fields'] = fields

    class_name = str("%sForm" % model._meta.object_name)
    return type(class_name, (forms.Form,), fields)

def modelform_factory(model, fields):
    flow = Flow.objects.filter(content_type__model=model._meta.model_name)
    if flow.exists(): fields.remove('approvers') if 'approvers' else fields.insert(0, 'approvers')
    
    attrs = {'model': model}
    if fields: attrs['fields'] = fields

    attrs['widgets'] = {field.name: ListSelect2() for field in model._meta.fields if field.choices}
    Meta = type(str('Meta'), (object,), attrs)

    attrs = {'Meta': Meta}
    helper = FormHelper()
    helper.layout = getattr(model, 'layout', None)

    if flow:
        if 'approvers' in attrs: del attrs['approvers']
        helper.layout = getattr(model, '_layout', None)
    elif 'approvers' in getattr(model, 'layout', None).fields:
        attrs['approvers'] = approvers
        helper.layout = getattr(model, 'layout', None)
            
    attrs['helper'] = helper
    class_name = str("%sModelForm" % model._meta.object_name)
    return type(class_name, (forms.ModelForm,), attrs)


from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordResetForm

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from twilio.rest import Client

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)
UserModel = get_user_model()

class PasswordResetForm(PasswordResetForm):
    email = None
    mobile_number = PhoneNumberField(
        label=_('numéro de téléphone mobile')
    )

    def send_sms(
        self,
        context,
        to_mobile_number,
    ):
        message = "Please go to the following page and choose a new password:\n\n"
        context['url'] = reverse_lazy('password_reset_confirm', kwargs={'uidb64': context.get('uid'), 'token': context.get('token')})
        message += "{protocol}://{domain}{url}".format(**context)
        message = client.messages.create(body=message, from_=settings.TWILIO_NUMBER, to=to_mobile_number)

    def get_users(self, mobile_number):
        """Given an mobile number, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        mobile_number_field_name = 'mobile_number'
        active_users = UserModel._default_manager.filter(
            **{
                #"%s__iexact" % mobile_number_field_name: mobile_number.as_e164,
                mobile_number_field_name: mobile_number,
                "is_active": True
            }
        )
        return list(active_users)

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        mobile_number = self.cleaned_data["mobile_number"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        mobile_number_field_name = 'mobile_number'
        for user in self.get_users(mobile_number):
            user_mobile_number = getattr(user, mobile_number_field_name)
            context = {
                "mobile_number": user_mobile_number.as_e164,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_sms(context, user_mobile_number.as_e164)
