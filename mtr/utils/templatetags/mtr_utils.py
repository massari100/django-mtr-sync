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


@register.simple_tag
def format_get_values(request, name, key):
    GET = request.GET.copy()
    key = str(key)
    value = GET.get(name, None)

    if value is not None and key in value:
        value = ','.join(filter(lambda v: key != v, value.split(',')))
    else:
        value = value.split(',') if value else []
        value = ','.join(value + [key])

    if value:
        GET[name] = value
    else:
        GET.pop(name, None)
    params = GET.urlencode()

    return '{}?{}'.format(request.path, params)


@register.simple_tag
def request_path_replace(request, key, value=None):
    GET = request.GET.copy()
    if value:
        GET[key] = value
    else:
        GET.pop(key, None)
    GET.pop('page', None)
    params = GET.urlencode()
    return '{}?{}'.format(request.path, params)


@register.filter
def split(string, separator):
    return string.split(separator)
