from copy import deepcopy

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_preset_args(preset_label, presets=None, defaults=None):
    if presets is None:
        presets = getattr(settings, 'ARMSTRONG_PRESETS', {})

    if not preset_label in presets:
        raise ImproperlyConfigured('The "%s" preset hasn\'t been '
            'configured in your settings module.' % preset_label)
    
    if defaults is None:
        defaults = getattr(settings, 'ARMSTRONG_PRESET_DEFAULTS', {})
    args = deepcopy(defaults)
    args.update(presets[preset_label])
    return args
