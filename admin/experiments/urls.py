from django.conf.urls import url

from .views.experiments import ExperimentsViews
from .views.suggests import SuggestsViews

experiments_list = ExperimentsViews.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'delete',
})

experiment_management = ExperimentsViews.as_view({
    'get': 'retrieve',
    'put': 'add_camera_to_experiment',
    'patch': 'update_info',
})

change_experiment_status = ExperimentsViews.as_view({
    'post': 'change_experiment_status',
})

experiment_suggests_statuses = SuggestsViews.as_view({
    'get': 'get_statuses'
})

urlpatterns = [
    url(
        r'^$',
        experiments_list,
        name='experiments-list'
    ),
    url(
        r'^experiment/(?P<pk>[0-9]+)/?$',
        experiment_management,
        name='experiments-management'
    ),
    url(
        r'^experiment/(?P<pk>[0-9]+)/change_experiment_status/?$',
        change_experiment_status,
        name='change_experiment_status'
    ),
    url(
        r'^suggests/statuses/?$',
        experiment_suggests_statuses,
    ),
]
