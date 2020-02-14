from django.db import models

from common.models import BasicDateModel
from experiments.models import Experiments


class ExperimentWatchers(BasicDateModel):
    experiment = models.ForeignKey(Experiments, on_delete=models.CASCADE)
    container = models.CharField(max_length=512)

    class Meta:
        unique_together = (('experiment', 'container'),)
