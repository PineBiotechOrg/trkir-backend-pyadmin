from django.conf.urls import url

from .views import UsersViews

users_auth = UsersViews.as_view({
    'post': 'oauth',
})

user_management = UsersViews.as_view({
    'get': 'get_user_data',
    'patch': 'update',
})

user_logout = UsersViews.as_view({
    'post': 'delete',
})

client_id = UsersViews.as_view({
    'get': 'get_service_client_id',
})

urlpatterns = [
    url(r'^$', users_auth, name='users-auth'),
    url(r'^user/?$', user_management, name='user-management'),
    url(r'^user/logout/?$', user_logout, name='user-logout'),
    url(r'^service_client_id/?$', client_id, name='client-id'),
]
