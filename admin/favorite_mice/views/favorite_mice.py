import json

from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.login_required import login_required
from common.helpers.required_keys import required_keys
from common.helpers.models_to_list import models_to_list

from mice.models import Mice

from favorite_mice.models import FavoriteMice
from favorite_mice.serializers import FavoriteSerializer


class FavoriteMiceViews(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    @login_required()
    def list(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            favorite_mice_ids =  FavoriteMice.objects\
                .filter(user_id=user_id)\
                .values_list('mouse', flat=True)
            mice = models_to_list(Mice.objects.filter(id__in=favorite_mice_ids))

            return create_custom_response(
                status.HTTP_200_OK,
                {'favorite': mice}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys([
        'mouse_ids'
    ])
    @login_required()
    def add_mice(self, request, user): # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']
            mouse_ids = json.loads(request.body)['mouse_ids']

            favorite_mice = [
                FavoriteMice(user_id=user_id, mouse_id=mouse_id)
                for mouse_id in mouse_ids
            ]

            FavoriteMice.objects.bulk_create(favorite_mice)

            return create_custom_response(
                status.HTTP_201_CREATED,
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
            mouse_ids = json.loads(request.body)['mouse_ids']

            FavoriteMice.objects.filter(user_id=user_id, mouse_id__in=mouse_ids).delete()

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
