from armstrong.dev.tasks import *


settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'armstrong.core.arm_content',
        'armstrong.core.arm_content.tests.arm_content_support',
        'armstrong.core.arm_sections',
        'armstrong.utils.backends',
        'south',
    ),
    'AUTH_PROFILE_MODULE': 'arm_content_support.SimpleProfile',
    'ROOT_URLCONF': 'armstrong.core.arm_content.tests.arm_content_support.urls',
    'ARMSTRONG_EXTERNAL_VIDEO_BACKEND': 'armstrong.core.arm_content.video.backends.YouTubeBackend',
    'ARMSTRONG_EXTERNAL_AUDIO_METADATA_BACKEND':'armstrong.core.arm_content.audio.Id3readerBackend'
}

main_app = "arm_content"
tested_apps = ("arm_content_support", "arm_content", )
