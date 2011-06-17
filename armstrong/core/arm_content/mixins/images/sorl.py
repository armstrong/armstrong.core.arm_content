from .base import BaseImageMixin

try:
    from ...utils.sorl import get_preset_thumbnail

    class SorlImageMixin(BaseImageMixin):
        visual_field_name = 'image'

        def render_visual(self, preset_label, *args, **kwargs):
            thumbnail = get_preset_thumbnail(
                getattr(self, self.visual_field_name), preset_label)
            # TODO: Use a template for this.
            return '<img src="%s" />' % thumbnail.url

except ImportError:
    pass
