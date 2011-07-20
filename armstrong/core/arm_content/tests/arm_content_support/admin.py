from django.contrib import admin
from .models import *


admin.site.register(SimpleAuthoredModel)
admin.site.register(AudioModel)
admin.site.register(OverrideAudioModel)
admin.site.register(SorlImage)
