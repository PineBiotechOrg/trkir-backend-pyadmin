from rest_framework import serializers

from analysis.models.analysis_projects import AnalysisProjects


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisProjects
        fields = '__all__'

