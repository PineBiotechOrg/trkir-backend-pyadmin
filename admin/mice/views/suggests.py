from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.login_required import login_required
from experiments.constants.enums import ExperimentStatuses
from cameras.serializers import CamerasSerializer


class SuggestsViews(viewsets.ModelViewSet):
    """
    get_statuses:
        Return experiment statuses.
    """
    serializer_class = CamerasSerializer

    @login_required()
    def get_statuses(self, request, user):  # pylint: disable=unused-argument
        try:
            return create_custom_response(
                status.HTTP_200_OK,
                {'statuses': ExperimentStatuses.choices_to_json()}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
