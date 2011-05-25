from django.forms import ModelForm

from .arm_content_support.models import AudioModel

class AudioModelForm(ModelForm):
    class Meta:
        model=AudioModel
