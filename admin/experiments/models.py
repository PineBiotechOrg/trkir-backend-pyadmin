from django.db import models

from .helpers.experiment_status_class import ExperimentStatus
from cameras.models import Cameras


class Experiments(models.Model):
    user = models.CharField(max_length=512)

    title = models.CharField(max_length=512)
    description = models.CharField(max_length=1024, null=True)
    status = models.CharField(
        max_length=124,
        choices=ExperimentStatus.choices(),
        default=ExperimentStatus.CREATED.value,
    )
    place = models.CharField(max_length=512, null=True)

    date_added = models.DateTimeField()
    date_changed = models.DateTimeField(null=True)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)


class Mice(models.Model):
    user = models.CharField(max_length=512)
    camera = models.ForeignKey(Cameras, on_delete=models.DO_NOTHING)
    experiment = models.ForeignKey(Experiments, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=1024, null=True)
    virus = models.CharField(max_length=512, null=True)

