from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^category/$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^category/(?P<slug>[-\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
]