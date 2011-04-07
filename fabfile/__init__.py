from ._utils import *

@task
def test():
    settings = {
        'INSTALLED_APPS': (
            'django.contrib.contenttypes',
            'armstrong.core.arm_content',
            'armstrong.core.arm_content.tests.arm_content_support',
        ),
        'ROOT_URLCONF': 'armstrong.core.arm_content.tests.arm_content_support.urls',
    }
    with html_coverage_report():
        run_tests(settings, 'arm_content_support', 'arm_content')

