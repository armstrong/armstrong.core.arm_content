from copy import deepcopy

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_preset_args(preset_label):
    presets = getattr(settings, 'ARMSTRONG_PRESETS', {})

    if not preset_label in presets:
        raise ImproperlyConfigured('The "%s" preset hasn\'t been '
            'configured in your settings module.' % preset_label)
    
    args = deepcopy(getattr(settings, 'ARMSTRONG_PRESET_DEFAULTS', {}))
    args.update(presets[preset_label])
    return args
