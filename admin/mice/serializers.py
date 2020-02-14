from rest_framework import serializers

from .models import Mice


class MiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mice
        fields = '__all__'

