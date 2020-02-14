from django.conf.urls import url

from .views.mice import MiceViews
from .views.suggests import SuggestsViews


mice_list = MiceViews.as_view({
    'get': 'list',
    'delete': 'delete',
})

mouse_management = MiceViews.as_view({
    'get': 'retrieve',
    'patch': 'update_info',
})

mouse_image = MiceViews.as_view({
    'get': 'get_image',
})

mouse_virus = MiceViews.as_view({
    'post': 'set_virus',
})

change_mouse_status = MiceViews.as_view({
    'post': 'change_mouse_status',
})

mouse_suggests_statuses = SuggestsViews.as_view({
    'get': 'get_statuses'
})

urlpatterns = [
    url(
        r'^$',
        mice_list,
        name='mice-list'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/?$',
        mouse_management,
        name='mouse-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/image/?$',
        mouse_image,
        name='mouse-management'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/virus/?$',
        mouse_virus,
        name='mouse-virus'
    ),
    url(
        r'^mouse/(?P<pk>[0-9]+)/change_mouse_status/?$',
        change_mouse_status,
        name='change_mouse_status'
    ),
    url(
        r'^suggests/statuses/?$',
        mouse_suggests_statuses,
    ),
]
