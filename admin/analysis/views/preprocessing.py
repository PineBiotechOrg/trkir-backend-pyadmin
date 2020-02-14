import json
from datetime import datetime

from rest_framework import status, viewsets

from common.helpers.create_custom_response import create_custom_response
from common.helpers.login_required import login_required
from common.helpers.models_to_list import models_to_list
from common.helpers.get_random_color import get_random_color

from analysis.constants.enums import Defaults, FeatureNames
from analysis.constants.constants import \
    FEATURES_FIELDS
from analysis.methods.preprocessing import Preprocessing
from analysis.models.preprocessing import \
    MiceFeatures, \
    AverageFeaturesMeta, \
    AveragedMiceFeatures, \
    NormalizedMiceFeatures, \
    AveragedNormalizedMiceFeatures, \
    AverageHealthyMice, \
    NormalizedAverageHealthyMice


class PreprocessingViews(viewsets.ModelViewSet):
    @login_required()
    def get_mouse_features(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            features_count = int(request.GET.get('features_count', 1))
            features = {
                'color': get_random_color(),
                'data': list(
                    MiceFeatures.objects
                        .filter(mouse=pk)
                        .order_by('date')
                        .values(*FEATURES_FIELDS)
                )[-features_count:]
            }

            return create_custom_response(
                status.HTTP_200_OK,
                {'features': features}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_averaged_features(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            average_frames_count = int(request.GET.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))
            features_count = int(request.GET.get(
                'features_count',
                Defaults.FeaturesCount.value,
            ))

            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=average_frames_count
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no features with this average value'}
                )

            features = {
                'color': get_random_color(),
                'data': list(
                    AveragedMiceFeatures.objects \
                        .filter(
                            meta=meta.id,
                            mouse=pk,
                        )
                        .order_by('date')
                        .values(*FEATURES_FIELDS)
                )[-features_count:]
            }

            return create_custom_response(
                status.HTTP_200_OK,
                {'features': features}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_averaged_features(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)

            average_frames_count = int(request_data.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))

            meta, _ = AverageFeaturesMeta.objects.get_or_create(
                average_frames_value=average_frames_count
            )

            #  find latest date added before
            try:
                latest_added_date = AveragedMiceFeatures.objects\
                    .filter(
                        mouse=pk,
                        meta=meta.id,
                    )\
                    .latest(FeatureNames.Date.value).date
            except Exception:
                latest_added_date = datetime.min

            features = models_to_list(
                MiceFeatures.objects
                    .filter(
                        mouse=pk,
                        date__gt=latest_added_date
                    )
                    .order_by('date')
            )

            averaged_features = Preprocessing.average_features(features, average_frames_count)

            db_averaged_features = [
                AveragedMiceFeatures(
                    **{
                        **averaged_features[features_index],
                        'mouse_id': pk,
                        'meta': meta,
                    }
                )
                for features_index in range(len(averaged_features))
            ]

            AveragedMiceFeatures.objects.bulk_create(db_averaged_features)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_normalized_features(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            normalization_method = request.GET.get(
                'method',
                Defaults.NormalizationMethod.value,
            )
            features_count = int(request.GET.get(
                'features_count',
                Defaults.FeaturesCount.value,
            ))

            features = {
                'color': get_random_color(),
                'data': list(
                    NormalizedMiceFeatures.objects \
                        .filter(
                            mouse=pk,
                            normalization_method=normalization_method,
                        )
                        .order_by('date')
                        .values(*FEATURES_FIELDS)
                )[-features_count:]
            }

            return create_custom_response(
                status.HTTP_200_OK,
                {'features': features}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_normalized_features(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)

            normalization_method = request_data.get(
                'method',
                Defaults.NormalizationMethod.value,
            )

            #  find latest date added before
            try:
                latest_added_date = NormalizedMiceFeatures.objects\
                    .filter(
                        mouse=pk,
                        normalization_method=normalization_method,
                    )\
                    .latest(FeatureNames.Date.value).date
            except Exception:
                latest_added_date = datetime.min

            features = models_to_list(
                MiceFeatures.objects
                    .filter(
                        mouse=pk,
                        date__gt=latest_added_date,
                    )
                    .order_by('date')
            )

            normalized_features = Preprocessing.normalize_features(features, normalization_method)

            db_normalized_features = [
                NormalizedMiceFeatures(
                    **{
                        **normalized_features[features_index],
                        'mouse_id': pk,
                        'normalization_method': normalization_method,
                    }
                )
                for features_index in range(len(normalized_features))
            ]

            NormalizedMiceFeatures.objects.bulk_create(db_normalized_features)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_averaged_normalized_features(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            average_frames_count = int(request.GET.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))
            normalization_method = request.GET.get(
                'method',
                Defaults.NormalizationMethod.value,
            )
            features_count = int(request.GET.get(
                'features_count',
                Defaults.FeaturesCount.value,
            ))

            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=average_frames_count
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no features with this average value'}
                )

            features = {
                'color': get_random_color(),
                'data': list(
                    AveragedNormalizedMiceFeatures.objects \
                        .filter(
                            mouse=pk,
                            normalization_method=normalization_method,
                            meta=meta,
                        )
                        .order_by('date')
                        .values(*FEATURES_FIELDS)
                )[-features_count:]
            }

            return create_custom_response(
                status.HTTP_200_OK,
                {'features': features}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_averaged_normalized_features(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)

            average_frames_count = int(request_data.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))
            normalization_method = request_data.get(
                'method',
                Defaults.NormalizationMethod.value
            )

            meta, _ = AverageFeaturesMeta.objects.get_or_create(
                average_frames_value=average_frames_count
            )

            #  find latest date added before
            try:
                latest_added_date = AveragedNormalizedMiceFeatures.objects\
                    .filter(
                        mouse=pk,
                        normalization_method=normalization_method,
                        meta=meta.id,
                    )\
                    .latest(FeatureNames.Date.value).date
            except Exception:
                latest_added_date = datetime.min

            averaged_features = models_to_list(
                AveragedMiceFeatures.objects
                    .filter(
                        mouse=pk,
                        meta=meta.id,
                        date__gt=latest_added_date,
                    )
                    .order_by('date')
            )

            averaged_normalized_features = Preprocessing.normalize_features(
                averaged_features,
                normalization_method
            )

            db_averaged_normalized_features = [
                AveragedNormalizedMiceFeatures(
                    **{
                        **averaged_normalized_features[features_index],
                        'mouse_id': pk,
                        'normalization_method': normalization_method,
                        'meta': meta,
                    }
                )
                for features_index in range(len(averaged_normalized_features))
            ]

            AveragedNormalizedMiceFeatures.objects.bulk_create(db_averaged_normalized_features)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_average_healthy(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            average_frames_count = int(request.GET.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))

            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=average_frames_count
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no features with this average value'}
                )

            average_healthy = {
                'color': get_random_color(),
                'data': list(
                    AverageHealthyMice.objects \
                        .filter(
                            mouse=pk,
                            meta=meta,
                        )
                        .order_by('date')
                        .values(*FEATURES_FIELDS)
                )
            }

            return create_custom_response(
                status.HTTP_200_OK,
                {'average_healthy': average_healthy}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_average_healthy(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)

            average_frames_count = int(request_data.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))

            meta, _ = AverageFeaturesMeta.objects.get_or_create(
                average_frames_value=average_frames_count
            )

            averaged_features = models_to_list(
                AveragedMiceFeatures.objects
                    .filter(
                        mouse=pk,
                        meta=meta.id
                    )
                    .order_by('date')
            )

            average_healthy = Preprocessing.create_average_healthy(
                averaged_features,
            )

            db_average_healthy = [
                AverageHealthyMice(
                    **{
                        **average_healthy[features_index],
                        'mouse_id': pk,
                        'meta': meta,
                    }
                )
                for features_index in range(len(average_healthy))
            ]

            AverageHealthyMice.objects\
                .filter(
                    mouse=pk,
                    meta=meta.id,
                )\
                .delete()

            AverageHealthyMice.objects.bulk_create(db_average_healthy)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def get_mouse_normalized_average_healthy(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            average_frames_count = int(request.GET.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))
            normalization_method = request.GET.get(
                'method',
                Defaults.NormalizationMethod.value
            )

            try:
                meta = AverageFeaturesMeta.objects.get(
                    average_frames_value=average_frames_count
                )
            except Exception:
                return create_custom_response(
                    status.HTTP_400_BAD_REQUEST,
                    {'reason': 'no features with this average value'}
                )

            average_healthy = {
                'color': get_random_color(),
                'data': list(
                    NormalizedAverageHealthyMice.objects \
                        .filter(
                            mouse=pk,
                            normalization_method=normalization_method,
                            meta=meta,
                        )
                        .order_by('date')
                        .values(*FEATURES_FIELDS)
                )
            }

            return create_custom_response(
                status.HTTP_200_OK,
                {'average_healthy': average_healthy}
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @login_required()
    def make_mouse_normalized_average_healthy(self, request, user, pk=None):  # pylint: disable=unused-argument
        try:
            request_data = json.loads(request.body)

            average_frames_count = int(request_data.get(
                'average_frames_count',
                Defaults.AverageFramesCount.value,
            ))
            normalization_method = request_data.get(
                'method',
                Defaults.NormalizationMethod.value
            )

            meta, _ = AverageFeaturesMeta.objects.get_or_create(
                average_frames_value=average_frames_count
            )

            averaged_normalized_features = models_to_list(
                AveragedNormalizedMiceFeatures.objects
                    .filter(
                        mouse=pk,
                        meta=meta.id,
                        normalization_method=normalization_method,
                    )
                    .order_by('date')
            )

            normalized_average_healthy = Preprocessing.create_average_healthy(
                averaged_normalized_features,
            )

            db_normalized_average_healthy = [
                NormalizedAverageHealthyMice(
                    **{
                        **normalized_average_healthy[features_index],
                        'mouse_id': pk,
                        'normalization_method': normalization_method,
                        'meta': meta,
                    }
                )
                for features_index in range(len(normalized_average_healthy))
            ]

            NormalizedAverageHealthyMice.objects\
                .filter(
                    mouse=pk,
                    normalization_method=normalization_method,
                    meta=meta.id,
                )\
                .delete()

            NormalizedAverageHealthyMice.objects.bulk_create(db_normalized_average_healthy)

            return create_custom_response(
                status.HTTP_200_OK,
            )
        except Exception:
            return create_custom_response(status.HTTP_500_INTERNAL_SERVER_ERROR)
