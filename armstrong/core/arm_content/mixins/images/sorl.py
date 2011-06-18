from .base import BaseImageMixin
from ...images.sorl import get_preset_thumbnail

class SorlImageMixin(BaseImageMixin):
    visual_field_name = 'image'

    def render_visual(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        thumbnail = get_preset_thumbnail(
            getattr(self, self.visual_field_name), preset_label, presets, defaults)
        # TODO: Use a template for this.
        return '<img src="%s" />' % thumbnail.url
