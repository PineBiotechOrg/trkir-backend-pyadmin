from django.db import models

from common.models import BasicDateModel
from users.models import Users
from experiments.models import Experiments
from experiments.constants.enums import ExperimentStatuses
from cameras.models import Cameras


class Mice(BasicDateModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    camera = models.ForeignKey(Cameras, on_delete=models.DO_NOTHING)
    experiment = models.ForeignKey(Experiments, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=1024, null=True)
    virus = models.CharField(max_length=512, null=True)
    date_virus = models.DateTimeField(null=True)

    status = models.CharField(
        max_length=124,
        choices=ExperimentStatuses.choices(),
        default=ExperimentStatuses.Create.value,
    )

    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)

    class Meta:
        unique_together = (('user', 'camera'), ('camera', 'experiment'), ('experiment', 'name'))


class MouseSimilarMouseRelation(BasicDateModel):
    mouse = models.ForeignKey(
        Mice,
        on_delete=models.CASCADE,
        related_name='mouse'
    )
    similar_mouse = models.ForeignKey(
        Mice,
        on_delete=models.CASCADE,
        related_name='similar_mouse'
    )

    class Meta:
        unique_together = (('mouse', 'similar_mouse'),)


class MiceLastImages(BasicDateModel):
    mouse = models.OneToOneField(
        Mice,
        on_delete=models.CASCADE,
    )
    image = models.BinaryField()


class MiceImages(BasicDateModel):
    mouse = models.ForeignKey(
        Mice,
        on_delete=models.CASCADE,
    )
    image = models.BinaryField()
