from django.views.generic import ListView

from catalogue.models import Item
from catalogue.forms import MainPageItemFilter

# Create your views here.


class MainPageListView(ListView):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        qs = super().get_queryset()

        if 'order_by' in self.request.GET:
            self.filter_form = MainPageItemFilter(self.request.GET, items_qs=qs)
        else:
            self.filter_form = MainPageItemFilter(items_qs=qs)

        if self.filter_form.is_valid():
            qs = self.filter_form.filter_data()

        if self.request.is_ajax():
            self.template_name='catalogue/item_list_page.html'

        return qs[:18]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter_form'] = self.filter_form
        return ctx