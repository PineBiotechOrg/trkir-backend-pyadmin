from django.conf.urls import url

from .views.favorite_mice import FavoriteMiceViews

favorites_list = FavoriteMiceViews.as_view({
    'get': 'list',
    'put': 'add_mice',
    'delete': 'delete',
})

urlpatterns = [
    url(
        r'^$',
        favorites_list,
        name='favorites-list'
    ),
]
