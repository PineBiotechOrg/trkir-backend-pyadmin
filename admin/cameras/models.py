from django.db import models

from common.models import BasicDateModel
from users.models import Users


class Cameras(BasicDateModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    name = models.CharField(max_length=512)
    ip = models.CharField(max_length=512)

    place = models.CharField(max_length=512, null=True)

    class Meta:
        unique_together = (('user', 'ip'),)
