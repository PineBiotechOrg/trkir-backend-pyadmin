import json

from django.forms.models import model_to_dict
from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.required_keys import required_keys
from common.helpers.login_required import login_required
from common.helpers.models_to_list import models_to_list

from users.models import Users
from cameras.models import Cameras
from cameras.serializers import CamerasSerializer


class CamerasViews(viewsets.ModelViewSet):
    serializer_class = CamerasSerializer

    @login_required()
    def list(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']
            cameras = list(Cameras.objects.filter(user_id=user_id))

            return create_custom_response(
                status.HTTP_200_OK,
                {'cameras': models_to_list(cameras)}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def retrieve(self, request, user, pk=None): # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            camera = model_to_dict(Cameras.objects.get(
                user_id=user_id,
                id=pk
            ))
            return create_custom_response(status.HTTP_200_OK, {'camera': camera})
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys([
        'ip',
        'name'
    ])
    @login_required()
    def create(self, request, user): # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)
            camera_data = {
                **request_data,
                'user_id': user['user_info']['id']
            }

            camera = Cameras.objects.create(**camera_data)

            return create_custom_response(
                status.HTTP_201_CREATED,
                {'camera': camera.id}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'camera_ids'
    ])
    @login_required()
    def delete(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            request_data = json.loads(request.body)
            camera_ids = request_data['camera_ids']

            Cameras.objects.filter(
                user_id=user_id,
                id__in=camera_ids
            ).delete()

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @login_required()
    def update(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            update_fields = json.loads(request.body)
            Cameras.objects.filter(
                user_id=user_id,
                pk=pk
            ).update(**update_fields)

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
