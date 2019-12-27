from django.conf.urls import url

from .views import ExperimentsViews

experiments_list = ExperimentsViews.as_view({
    'get': 'list',
    'put': 'create',
    'delete': 'delete',
})

experiment_management = ExperimentsViews.as_view({
    'get': 'retrieve',
    'put': 'add_camera_to_experiment',
    'post': 'update_info',
})

experiment_start = ExperimentsViews.as_view({
    'post': 'start_experiment',
})

experiment_complete = ExperimentsViews.as_view({
    'post': 'complete_experiment',
})

experiment_pause = ExperimentsViews.as_view({
    'post': 'pause_experiment',
})

experiment_continue = ExperimentsViews.as_view({
    'post': 'continue_experiment',
})

urlpatterns = [
    url(r'^$', experiments_list, name='experiments-list'),
    url(r'^experiment/(?P<pk>[0-9]+)/?$', experiment_management, name='experiments-management'),
    url(r'^experiment/(?P<pk>[0-9]+)/start_experiment/?$', experiment_start, name='experiment_start'),
    url(r'^experiment/(?P<pk>[0-9]+)/complete_experiment/?$', experiment_complete, name='experiment_complete'),
    url(r'^experiment/(?P<pk>[0-9]+)/pause_experiment/?$', experiment_pause, name='experiment_pause'),
    url(r'^experiment/(?P<pk>[0-9]+)/continue_experiment/?$', experiment_continue, name='experiment_continue'),
]
