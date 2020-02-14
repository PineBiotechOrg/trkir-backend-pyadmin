import json

from django.utils import timezone
from django.forms.models import model_to_dict
from rest_framework import status, viewsets
from django.http.response import StreamingHttpResponse
from django.http import HttpResponse

from common.helpers.create_custom_response import create_custom_response
from common.helpers.login_required import login_required
from common.helpers.models_to_list import models_to_list
from common.helpers.render_image import render_image
from common.helpers.required_keys import required_keys

from mice.models import Mice, MiceLastImages
from mice.serializers import MiceSerializer
from watchers.constants.constants import ExperimentWatcherRequests
from watchers.constants.watcher_requests import WatcherRequests
from experiments.constants.enums import ExperimentStatuses


class MiceViews(viewsets.ModelViewSet):
    serializer_class = MiceSerializer

    @login_required()
    def list(self, request, user): # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            mice = models_to_list(Mice.objects.filter(user_id=user_id))

            return create_custom_response(
                status.HTTP_200_OK,
                {'mice': mice}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def retrieve(self, request, user, pk=None): # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            mouse = model_to_dict(Mice.objects.get(
                user_id=user_id,
                id=pk
            ))

            return create_custom_response(status.HTTP_200_OK, {'mouse': mouse})
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_image(self, request, user, pk=None): # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            image = MiceLastImages.objects.get(
                mouse__user_id=user_id,
                mouse_id=pk,
            ).image.tobytes()

            return StreamingHttpResponse(
                render_image(image),
                content_type='multipart/x-mixed-replace; boundary=frame',
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'mouse_ids'
    ])
    @login_required()
    def delete(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            request_data = json.loads(request.body)
            mouse_ids = request_data['mouse_ids']

            Mice.objects.filter(
                user_id=user_id,
                id__in=mouse_ids
            ).delete()

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'status'
    ])
    @login_required()
    def change_mouse_status(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            new_status = json.loads(request.body)['status']

            model_object_dates = dict()
            if ExperimentStatuses.validate_change_status(new_status):
                if new_status == ExperimentStatuses.Start.value:
                    model_object_dates['date_start'] = timezone.now()
                    new_status = ExperimentStatuses.Continue.value
                if new_status == ExperimentStatuses.Complete.value:
                    model_object_dates['date_end'] = timezone.now()

                model_object = {
                    **model_object_dates,
                    'status': new_status,
                }
                Mice.objects.filter(
                    user_id=user_id,
                    pk=pk
                ).update(**model_object)

                mouse_experiment_id = model_to_dict(Mice.objects.get(id=pk))['experiment']

                WatcherRequests.manage_experiment_watcher(
                    experiment_id=mouse_experiment_id,
                    status=ExperimentWatcherRequests.Update.value
                )

            else:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'wrong status'}
                )

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    # TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @login_required()
    def update_info(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            update_fields = json.loads(request.body)
            Mice.objects.filter(
                user_id=user_id,
                pk=pk
            ).update(**update_fields)

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    # TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys([
        'virus'
    ])
    @login_required()
    def set_virus(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            virus = json.loads(request.body)['virus']

            Mice.objects.filter(
                user_id=user_id,
                pk=pk
            ).update(virus=virus, date_virus=timezone.now())

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)
