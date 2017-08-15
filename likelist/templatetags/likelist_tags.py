from django import template

register = template.Library()

@register.filter
def likelist_exist(item, likelist):
    return likelist.exist_item(item)