from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^friends$', views.friends),
    url(r'^add_friend/(?P<id>\d+$)', views.add_friend),
    url(r'^logout$', views.logout),
    url(r'^user/(?P<id>\d+$)', views.user),
    url(r'^end/(?P<id>\d$)', views.end),



]
