from django.db import models

from common.models import BasicDateModel
from users.models import Users
from .constants.enums import ExperimentStatuses


class Experiments(BasicDateModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    title = models.CharField(max_length=512)
    description = models.CharField(max_length=1024, null=True)
    status = models.CharField(
        max_length=124,
        choices=ExperimentStatuses.choices(),
        default=ExperimentStatuses.Create.value,
    )
    place = models.CharField(max_length=512, null=True)

    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)

    class Meta:
        unique_together = (('user', 'title'),)
