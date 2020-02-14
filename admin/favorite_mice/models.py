from django.db import models

from common.models import BasicDateModel
from mice.models import Mice
from users.models import Users


class FavoriteMice(BasicDateModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    mouse = models.ForeignKey(Mice, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'mouse'),)


