from django.shortcuts import render
from django.views.generic import ListView, DetailView

from . import models


class IssueListView(ListView):
    model = models.Issue
    template_name = 'featured/issue_list.html'
    context_object_name = 'issue_list'


class IssueDetailView(DetailView):
    model = models.Issue
    template_name = 'featured/issue_detail.html'
    context_object_name = 'issue'
