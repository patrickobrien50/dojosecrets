from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^makePost$', views.makePost),
    url(r'^likePost$', views.likePost),
    url(r'^mostLikes$', views.mostLikes),
    url(r'^deletePost$', views.deletePost)
]
