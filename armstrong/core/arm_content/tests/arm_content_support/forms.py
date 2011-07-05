from django.forms import ModelForm
from .models import SimpleMixedinAuthorModel
from .models import AudioModel


class AudioModelForm(ModelForm):
    class Meta:
        model=AudioModel


class SimpleMixedinAuthorForm(ModelForm):
    class Meta:
        model = SimpleMixedinAuthorModel
