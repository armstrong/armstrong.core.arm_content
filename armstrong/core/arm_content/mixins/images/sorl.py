from .base import BaseThumbnailMixin
from ...images.sorl import get_preset_thumbnail

class SorlThumbnailMixin(BaseThumbnailMixin):
    visual_field_name = 'image'

    def render_visual(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        # TODO: Use a template for this.
        return '<img src="%s" />' % self.get_visual_thumbnail_url(preset_label,
            presets, defaults, *args, **kwargs)

    def get_visual_thumbnail_url(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        image_file = getattr(self, self.visual_field_name)
        thumbnail_file = get_preset_thumbnail(image_file, preset_label,
            presets, defaults)
        return thumbnail_file.url
