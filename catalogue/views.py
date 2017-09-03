from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Item, Category, Brand
from .forms import ItemFilterForm

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from el_pagination.views import AjaxListView
# Create your views here.


class BaseDetailView(AjaxListView):

    parent_model = Category
    parent_qs = parent_model.objects.all()

    template_name = 'catalogue/category_item_list.html'
    page_template = 'catalogue/item_list_page.html'
    context_object_name = 'items_list'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.parent_model, slug=kwargs['slug'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if 'tags' in self.request.GET or 'order_by' in self.request.GET:
            filter_form = ItemFilterForm(
                self.request.GET,
                tags_qs=self.object.get_tags,
                items_qs=self.object.items.all()
            )
        else:
            filter_form = ItemFilterForm(
                tags_qs=self.object.get_tags,
                items_qs=self.object.items.all()
            )
        if filter_form.is_valid():
            items_list = filter_form.filter_data()
        else:
            items_list = self.object.items.all()
        return items_list

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if 'tags' in self.request.GET or 'order_by' in self.request.GET:
            filter_form = ItemFilterForm(
                self.request.GET,
                tags_qs=self.object.get_tags,
                items_qs=self.object_list
            )
        else:
            filter_form = ItemFilterForm(
                tags_qs=self.object.get_tags,
                items_qs=self.object_list
            )

        ctx['category'] = self.object
        ctx['filter_form'] = filter_form
        return ctx


class CategoryDetailView(BaseDetailView):
    parent_model = Category
    parent_qs = parent_model.objects.filter(type=1)


class GiftDetailView(BaseDetailView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=2)


class BrandDetailView(BaseDetailView):
    parent_model = Brand
    parent_qs = parent_model


class BaseCategoryListView(ListView):
    model = Category
    template_name = 'catalogue/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['links_list'] = [('Categories', reverse('catalogue:category_list')), ('Gifts', reverse('catalogue:gift_list')), ('Brands', reverse('catalogue:brand_list'))]
        return ctx


class CategoryListView(BaseCategoryListView):

    def get_queryset(self):
        qs = super().get_queryset()
        print(qs.filter(type=1))
        return qs.filter(type=1)


class GiftListView(BaseCategoryListView):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=2)


class BrandListView(BaseCategoryListView):
    model = Brand


class ItemDetailView(DetailView):
    model = Item
    template_name = 'catalogue/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_items'] = Item.objects.all()[:15]
        return ctx

    def get_template_names(self):
        if self.request.is_ajax():
            self.template_name = 'catalogue/modal_item_content.html'
        return super().get_template_names()

"""
class CatalogueSearchView(SearchView):
    template_name = 'search/search.html'
    form_class = CalibrationSearch
    queryset = SearchQuerySet().filter(requires_calibration=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

"""