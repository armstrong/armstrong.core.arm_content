from __future__ import absolute_import

from sorl.thumbnail import get_thumbnail

from . import presets as presets_utils


def dimensions(width, height):
    s = '%sx%s' % (width if width is not None else '',
        height if height is not None else '')
    # If the width was omitted, we have 'x%(height)s', which is what sorl
    # expects. If the height was omitted, we have '%(width)sx'. sorl
    # expects just width, so strip trailing 'x' characters.
    return s.rstrip('x')

def get_preset_args(preset_label, presets=None, defaults=None):
    args = presets_utils.get_preset_args(preset_label, presets, defaults)
    width = args.pop('width') if 'width' in args else ''
    height = args.pop('height') if 'height' in args else ''
    args['dimensions'] = dimensions(width, height)
    return args

def get_preset_thumbnail(file_, preset_label, presets=None, defaults=None):
    '''A thin wrapper around sorl's get_thumbnail that allows for presets.

    Given an ImageFile (e.g. from an ImageField) and the label of a preset,
    return the ImageFile that represents the thumbnail with the settings
    specified in the preset.'''

    if preset_label == 'original':
        return file_
    args = get_preset_args(preset_label, presets, defaults)
    dimensions = args.pop('dimensions')
    return get_thumbnail(file_, dimensions, **args)
