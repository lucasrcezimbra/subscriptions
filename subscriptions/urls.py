"""subscriptions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from subscriptions.core.views import export, count_shirt_sizes, count_subscriptions, count_modality, count_teams_cities


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^export/', export),
    url(r'^quantidade-camisetas/$', count_shirt_sizes),
    url(r'^quantidade-inscritos/$', count_subscriptions),
    url(r'^quantidade-modalidades/$', count_modality),
    url(r'^cidades-equipes/$', count_teams_cities),
]
