from django.conf.urls import url, include

from app import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^feed.csv$', views.feed, name='feed'),
    url('^', include('django.contrib.auth.urls')),
]
