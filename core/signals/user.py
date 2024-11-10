from django.conf import settings
from django.db.models.signals import post_save

from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created, **kwargs):
    if not created: return
    Token.objects.create(user=instance)
    
    # set default password if empty or none
    if not instance.password:
        instance.set_password('Kinshasa-2021')
        instance.save()