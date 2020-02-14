"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.conf.urls import url


BASE_URL = 'api/v1'


def make_base_url(route_path=None):
    if not route_path:
        return r'^{base_url}/'

    return r'^{base_url}/{path}/'.format(base_url=BASE_URL, path=route_path)


urlpatterns = [
    # Project routes
    url(make_base_url('cameras'), include('cameras.urls')),
    url(make_base_url('experiments'), include('experiments.urls')),
    url(make_base_url('mice'), include('mice.urls')),
    url(make_base_url('analysis'), include('analysis.urls')),
    url(make_base_url('favorite_mice'), include('favorite_mice.urls')),
    url(make_base_url('users'), include('users.urls')),

    # Admin
    url(r'^admin/', admin.site.urls),
]
