from django.db import models

from common.models import BasicDateModel
from mice.models import Mice
from analysis.constants.enums import \
    NormalizationMethods


class Features(BasicDateModel):
    mouse = models.ForeignKey(Mice, on_delete=models.CASCADE)

    date = models.DateTimeField()

    x_head = models.FloatField()
    y_head = models.FloatField()

    x_center = models.FloatField()
    y_center = models.FloatField()

    area = models.FloatField()
    size = models.FloatField()
    speed = models.FloatField()
    rotation = models.FloatField()
    temperature = models.FloatField()
    temperature_speed = models.FloatField()

    class Meta:
        abstract = True


class MiceFeatures(Features):
    pass


class AverageFeaturesMeta(BasicDateModel):
    # moving average window width (in frames)
    average_frames_value = models.IntegerField(unique=True)


class AveragedMiceFeatures(Features):
    meta = models.ForeignKey(AverageFeaturesMeta, on_delete=models.CASCADE)


# feature values from 0 to 1
class NormalizedMiceFeatures(Features):
    normalization_method = models.CharField(
        max_length=124,
        choices=NormalizationMethods.choices()
    )


# feature values from 0 to 1
class AveragedNormalizedMiceFeatures(Features):
    meta = models.ForeignKey(AverageFeaturesMeta, on_delete=models.CASCADE)
    normalization_method = models.CharField(
        max_length=124,
        choices=NormalizationMethods.choices()
    )


class AverageHealthyMice(Features):
    meta = models.ForeignKey(AverageFeaturesMeta, on_delete=models.CASCADE)


class NormalizedAverageHealthyMice(Features):
    meta = models.ForeignKey(AverageFeaturesMeta, on_delete=models.CASCADE)
    normalization_method = models.CharField(
        max_length=124,
        choices=NormalizationMethods.choices()
    )
