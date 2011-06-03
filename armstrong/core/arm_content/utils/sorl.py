from __future__ import absolute_import

from . import presets


def get_preset_args(preset_label):
    args = presets.get_preset_args(preset_label)
    width = args.pop('width') if 'width' in args else ''
    height = args.pop('height') if 'height' in args else ''
    dimensions = '%sx%s' % (width, height)

    # If the width was omitted, we have 'x%(height)s', which is what sorl
    # expects. If the height was omitted, we have '%(width)sx'. sorl
    # expects just width, so strip trailing 'x' characters.
    args['dimensions'] = dimensions.rstrip('x')

    return args

try:
    from sorl.thumbnail import get_thumbnail

    def get_preset_thumbnail(file_, preset_label):
        '''A thin wrapper around sorl's get_thumbnail that allows for presets.

        Given an ImageFile (e.g. from an ImageField) and the label of a preset,
        return the ImageFile that represents the thumbnail with the settings
        specified in the preset.'''

        args = get_preset_args(preset_label)
        dimensions = args.pop('dimensions')
        return get_thumbnail(file_, dimensions, **args)

except ImportError:
    pass
