class BaseImageMixin(object):
    '''Properties of an image-centric content item.'''
    visual_type = 'image'
    is_visual_embedded = False

    def render_visual(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        raise NotImplementedError()
