from rest_framework import serializers

from .models import Cameras


class CamerasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameras
        fields = '__all__'
