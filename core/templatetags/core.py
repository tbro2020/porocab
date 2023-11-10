import re
import urllib
from django import template
from django.template.loader_tags import do_include

digital_value = re.compile("^\d+$")
register = template.Library()


@register.filter('getattr')
def getattribute(value, arg):
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'get') and value.get(arg):
        return value[arg]
    elif digital_value.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    return None


@register.filter('urlencode')
def urlencode(value):
    value = {k: v for k, v in value.items() if v}
    return urllib.parse.urlencode(value)


@register.filter('toint')
def toint(value):
    return int(value or 0)