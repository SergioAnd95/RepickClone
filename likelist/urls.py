from django.conf.urls import url

from . import views

urlpatterns = [
    url('^toggle_like/(?P<item_slug>[-\w]+)/$', views.toggle_like, name='toggle_like')
]