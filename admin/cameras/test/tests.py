from django.test import TestCase
from django.forms.models import model_to_dict

import json

from cameras.models import Cameras
from cameras.test.test_constants import \
    TEST_CAMERAS_USER, \
    TEST_CAMERAS_CAMERA, \
    TEST_CAMERAS_CREATE_CAMERA, \
    TEST_CAMERAS_CHANGE_FIELDS
from common.testing.utils import make_request, make_without_dates


class TestCameraHelpers(TestCase):
    @classmethod
    def setUpTestData(cls):
        camera_1 = Cameras.objects.create(**TEST_CAMERAS_CAMERA[0])
        camera_2 = Cameras.objects.create(**TEST_CAMERAS_CAMERA[1])

        cls.camera_1 = model_to_dict(camera_1)
        cls.camera_2 = model_to_dict(camera_2)

    def test_get_all_user_cameras(self):
        response = make_request(
            self.client.get,
            'cameras',
            params={'user': TEST_CAMERAS_USER},
        )
        self.assertEqual(response.status_code, 200)

        handler_camera = json.loads(response.content)['cameras']
        self.assertEqual(make_without_dates(handler_camera), make_without_dates([self.camera_1, self.camera_2]))

    def test_get_camera_by_id(self):
        response = make_request(self.client.get, 'cameras/camera/{}'.format(self.camera_1['id']))
        self.assertEqual(response.status_code, 200)

        handler_camera = json.loads(response.content)['camera']
        self.assertEqual(make_without_dates(handler_camera), make_without_dates(self.camera_1))

    def test_get_wrong_camera_by_id(self):
        response = make_request(self.client.get, 'cameras/camera/777')
        self.assertEqual(response.status_code, 400)

    def test_create_camera(self):
        response = make_request(self.client.put, 'cameras', TEST_CAMERAS_CREATE_CAMERA)

        cameras = Cameras.objects.filter(
            user=TEST_CAMERAS_USER,
            **TEST_CAMERAS_CREATE_CAMERA['camera'],
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(len(cameras) == 1)

    def test_simple_change_camera(self):
        changed_camera_fields = {
            'update_fields': TEST_CAMERAS_CHANGE_FIELDS,
        }
        response = make_request(
            self.client.post,
            'cameras/camera/{}'.format(self.camera_1['id']),
            changed_camera_fields
        )
        self.assertEqual(response.status_code, 200)

        camera = model_to_dict(Cameras.objects.get(pk=self.camera_1['id']))

        new_camera = {
            **self.camera_1,
            **changed_camera_fields['update_fields'],
        }

        self.assertEqual(make_without_dates(camera), make_without_dates(new_camera))

    def test_delete_camera(self):
        response = make_request(
            self.client.delete,
            'cameras',
            {'camera_ids': [self.camera_1['id']]}
        )

        self.assertEqual(response.status_code, 200)

        cameras_1 = Cameras.objects.filter(id=self.camera_1['id'])
        cameras_2 = Cameras.objects.filter(id=self.camera_2['id'])

        self.assertTrue(len(cameras_1) == 0)
        self.assertTrue(len(cameras_2) == 1)
