from django.forms import ModelForm
from .models import SimpleMixedinAuthorModel


class SimpleMixedinAuthorForm(ModelForm):
    class Meta:
        model = SimpleMixedinAuthorModel
