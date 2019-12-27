from django.db import models

from .helpers.camera_status_class import CameraStatus
# from users.models import Users


class Cameras(models.Model):
    # TODO: change after users implementation
    user = models.CharField(max_length=512)

    name = models.CharField(max_length=512)
    ip = models.CharField(max_length=512)
    status = models.CharField(
        max_length=124,
        choices=CameraStatus.choices(),
        default=CameraStatus.OFF.value,
    )
    date_added = models.DateTimeField()
    date_changed = models.DateTimeField(null=True)

    place = models.CharField(max_length=512, null=True)
