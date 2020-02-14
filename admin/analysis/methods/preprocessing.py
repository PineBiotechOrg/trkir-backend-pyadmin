from analysis.constants.constants import \
    FEATURES_FIELDS, \
    FEATURES_FIELDS_WITHOUT_DATE
from analysis.constants.enums import Defaults, FeatureNames
from analysis.helpers.helpers import \
    transform_list_of_dicts_to_dict_of_lists, \
    transform_dict_of_lists_to_list_of_dicts, \
    sparse_list, \
    moving_average_list, \
    normalize_list, \
    find_unique_days_indexes, \
    split_list_by_indexes, \
    average_lists_to_list


class Preprocessing:
    @staticmethod
    def average_features(features, average_frames_count):
        # transform features to usable format (feature1: [...], feature2: [...], ...)
        features_dict = transform_list_of_dicts_to_dict_of_lists(
            features,
            keys=FEATURES_FIELDS
        )

        return transform_dict_of_lists_to_list_of_dicts({
            **{
                feature: sparse_list(
                    moving_average_list(
                        sparse_list(
                            features_dict[feature],
                            Defaults.SparseValue.value,
                        ),
                        average_frames_count,
                    ),
                    average_frames_count,
                )
                for feature in FEATURES_FIELDS_WITHOUT_DATE
            },
            # dates always processed separately (no need to average or normalize them)
            FeatureNames.Date.value: sparse_list(
                sparse_list(
                    features_dict[FeatureNames.Date.value],
                    Defaults.SparseValue.value,
                )[:-average_frames_count + 1],  # moving average cuts last (average_frames_count + 1) values
                average_frames_count,
            ),
        })

    @staticmethod
    def normalize_features(features, method):
        # transform features to usable format (feature1: [...], feature2: [...], ...)
        features_dict = transform_list_of_dicts_to_dict_of_lists(
            features,
            keys=FEATURES_FIELDS,
        )

        return transform_dict_of_lists_to_list_of_dicts({
            **{
                feature: normalize_list(features_dict[feature], method)
                for feature in FEATURES_FIELDS_WITHOUT_DATE
            },
            # dates always processed separately (no need to average or normalize them)
            FeatureNames.Date.value: features_dict[FeatureNames.Date.value],
        })

    @staticmethod
    def create_average_healthy(features):
        # transform features to usable format (feature1: [...], feature2: [...], ...)
        features_dict = transform_list_of_dicts_to_dict_of_lists(
            features,
            keys=FEATURES_FIELDS,
        )

        unique_days_indexes = find_unique_days_indexes(features_dict[FeatureNames.Date.value])

        return transform_dict_of_lists_to_list_of_dicts({
            **{
                feature: average_lists_to_list(split_list_by_indexes(
                    features_dict[feature],
                    unique_days_indexes,
                ))
                for feature in FEATURES_FIELDS_WITHOUT_DATE
            },
            # dates always processed separately (no need to average or normalize them)
            FeatureNames.Date.value: \
                features_dict[FeatureNames.Date.value][unique_days_indexes[0]: unique_days_indexes[1]]
        })
