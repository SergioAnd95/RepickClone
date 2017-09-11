from el_pagination.views import AjaxListView

from haystack.generic_views import SearchView
from el_pagination.settings import PAGE_LABEL
from el_pagination.views import AjaxMultipleObjectTemplateResponseMixin

from catalogue.models import Item
from catalogue.forms import MainPageItemFilter

# Create your views here.


class MainPageListView(AjaxListView):
    model = Item
    template_name = 'index_list.html'
    page_template = 'catalogue/item_list_page.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        qs = super().get_queryset()

        if 'order' in self.request.GET:
            self.filter_form = MainPageItemFilter(self.request.GET, items_qs=qs)
        else:
            self.filter_form = MainPageItemFilter(items_qs=qs)

        qs = self.filter_form.filter_data()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter_form'] = self.filter_form
        return ctx


class AjaxSearchView(AjaxListView, SearchView):

    page_kwarg = None
    template_name = 'search/search_list.html'
    page_template = 'search/search_list_page.html'
    context_object_name = 'items_list'

    def get_queryset(self):
        qs = super().get_queryset()
        print(qs)
        return qs

    def get_context_data(self, **kwargs):
        kwargs.update({'page_template': self.page_template})
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_template_names(self):
        """Switch the templates for Ajax requests."""
        request = self.request
        key = 'querystring_key'
        querystring_key = request.GET.get(key,
            request.POST.get(key, PAGE_LABEL))
        print(querystring_key)
        if request.is_ajax() and request.GET.get(self.key):
            return [self.page_template]
        return super(
            AjaxMultipleObjectTemplateResponseMixin, self).get_template_names()