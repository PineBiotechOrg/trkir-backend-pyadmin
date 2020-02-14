from statsmodels.tsa.seasonal import seasonal_decompose

from analysis.constants.enums import \
    SeasonalDecompositionComponents
from analysis.constants.constants import \
    FEATURES_FIELDS_WITHOUT_DATE, \
    SEASONAL_DECOMPOSITION_COMPONENTS
from analysis.helpers.helpers import \
    transform_list_of_dicts_to_dict_of_lists, \
    transform_dict_of_lists_to_list_of_dicts


class SeasonalDecomposition:
    @staticmethod
    def create(features):
        features_dict = transform_list_of_dicts_to_dict_of_lists(
            features,
            keys=FEATURES_FIELDS_WITHOUT_DATE,
        )

        result_dict = dict.fromkeys(SEASONAL_DECOMPOSITION_COMPONENTS, {})

        for feature in FEATURES_FIELDS_WITHOUT_DATE:
            sd_result = seasonal_decompose(features_dict[feature])
            result_dict[SeasonalDecompositionComponents.Trend.value][feature] = sd_result.trend
            result_dict[SeasonalDecompositionComponents.Seasonal.value][feature] = sd_result.seasonal
            result_dict[SeasonalDecompositionComponents.Residual.value][feature] = sd_result.resid

        return {
            component: transform_dict_of_lists_to_list_of_dicts(result_dict[component])
            for component in SEASONAL_DECOMPOSITION_COMPONENTS
        }
