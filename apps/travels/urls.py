from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add$', views.add, name="add"),
    url(r'^create_trip$', views.create_trip, name="create_trip"),
    url(r'^join/(?P<trip_id>\d+?)/(?P<user_id>\d+?)$', views.join_trip, name="join_trip"),
    url(r'^destination/(?P<trip_id>\d+?)$', views.show_trip, name="show_trip")
]
