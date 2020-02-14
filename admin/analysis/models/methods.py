from django.db import models

from common.models import BasicDateModel
from experiments.models import Experiments
from analysis.constants.enums import SeasonalDecompositionComponents
from analysis.models.analysis_projects import AnalysisProjects
from analysis.models.preprocessing import \
    Features, \
    AverageFeaturesMeta


class MiceHeatMap(Features):
    x = models.FloatField()
    y = models.FloatField()

    date = None


# need this (table similar to Features)
class MiceBoxPlot(Features):
    pass


class MiceTimeWarping(Features):
    meta = models.ForeignKey(AverageFeaturesMeta, on_delete=models.CASCADE)


class MiceSeasonalDecomposition(Features):
    meta = models.ForeignKey(AverageFeaturesMeta, on_delete=models.CASCADE)
    component = models.CharField(
        max_length=124,
        choices=SeasonalDecompositionComponents.choices()
    )


class PCA(BasicDateModel):
    meta = models.ForeignKey(
        AverageFeaturesMeta,
        on_delete=models.CASCADE
    )

    PC1 = models.FloatField()
    PC2 = models.FloatField()
    PC3 = models.FloatField(null=True)
    PC4 = models.FloatField(null=True)
    PC5 = models.FloatField(null=True)

    label = models.CharField(max_length=124)
    color = models.CharField(max_length=124, null=True)

    is_days = models.BooleanField()

    class Meta:
        abstract = True


class AnalysisPCA(PCA):
    analysis_project = models.ForeignKey(AnalysisProjects, on_delete=models.CASCADE)


class ExperimentsPCA(PCA):
    experiment = models.ForeignKey(Experiments, on_delete=models.CASCADE)
