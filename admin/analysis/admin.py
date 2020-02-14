from django.contrib import admin

from analysis.models.analysis_projects import \
    AnalysisProjects, \
    AnalysisMouseRelation
from analysis.models.preprocessing import \
    MiceFeatures, \
    AverageFeaturesMeta, \
    AveragedMiceFeatures, \
    NormalizedMiceFeatures, \
    AveragedNormalizedMiceFeatures, \
    AverageHealthyMice, \
    NormalizedAverageHealthyMice
from analysis.models.methods import \
    MiceHeatMap, \
    MiceBoxPlot, \
    MiceTimeWarping, \
    MiceSeasonalDecomposition, \
    AnalysisPCA, \
    ExperimentsPCA

# Analysis projects
admin.site.register(AnalysisProjects)
admin.site.register(AnalysisMouseRelation)

# Preprocessing
admin.site.register(MiceFeatures)
admin.site.register(AverageFeaturesMeta)
admin.site.register(AveragedMiceFeatures)
admin.site.register(NormalizedMiceFeatures)
admin.site.register(AveragedNormalizedMiceFeatures)
admin.site.register(AverageHealthyMice)
admin.site.register(NormalizedAverageHealthyMice)

# Methods
admin.site.register(MiceHeatMap)
admin.site.register(MiceBoxPlot)
admin.site.register(MiceTimeWarping)
admin.site.register(MiceSeasonalDecomposition)
admin.site.register(AnalysisPCA)
admin.site.register(ExperimentsPCA)
