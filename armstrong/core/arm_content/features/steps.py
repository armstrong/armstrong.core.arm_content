from copy import deepcopy

from django.conf import settings
import fudge
import fudge.patcher
from lettuce import *
from sorl.thumbnail.base import ThumbnailBackend

from armstrong.core.arm_content.images.sorl import get_preset_thumbnail, dimensions
from armstrong.core.arm_content.tests.arm_content_support.models import SorlImage


def get_thumbnail_mock(self, file_, dimensions, **kwargs):
    thumbnail = deepcopy(file_)
    thumbnail.storage = file_.storage  # This doesn't copy over for some reason.
    thumbnail._kwargs = kwargs
    thumbnail._kwargs['dimensions'] = dimensions
    return thumbnail

@before.each_scenario
def initialize_world(scenario):
    world.presets = None
    world.defaults = None

@step(u'Given I have an Image that refers to (.*)')
def given_i_have_an_image_that_refers_to_path(step, path):
    world.image = SorlImage(image=path)

@step(u'And I have the following thumbnail presets:')
def and_i_have_the_following_thumbnail_presets(step):
    world.presets = {}
    for hash in step.hashes:
        name = hash.pop('name')
        # Empty columns should be treated as completely omitted.
        for key, value in hash.items():
            if not value:
                del hash[key]
        world.presets[name] = hash

@step(u'When I ask for each preset thumbnail for the image')
@fudge.patcher.with_patched_object(ThumbnailBackend, 'get_thumbnail', get_thumbnail_mock)
def when_i_ask_for_each_preset_thumbnail_for_the_image(step):
    world.thumbnails = dict(
        (preset, get_preset_thumbnail(world.image.image, preset,
            presets=world.presets, defaults=world.defaults))
        for preset in world.presets)

@step(u'When I ask for the (.*) thumbnail for the image')
@fudge.patcher.with_patched_object(ThumbnailBackend, 'get_thumbnail', get_thumbnail_mock)
def when_i_ask_for_a_preset_thumbnail_for_the_image(step, preset_label):
    world.thumbnail = get_preset_thumbnail(world.image.image, preset_label,
        presets=world.presets, defaults=world.defaults)

@step(u'Then the returned thumbnail is the original image')
def then_the_returned_thumbnail_is_the_original_image(step):
    assert world.thumbnail.name == world.image.image.name

@step(u'Then each thumbnail has the specified settings')
def then_each_thumbnail_has_the_specified_settings(step):
    for preset_label, preset in world.presets.items():
        preset = preset.copy()
        thumbnail = world.thumbnails[preset_label]

        # Use the arguments passed to sorl's get_thumbnail as an approximation of
        # getting a thumbnail returned with those settings.
        args = thumbnail._kwargs
        assert args['dimensions'] == dimensions(preset.get('width'), preset.get('height'))
        preset.pop('height', None), preset.pop('width', None)
        for key, value in preset.items():
            assert args[key] == value

@step(u'And I have a default preset quality of 100')
def and_i_have_a_default_preset_quality_of_100(step):
    world.defaults = world.defaults or {}
    world.defaults['quality'] = 100

@step(u'And each thumbnail has a quality of 100')
def and_each_thumbnail_has_a_quality_of_100(step):
    for thumbnail in world.thumbnails.values():
        assert thumbnail._kwargs['quality'] == 100

@step(u'And the thumbnails without specified quality settings have a quality of 100')
def and_the_thumbnails_without_specified_quality_settings_have_a_quality_of_100(step):
    for preset_label, preset in world.presets.items():
        thumbnail = world.thumbnails[preset_label]
        if 'quality' not in preset:
            assert thumbnail._kwargs['quality'] == 100

@step(u'When I render its (\w+) thumbnail')
@fudge.patcher.with_patched_object(ThumbnailBackend, 'get_thumbnail', get_thumbnail_mock)
def when_i_render_its_thumbnail(step, preset_label):
    world.rendered = world.image.render_visual(preset_label, presets=world.presets,
        defaults=world.defaults)

@step(u'Then I see an IMG tag')
def then_i_see_an_img_tag(step):
    assert world.rendered.startswith('<img')
