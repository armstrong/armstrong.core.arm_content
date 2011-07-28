from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput
from django.conf import settings


STATIC_URL = getattr(settings, settings.STATIC_URL, "/static/")


class AudioFileWidget(ClearableFileInput):
    class Media:
        css = {
                "all": [STATIC_URL + "skin/jplayer.blue.monday.css",]
        }
        js = [STATIC_URL + "js/jquery.jplayer.min.js",]
 
    def render(self, name, value, attrs):
        self.attrs=attrs
        parent_output = super(AudioFileWidget, self).render(name, value, attrs)
        from  ...fields.audio import AudioFile
        if type(value) is AudioFile:
            template_player = value.render()
        else:
            template_player = ''

        return mark_safe(parent_output + (template_player))
