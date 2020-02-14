import json

from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.login_required import login_required
from common.helpers.models_to_list import models_to_list
from common.helpers.required_keys import required_keys

from mice.models import Mice
from analysis.constants.constants import \
    HEATMAP_FIELDS, \
    BOXPLOT_FIELDS, \
    TIME_WARPING_FIELDS, \
    SEASONAL_DECOMPOSITION_FIELDS, \
    SEASONAL_DECOMPOSITION_COMPONENTS, \
    PCA_FIELDS
from analysis.constants.enums import Defaults

from analysis.methods.heatmap import HeatMap
from analysis.methods.boxplot import BoxPlot
from analysis.methods.time_warping import TimeWarping
from analysis.methods.seasonal_decomposition import SeasonalDecomposition
from analysis.methods.pca import PCA

from analysis.models.preprocessing import \
    AverageFeaturesMeta, \
    AveragedMiceFeatures
from analysis.models.analysis_projects import AnalysisMouseRelation
from analysis.models.methods import \
    MiceHeatMap, \
    MiceBoxPlot, \
    MiceTimeWarping, \
    MiceSeasonalDecomposition, \
    AnalysisPCA, \
    ExperimentsPCA


class MethodsViews(viewsets.ModelViewSet):
    @login_required()
    def get_mouse_heatmap(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            heatmap = list(
                MiceHeatMap.objects
                    .filter(mouse=pk)
                    .values(*HEATMAP_FIELDS)
            )

            return create_custom_response(
                status.HTTP_200_OK,
                {'heatmap': heatmap}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_heatmap(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            features = models_to_list(
                AveragedMiceFeatures.objects
                    .filter(mouse=pk)
                    .order_by('date')
            )

            heatmap = HeatMap.create(features)

            db_heatmap = [
                MiceHeatMap(
                    **{
                        **heatmap[index],
                        'mouse_id': pk,
                    })
                for index in range(len(heatmap))
            ]

            MiceHeatMap.objects.filter(mouse=pk).delete()
            MiceHeatMap.objects.bulk_create(db_heatmap)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_boxplot(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            boxplot = list(
                MiceBoxPlot.objects
                    .filter(mouse=pk)
                    .values(*BOXPLOT_FIELDS)
            )

            return create_custom_response(
                status.HTTP_200_OK,
                {'boxplot': boxplot}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_boxplot(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=Defaults.AverageFramesCount.value
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no meta for average features (create average features first)'}
                )

            features = models_to_list(
                AveragedMiceFeatures.objects
                    .filter(
                        mouse=pk,
                        meta=meta.id,
                    )
                    .order_by('date')
            )

            #  TODO: boxplots
            boxplot = BoxPlot.create(features)

            db_boxplot = [
                MiceBoxPlot(
                    **{
                        **boxplot[index],
                        'mouse_id': pk,
                    })
                for index in range(len(boxplot))
            ]

            MiceBoxPlot.objects.filter(mouse=pk).delete()
            MiceBoxPlot.objects.bulk_create(db_boxplot)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_time_warping(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            time_warping = list(
                MiceTimeWarping.objects
                    .filter(mouse=pk)
                    .values(*TIME_WARPING_FIELDS)
            )

            return create_custom_response(
                status.HTTP_200_OK,
                {'time_warping': time_warping}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_time_warping(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=Defaults.AverageFramesCount.value
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no meta for average features (create average features first)'}
                )

            features = models_to_list(
                AveragedMiceFeatures.objects
                    .filter(
                        mouse=pk,
                        meta=meta.id,
                    )
                    .order_by('date')
            )

            #  TODO: time_warping
            time_warping = TimeWarping.create(features)

            db_time_warping = [
                MiceTimeWarping(
                    **{
                        **time_warping[index],
                        'mouse_id': pk,
                    })
                for index in range(len(time_warping))
            ]

            MiceTimeWarping.objects.filter(mouse=pk).delete()
            MiceTimeWarping.objects.bulk_create(db_time_warping)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_seasonal_decomposition(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            seasonal_decomposition = list(
                MiceSeasonalDecomposition.objects
                    .filter(mouse=pk)
                    .values(*SEASONAL_DECOMPOSITION_FIELDS)
            )

            return create_custom_response(
                status.HTTP_200_OK,
                {'seasonal_decomposition': seasonal_decomposition}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_seasonal_decomposition(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=Defaults.AverageFramesCount.value
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no meta for average features (create average features first)'}
                )

            features = models_to_list(
                AveragedMiceFeatures.objects
                    .filter(
                        mouse=pk,
                        meta=meta.id,
                    )
                    .order_by('date')
            )

            seasonal_decomposition = SeasonalDecomposition.create(features)

            MiceSeasonalDecomposition.objects.filter(mouse=pk).delete()

            db_seasonal_decomposition = [
                MiceSeasonalDecomposition(
                    **{
                        **seasonal_decomposition[component][index],
                        'mouse_id': pk,
                        'component': component,
                    })
                for component in SEASONAL_DECOMPOSITION_COMPONENTS
                for index in range(len(seasonal_decomposition[component]))
            ]

            MiceSeasonalDecomposition.objects.bulk_create(db_seasonal_decomposition)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'is_days'
    ])
    @login_required()
    def get_project_pca(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            is_days = True if request.GET['is_days'] else False
            project_pca = list(
                AnalysisPCA.objects
                    .filter(
                        analysis_project=pk,
                        is_days=is_days
                    )
                    .values(*PCA_FIELDS)
            )

            return create_custom_response(
                status.HTTP_200_OK,
                {'project_pca': project_pca}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'is_days'
    ])
    @login_required()
    def make_project_pca(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=Defaults.AverageFramesCount.value
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no meta for average features (create average features first)'}
                )
            is_days = json.loads(request.body)['is_days']

            project_mice = AnalysisMouseRelation.objects \
                .filter(analysis_project=pk). \
                values_list('mouse', flat=True)

            mice_features = {
                mouse_id: models_to_list(
                    AveragedMiceFeatures.objects
                        .filter(
                            mouse=mouse_id,
                            meta=meta.id,
                        )
                        .order_by('date')
                )
                for mouse_id in project_mice
            }

            project_pca = PCA.create(mice_features, is_days=is_days)

            AnalysisPCA.objects.filter(
                analysis_project=pk,
                is_days=is_days,
            ).delete()

            db_project_pca = [
                AnalysisPCA(
                    **{
                        **project_pca[index],
                        'analysis_project_id': pk,
                        'meta': meta,
                        'is_days': is_days,
                    })
                for index in range(len(project_pca))
            ]

            AnalysisPCA.objects.bulk_create(db_project_pca)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'is_days'
    ])
    @login_required()
    def get_experiment_pca(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            is_days = True if request.GET['is_days'] else False
            experiment_pca = list(
                ExperimentsPCA.objects
                    .filter(
                        experiment=pk,
                        is_days=is_days,
                    )
                    .values(*PCA_FIELDS)
            )

            return create_custom_response(
                status.HTTP_200_OK,
                {'experiment_pca': experiment_pca}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @required_keys([
        'is_days'
    ])
    @login_required()
    def make_experiment_pca(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=Defaults.AverageFramesCount.value
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no meta for average features (create average features first)'}
                )
            is_days = json.loads(request.body)['is_days']

            experiment_mice = Mice.objects \
                .filter(experiment=pk). \
                values_list('id', flat=True)

            mice_features = {
                mouse_id: models_to_list(
                    AveragedMiceFeatures.objects
                        .filter(
                            mouse=mouse_id,
                            meta=meta.id,
                        )
                        .order_by('date')
                )
                for mouse_id in experiment_mice
            }

            experiment_pca = PCA.create(mice_features, is_days=is_days)

            ExperimentsPCA.objects.filter(
                experiment=pk,
                is_days=is_days,
            ).delete()

            db_experiment_pca = [
                ExperimentsPCA(
                    **{
                        **experiment_pca[index],
                        'experiment_id': pk,
                        'meta': meta,
                        'is_days': is_days,
                    })
                for index in range(len(experiment_pca))
            ]

            ExperimentsPCA.objects.bulk_create(db_experiment_pca)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
