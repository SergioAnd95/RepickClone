from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from catalogue.models import Item
# Create your views here.


def toggle_like(request, item_slug):

    ctx = {}
    item = get_object_or_404(Item, slug=item_slug)
    if request.likelist.exist_item(item):
        request.likelist.remove_item(item)
        ctx['removed'] ='ok'
    else:
        request.likelist.add_item(item)
        ctx['added'] = 'ok'

    if request.is_ajax():
        return JsonResponse(ctx)

    return redirect(request.META.get('HTTP_REFERER', '/'))
