from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^users/(?P<user_id>\d+)$', views.user_info),
    url(r'^quotes/(?P<quote_id>\d+)/addfave$', views.add_fave),
    url(r'^quotes/(?P<quote_id>\d+)/removefave$', views.remove_fave),
    url(r'^quotes/create$', views.create),
]