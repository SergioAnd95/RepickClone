from django.views.generic import ListView

from catalogue.models import Item

# Create your views here.


class MainPageListView(ListView):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items'
    paginate_by = 20