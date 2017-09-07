from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IssueListView.as_view(), name='issue_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.IssueDetailView.as_view(), name='issue_detail'),
]