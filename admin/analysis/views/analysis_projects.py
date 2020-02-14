import json

from django.forms.models import model_to_dict
from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.login_required import login_required
from common.helpers.required_keys import required_keys
from common.helpers.models_to_list import models_to_list

from mice.models import Mice
from favorite_mice.models import FavoriteMice
from experiments.helpers.filter_experiments import filter_experiments
from analysis.models.analysis_projects import \
    AnalysisProjects, \
    AnalysisMouseRelation


class AnalysisProjectsViews(viewsets.ModelViewSet):
    @login_required()
    def list(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            projects = list(AnalysisProjects.objects.filter(user_id=user_id))
            projects = filter_experiments(projects, request.GET.get('filters', {}))

            return create_custom_response(
                status.HTTP_200_OK,
                {'projects': projects}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

        # TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602

    @login_required()
    def create(self, request, user):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)

            project_data = {
                **request_data,
                'user_id': user['user_info']['id']
            }

            project = AnalysisProjects.objects.create(**project_data)

            return create_custom_response(
                status.HTTP_201_CREATED,
                {'project': project.id}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)


    @required_keys([
        'project_ids'
    ])
    @login_required()
    def delete(self, request, user):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            request_data = json.loads(request.body)
            project_ids = request_data['project_ids']

            AnalysisProjects.objects.filter(
                user_id=user_id,
                id__in=project_ids
            ).delete()

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    # TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys([
        'title'
    ])
    @login_required()
    def create_from_favorites(self, request, user): # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']
            request_data = json.loads(request.body)
            is_clear_favorites = request_data.get('clear_favorites', False)

            if 'clear_favorites' in request_data.keys():
                del request_data['clear_favorites']

            project_data = {
                **request_data,
                'user_id': user_id
            }

            project = AnalysisProjects.objects.create(**project_data)
            favorite_mice_ids = list(
                FavoriteMice.objects.filter(user_id=user_id).values_list('mouse', flat=True)
            )
            mice = Mice.objects.filter(id__in=favorite_mice_ids)

            mice = [
                AnalysisMouseRelation(
                    analysis_project=project,
                    mouse=mouse
                )
                for mouse in mice
            ]

            AnalysisMouseRelation.objects.bulk_create(mice)

            if is_clear_favorites:
                FavoriteMice.objects.filter(user_id=user_id).delete()

            return create_custom_response(
                status.HTTP_201_CREATED,
                {'project': project.id}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def retrieve(self, request, user, pk=None): # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            project = model_to_dict(AnalysisProjects.objects.get(
                user_id=user_id,
                id=pk
            ))
            project_mice = AnalysisMouseRelation.objects.filter(analysis_project=pk)
            project['mice'] = models_to_list(project_mice)

            return create_custom_response(status.HTTP_200_OK, {'project': project})
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    #TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys([
        'mouse_ids'
    ])
    @login_required()
    def add_mice_to_project(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            request_data = json.loads(request.body)
            mice = Mice.objects.filter(id__in=request_data['mouse_ids'])
            project = AnalysisProjects.objects.get(
                user_id=user_id,
                pk=pk
            )

            mice = [
                AnalysisMouseRelation(
                    analysis_project=project,
                    mouse=mouse
                )
                for mouse in mice
            ]

            AnalysisMouseRelation.objects.bulk_create(mice)

            return create_custom_response(
                status.HTTP_201_CREATED,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TODO: добавить валидацию данных https://tracker.yandex.ru/VPAGROUPDEV-602
    @required_keys([
        'update_fields'
    ])
    @login_required()
    def update_info(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            user_id = user['user_info']['id']

            update_fields = json.loads(request.body)['update_fields']
            AnalysisProjects.objects.filter(
                user_id=user_id,
                pk=pk
            ).update(**update_fields)

            return create_custom_response(status.HTTP_200_OK)
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
