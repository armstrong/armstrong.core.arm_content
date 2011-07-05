from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput


class AudioFileWidget(ClearableFileInput):
    def render(self, name, value, attrs):
        parrent_output = super(AudioFileWidget, self).render(name, value, attrs)
        from  ...fields.audio import AudioFile
        if type(value) is AudioFile:
            template_player = value.render()
        else:
            template_player = ''
        return mark_safe(parrent_output + (template_player))
