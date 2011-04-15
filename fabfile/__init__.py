from ._utils import *


@task
def clean():
    local('find . -name "*.py[co]" -exec rm {} \;')


@task
def pep8():
    local('find ./armstrong -name "*.py" | xargs pep8', capture=False)


@task
def test():
    settings = {
        'INSTALLED_APPS': (
            'django.contrib.contenttypes',
            'armstrong.core.arm_content',
            'armstrong.core.arm_content.tests.arm_content_support',
        ),
        'ROOT_URLCONF': 'armstrong.core.arm_content.tests.arm_content_support.urls',
        'ARMSTRONG_EXTERNAL_VIDEO_BACKEND': 'armstrong.core.arm_content.video.backends.YouTubeBackend'
    }
    with html_coverage_report():
        run_tests(settings, 'arm_content_support', 'arm_content')

