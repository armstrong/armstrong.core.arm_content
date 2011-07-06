from .._utils import *

from ...fields.video import EmbeddedVideo
from ...fields.video import EmbeddedVideoField
from ..arm_content_support.models import SimpleMixedinVideoModel


class EmbeddedVideoMixinTestCase(ArmContentTestCase):
    def test_model_has_video_field(self):
        model = SimpleMixedinVideoModel.objects.create()
        self.assertModelHasField(model, "video", EmbeddedVideoField)
        self.assertTrue(isinstance(model.video, EmbeddedVideo))
