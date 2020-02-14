from django.db import models

from common.models import BasicDateModel
from mice.models import Mice
from users.models import Users


class AnalysisProjects(BasicDateModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    title = models.CharField(max_length=512)
    description = models.CharField(max_length=1024, null=True)

    class Meta:
        unique_together = (('user', 'title'),)


class AnalysisMouseRelation(BasicDateModel):
    analysis_project = models.ForeignKey(AnalysisProjects, on_delete=models.CASCADE)
    mouse = models.ForeignKey(Mice, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('analysis_project', 'mouse'),)
