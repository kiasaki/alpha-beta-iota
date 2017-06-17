from django.conf.urls import url, include

from app import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^trade/$', views.trade, name='trade'),
    url(r'^research/$', views.research, name='research'),
    url(r'^games/$', views.games, name='games'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^accounts/add/$', views.accounts_add, name='accounts-add'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', views.accounts_update, name='accounts-update'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^feed.csv$', views.feed, name='feed'),
    url('^', include('django.contrib.auth.urls')),
]
