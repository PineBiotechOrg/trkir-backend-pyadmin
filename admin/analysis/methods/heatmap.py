from analysis.constants.constants import \
    HEATMAP_FIELDS, \
    CAGE_SIZE
from analysis.constants.enums import FeatureNames
from analysis.constants.constants import FEATURES_FIELDS_WITHOUT_DATE


class HeatMap:
    X_CAGE_SCALE = 10
    Y_CAGE_SCALE = 10

    @staticmethod
    def create(features):
        scaled_cage_width = CAGE_SIZE[0] // HeatMap.X_CAGE_SCALE
        scaled_cage_height = CAGE_SIZE[1] // HeatMap.Y_CAGE_SCALE
        heatmap = dict.fromkeys(
            FEATURES_FIELDS_WITHOUT_DATE,
            [
                [0 for i in range(scaled_cage_width)]
                for j in range(scaled_cage_height)
            ]
        )

        for features_dict in features:
            x = int(features_dict[FeatureNames.BodyXCoord.value] // HeatMap.X_CAGE_SCALE)
            y = int(features_dict[FeatureNames.BodyYCoord.value] // HeatMap.Y_CAGE_SCALE)

            for feature in FEATURES_FIELDS_WITHOUT_DATE:
                heatmap[feature][y][x] += 1

        return [{
            HEATMAP_FIELDS[0]: x,
            HEATMAP_FIELDS[1]: y,
            **{
                feature: heatmap[feature][y][x]
                for feature in FEATURES_FIELDS_WITHOUT_DATE
            }
        } for x in range(scaled_cage_width) for y in range(scaled_cage_height)]
