from django.conf.urls import url

from .views import CamerasViews

cameras_list = CamerasViews.as_view({
    'get': 'list',
    'put': 'create',
    'delete': 'delete',
})

camera_management = CamerasViews.as_view({
    'get': 'retrieve',
    'post': 'update',
})

urlpatterns = [
    url(r'^$', cameras_list, name='cameras-list'),
    url(r'^camera/(?P<pk>[0-9]+)/?$', camera_management, name='cameras-management'),
]
