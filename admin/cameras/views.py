import json
import datetime

from django.forms.models import model_to_dict
from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.required_keys import required_keys
from common.helpers.login_required import login_required
from common.helpers.models_to_list import models_to_list

from .models import Cameras
from .serializers import CamerasSerializer


class CamerasViews(viewsets.ModelViewSet):
    # TODO: login required
    serializer_class = CamerasSerializer

    @login_required()
    def list(self, request, user):  # pylint: disable=unused-argument
        try:
            login = user['decrypted_cookie']['login']
            cameras = list(Cameras.objects.filter(user=login))

            return create_custom_response(
                status.HTTP_200_OK,
                {'cameras': models_to_list(cameras)}
            )
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None): # pylint: disable=unused-argument
        try:
            camera = model_to_dict(Cameras.objects.get(id=pk))
            return create_custom_response(status.HTTP_200_OK, {'camera': camera})
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys(['user', 'camera'])
    def create(self, request): # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)
            camera = request_data['camera']
            user = request_data['user']

            camera = Cameras.objects.create(**camera, date_added=datetime.datetime.now(), user=user)

            return create_custom_response(
                status.HTTP_201_CREATED,
                {'camera': model_to_dict(camera)['id']}
            )
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    @required_keys(['camera_ids'])
    def delete(self, request):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)
            camera_ids = request_data['camera_ids']

            Cameras.objects.filter(id__in=camera_ids).delete()

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys(['update_fields'])
    def update(self, request, pk=None):  # pylint: disable=unused-argument
        try:
            update_fields = json.loads(request.body)['update_fields']
            Cameras.objects.filter(pk=pk).update(
                **update_fields,
                date_changed=datetime.datetime.now()
            )

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)
