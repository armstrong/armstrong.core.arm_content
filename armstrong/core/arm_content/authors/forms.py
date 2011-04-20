from django import forms
from django.contrib.auth.models import User
from django.forms import ModelMultipleChoiceField, TextInput
from django.template.loader import render_to_string


class AuthorsWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        # TODO: handle when value is loaded
        staff = User.objects.filter(is_staff=True)
        staff_widget = ModelMultipleChoiceField(staff).widget.render(
                "%s__users" % name, None)
        override_widget = TextInput().render("%s__override" % name,
                None)
        extra_widget = TextInput().render("%s__extra" % name, None)
        context = {'staff_widget': staff_widget,
                "override_widget": override_widget,
                "extra_widget": extra_widget,
        }
        return render_to_string("armstrong/fields/authors.html", context)
