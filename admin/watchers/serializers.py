from rest_framework import serializers

from .models import ExperimentWatchers


class ExperimentWatchersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentWatchers
        fields = '__all__'
