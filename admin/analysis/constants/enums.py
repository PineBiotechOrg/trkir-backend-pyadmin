from common.enums import ChoicesEnum


class NormalizationMethods(ChoicesEnum):
    MinMax = 'min_max'
    Mean = 'mean'


class FeatureNames(ChoicesEnum):
    Date = 'date'

    BodyXCoord = 'x_center'
    BodyYCoord = 'y_center'
    HeadXCoord = 'x_head'
    HeadYCoord = 'y_head'

    Area = 'area'
    Size = 'size'
    Speed = 'speed'
    Rotation = 'rotation'
    Temperature = 'temperature'
    TemperatureSpeed = 'temperature_speed'


class SeasonalDecompositionComponents(ChoicesEnum):
    Trend = 'trend'
    Seasonal = 'seasonal'
    Residual = 'resid'


class Defaults(ChoicesEnum):
    AverageFramesCount = 10
    FeaturesCount = 1
    NormalizationMethod = NormalizationMethods.MinMax.value
    SparseValue = 2
