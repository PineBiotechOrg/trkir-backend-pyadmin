import numpy as np
from sklearn.decomposition import PCA as PCA_method

from common.helpers.get_random_color import get_random_color
from analysis.constants.enums import FeatureNames
from analysis.constants.constants import \
    FEATURES_FIELDS, \
    FEATURES_FIELDS_WITHOUT_DATE
from analysis.helpers.helpers import \
    transform_list_of_dicts_to_dict_of_lists, \
    find_unique_days_indexes, \
    split_list_by_indexes


class PCA:
    @staticmethod
    def make_mouse_pca_labels_from_days(mouse_id, days_count):
        return ['{}_{}'.format(mouse_id, day) for day in range(days_count)]

    @staticmethod
    def features_dict_to_lists(features):
        return [features[feature] for feature in features.keys()]

    @staticmethod
    def average_list_of_feature_lists(feature_lists, is_days):
        if not is_days:
            return np.mean(feature_lists, axis=1).tolist()
        else:
            return np.mean(feature_lists, axis=2).T.tolist()

    @staticmethod
    def create_data_for_pca(mice_features, is_days):
        if not is_days:
            labels = list(mice_features.keys())

            return [
                labels,
                [
                    PCA.average_list_of_feature_lists(
                        PCA.features_dict_to_lists(
                            transform_list_of_dicts_to_dict_of_lists(
                                mice_features[label],
                                keys=FEATURES_FIELDS_WITHOUT_DATE,
                            )
                        ),
                        is_days=is_days,
                    ) for label in labels
                ]
            ]
        else:
            labels = []
            data_for_pca = []

            for mouse_id in mice_features.keys():
                mouse_features = transform_list_of_dicts_to_dict_of_lists(
                    mice_features[mouse_id],
                    keys=FEATURES_FIELDS,
                )

                mouse_unique_days_indexes = find_unique_days_indexes(mouse_features[FeatureNames.Date.value])
                days_count = len(mouse_unique_days_indexes) - 1

                mouse_features_splitted_by_days = {
                    feature: split_list_by_indexes(
                        mouse_features[feature],
                        mouse_unique_days_indexes,
                    )
                    for feature in FEATURES_FIELDS_WITHOUT_DATE
                }

                mouse_data_for_pca = PCA.average_list_of_feature_lists(
                    PCA.features_dict_to_lists(
                        mouse_features_splitted_by_days
                    ),
                    is_days=is_days,
                )
                data_for_pca += mouse_data_for_pca
                labels += PCA.make_mouse_pca_labels_from_days(mouse_id, days_count)

            return labels, data_for_pca

    @staticmethod
    def create(mice_features, is_days, components_count=3):
        components_count = min([components_count, len(FEATURES_FIELDS_WITHOUT_DATE)])
        pca = PCA_method(n_components=components_count)

        labels, data_for_pca = PCA.create_data_for_pca(mice_features, is_days)

        pca.fit(data_for_pca)
        pca_data = pca.transform(data_for_pca).tolist()

        return [
            {
                **{
                    'PC{}'.format(component + 1): pca_data[ind][component]
                    for component in range(components_count)
                },
                'color': get_random_color(),
                'label': labels[ind],
            }
            for ind in range(len(labels))
        ]
