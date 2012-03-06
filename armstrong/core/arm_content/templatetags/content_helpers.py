from django import template
from armstrong.core.arm_content.images.sorl import get_preset_thumbnail

register = template.Library()


@register.filter
def thumbnail(value, arg):
    return get_preset_thumbnail(value, arg).url
