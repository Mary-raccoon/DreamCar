from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^$', views.index),
    url(r'^search$', views.search),
    url(r'^main$', views.main),
    url(r'^display_cars$', views.display_cars),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^logout$', views.logout),
    url(r'^favorites/(?P<number>\d+)$', views.favorites),
    url(r'^my_fav$', views.my_fav),
    url(r'^new_car$', views.new_car),
    url(r'^add_car$', views.add_car),
    url(r'^destroy_car/(?P<id>\d+)$', views.destroy_car),
    url(r'^remove_fav/(?P<id>\d+)$', views.remove_fav),
    url(r'^edit_car/(?P<id>\d+)$', views.edit_car),
    url(r'^update_car/(?P<id>\d+)$', views.update_car),
    
]                 