from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MainPageListView.as_view(), name='index'),
]