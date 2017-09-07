from django import template
from featured.models import Issue

register = template.Library()

@register.inclusion_tag('featured/new_issue.html')
def latest_issue():
    return {'issue':Issue.objects.first()}