from django import template
from django.conf import settings
from django.utils.formats import get_format
from django.utils.translation import get_language

register = template.Library()


# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.simple_tag
def settings_format(name):
    lang = get_language()
    return get_format(name, lang, use_l10n=settings.USE_L10N)
