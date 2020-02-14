from django.db import models

from common.models import BasicDateModel

from users.constants.constants import USERS_UPDATE_KEYS


class Users(BasicDateModel):
    login = models.CharField(max_length=512)

    email = models.CharField(max_length=512, unique=True, null=True)
    phone = models.CharField(max_length=512, unique=True, null=True)

    def update(self, *args, **kwargs):
        if not set(kwargs.keys()).issubset(USERS_UPDATE_KEYS):
            raise Exception

        super(Users, self).update(*args, **kwargs)


class Cookies(BasicDateModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    cookie = models.CharField(max_length=1024, unique=True)

