from armstrong.dev.tasks import *


settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        'armstrong.apps.content',
        'armstrong.core.arm_access',
        'armstrong.core.arm_content',
        'armstrong.core.arm_content.tests.arm_content_support',
        'armstrong.core.arm_sections',
        'armstrong.utils.backends',
        'south',
        'lettuce.django',
        'sorl.thumbnail',
        'taggit',
    ),
    'AUTH_PROFILE_MODULE': 'arm_content_support.SimpleProfile',
    'ROOT_URLCONF': 'armstrong.core.arm_content.tests.arm_content_support.urls',
    'ARMSTRONG_EXTERNAL_VIDEO_BACKEND': 'armstrong.core.arm_content.video.backends.YouTubeBackend',
    'ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND':'armstrong.apps.audio.backends.id3reader.Id3readerBackend',
    'MEDIA_URL': '/media/',
    'STATIC_ROOT':'./armstrong/core/arm_content/tests/arm_content_support/static/',
    'STATIC_URL':'/static/',
    'ARMSTRONG_PRESETS': {
        'small_square': {'width': 75, 'height': 75, 'crop': '50%'},
        'qvga': {'width': 320, 'height': 240},
    },
    'SITE_ID': '1',
}

full_name = "armstrong.core.arm_content"
main_app = "arm_content"
tested_apps = ("arm_content_support", "arm_content", )
pip_install_first = True
