from rest_framework import serializers

from .models import Experiments


class ExperimentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiments
        fields = '__all__'

