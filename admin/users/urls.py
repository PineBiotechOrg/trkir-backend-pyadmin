from django.conf.urls import url

from .views import UsersViews

users_auth = UsersViews.as_view({
    'post': 'oauth',
})


urlpatterns = [
    url(r'^$', users_auth, name='user-management'),
]
