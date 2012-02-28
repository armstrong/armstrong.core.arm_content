from django import template
from armstrong.core.images.sorl import get_preset_thumbnail

register = template.Library()


@register.filter
def thumbnail(value, arg):
    return get_preset_thumbnail(value, arg)
