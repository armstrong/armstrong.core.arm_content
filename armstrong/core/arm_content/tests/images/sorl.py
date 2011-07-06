from django.conf import settings

from .._utils import *
from ...images.sorl import get_preset_args


class PresetTestCase(ArmContentTestCase):

    def setUp(self):
        if hasattr(settings, 'ARMSTRONG_PRESETS'):
            self._previous_presets = settings.ARMSTRONG_PRESETS
        else:
            self._previous_presets = None

        settings.ARMSTRONG_PRESETS = {
            'width_only': {'width': 200},
            'height_only': {'height': 300},
            'width_and_height': {
                'width': 75,
                'height': 100,
            },
        }

    def tearDown(self):
        if self._previous_presets is not None:
            settings.ARMSTRONG_PRESETS = self._previous_presets

    def test_width_only(self):
        args = get_preset_args('width_only')
        self.assertEqual(args['dimensions'], '200')

    def test_height_only(self):
        args = get_preset_args('height_only')
        self.assertEqual(args['dimensions'], 'x300')

    def test_width_and_height(self):
        args = get_preset_args('width_and_height')
        self.assertEqual(args['dimensions'], '75x100')
