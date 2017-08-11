from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^category/$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^category/(?P<slug>[-\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),

    url(r'^gift/$', views.GiftListView.as_view(), name='gift_list'),
    url(r'^gift/(?P<slug>[-\w]+)/$', views.GiftDetailView.as_view(), name='gift_detail'),

    url(r'^brand/$', views.BrandListView.as_view(), name='brand_list'),
    url(r'^brand/(?P<slug>[-\w]+)/$', views.BrandDetailView.as_view(), name='brand_detail'),
]