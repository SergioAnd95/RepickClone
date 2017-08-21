from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from .models import LikeList

from catalogue.models import Item
from catalogue.views import BaseDetailView
# Create your views here.


def toggle_like(request, item_slug):

    ctx = {}
    item = get_object_or_404(Item, slug=item_slug)
    if request.likelist.exist_item(item):
        request.likelist.remove_item(item)
        ctx['removed'] = 'ok'
    else:
        request.likelist.add_item(item)
        ctx['added'] = 'ok'

    ctx['likes_count'] = item.get_total_likes
    if request.is_ajax():
        return JsonResponse(ctx)

    return redirect(request.META.get('HTTP_REFERER', '/'))


class LikeListDetailView(BaseDetailView):
    model = LikeList

    def get_object(self, queryset=None):
        self.object = self.request

