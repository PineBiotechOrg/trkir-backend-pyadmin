import json
import datetime

from django.forms.models import model_to_dict
from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.required_keys import required_keys

from .models import Mice, Experiments
from .helpers.find_experiment_mice import find_experiment_mice
from .helpers.filter_experiments import filter_experiments
from .helpers.experiment_status_class import ExperimentStatus
from .serializers import ExperimentsSerializer
from cameras.models import Cameras


class ExperimentsViews(viewsets.ModelViewSet):
    # TODO: login required
    serializer_class = ExperimentsSerializer

    @required_keys(['user'])
    def list(self, request):  # pylint: disable=unused-argument
        try:
            user = request.GET['user']

            experiments = list(Experiments.objects.filter(user=user))
            experiments = filter_experiments(experiments, request.GET.get('filters', {}))
            experiments = [{
                'mice': find_experiment_mice(experiment['id']),
                **experiment,
            } for experiment in experiments]

            return create_custom_response(
                status.HTTP_200_OK,
                {'experiments': experiments}
            )
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None): # pylint: disable=unused-argument
        try:
            experiment = model_to_dict(Experiments.objects.get(id=pk))
            experiment_mice = find_experiment_mice(pk)
            experiment['mice'] = experiment_mice

            return create_custom_response(status.HTTP_200_OK, {'experiment': experiment})
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys(['user', 'title'])
    def create(self, request): # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)

            experiment_data = {
                **request_data,
                'date_added': datetime.datetime.now()
            }

            experiment = Experiments.objects.create(**experiment_data)

            return create_custom_response(
                status.HTTP_201_CREATED,
                {'experiment': model_to_dict(experiment)['id']}
            )
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    @required_keys(['experiment_ids'])
    def delete(self, request):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)
            experiment_ids = request_data['experiment_ids']

            Experiments.objects.filter(id__in=experiment_ids).delete()

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    def start_experiment(self, request, pk=None):  # pylint: disable=unused-argument
        try:
            Experiments.objects.filter(pk=pk).update(
                status=ExperimentStatus.ACTIVE.value,
                date_start=datetime.datetime.now(),
                date_changed=datetime.datetime.now(),
            )
            # TODO: start scripts for all mice

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    def complete_experiment(self, request, pk=None):  # pylint: disable=unused-argument
        try:
            Experiments.objects.filter(pk=pk).update(
                status=ExperimentStatus.COMPLETED.value,
                date_changed=datetime.datetime.now(),
                date_end=datetime.datetime.now(),
            )
            # TODO: stop scripts for all mice and maybe do some analysis

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    def pause_experiment(self, request, pk=None):  # pylint: disable=unused-argument
        try:
            Experiments.objects.filter(pk=pk).update(
                status=ExperimentStatus.PAUSE.value,
                date_changed=datetime.datetime.now(),
            )
            # TODO: stop scripts for all mice and mark pause for all mice

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    def continue_experiment(self, request, pk=None):  # pylint: disable=unused-argument
        try:
            Experiments.objects.filter(pk=pk).update(
                status=ExperimentStatus.ACTIVE.value,
                date_changed=datetime.datetime.now(),
            )
            # TODO: start scripts for all mice and mark continue for all mice

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys(['update_fields'])
    def update_info(self, request, pk=None):  # pylint: disable=unused-argument
        try:
            update_fields = json.loads(request.body)['update_fields']
            Experiments.objects.filter(pk=pk).update(
                **update_fields,
                date_changed=datetime.datetime.now(),
            )

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys(['camera'])
    def add_camera_to_experiment(self, request, pk=None):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)
            camera = Cameras.objects.get(id=request_data['camera'])
            experiment = Experiments.objects.get(pk=pk)
            request_data['camera'] = camera
            request_data['experiment'] = experiment
            request_data['user'] = model_to_dict(experiment)['user'],

            mouse = Mice.objects.create(**request_data)

            Experiments.objects.filter(pk=pk).update(
                date_changed=datetime.datetime.now(),
            )

            # TODO: if experiment is active - start script for this mouse

            return create_custom_response(
                status.HTTP_201_CREATED,
                {'mouse': model_to_dict(mouse)['id']}
            )
        except Exception:
            return create_custom_response(status.HTTP_400_BAD_REQUEST)


