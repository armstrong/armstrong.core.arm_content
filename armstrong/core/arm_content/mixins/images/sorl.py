from .base import BaseImageMixin

try:
    from ...utils.sorl import get_preset_thumbnail

    class SorlImageMixin(BaseImageMixin):
        visual_field_name = 'image'

        def render_visual(preset_label, *args, **kwargs):
            # TODO: Use a template for this.
            return '<img src="%s" />' % get_preset_thumbnail(
                getattr(self, self.visual_field_name, preset_label))

except ImportError:
    pass
