from django.contrib.postgres.fields import ArrayField

from django.db import models


class Users(models.Model):
    login = models.CharField(max_length=512)
    cookies = ArrayField(models.CharField(max_length=1024), null=True)
    role = models.CharField(max_length=124, null=True)
