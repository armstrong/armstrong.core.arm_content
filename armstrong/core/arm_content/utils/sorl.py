from __future__ import absolute_import


class InvalidPresetException(Exception):
    pass

try:
    from sorl.thumbnail import get_thumbnail

    def get_preset_thumbnail(file_, label):
        '''A thin wrapper around sorl's get_thumbnail that allows for presets.

        Given an ImageFile (e.g. from an ImageField) and the label of a preset,
        return the ImageFile that represents the thumbnail with the settings
        specified in the preset.'''
        try:
            preset = settings.ARM_VISUAL_PRESETS[label]
        except AttributeError, KeyError:
            raise InvalidPresetException

        dimensions = preset.pop('dimensions')
        return get_thumbnail(file_, dimensions, **preset)

except ImportError:
    pass
