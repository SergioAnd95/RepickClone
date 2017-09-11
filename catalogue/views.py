from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Item, Category, Brand
from .forms import ItemFilterForm

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from el_pagination.views import AjaxListView
# Create your views here.


class BaseCategoryDetailView(AjaxListView):

    parent_model = Category
    parent_qs = parent_model.objects.all()

    template_name = 'catalogue/category_item_list.html'
    page_template = 'catalogue/item_list_page.html'
    context_object_name = 'items_list'
    back_link = []

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.parent_model, slug=kwargs['slug'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        if 'order_by' in self.request.GET:
            self.filter_form = ItemFilterForm(
                self.request.GET,
                items_qs=self.object.items.all()
            )
        else:
            self.filter_form = ItemFilterForm(items_qs=self.object.items.all())

        items_list = self.filter_form.filter_data()

        return items_list

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['category'] = self.object
        ctx['filter_form'] = self.filter_form
        ctx['back_link'] = (self.back_link[0], reverse(self.back_link[1]))
        return ctx


class BaseCategoryListView(ListView):
    model = Category
    template_name = 'catalogue/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['links_list'] = [('Categories', reverse('catalogue:category_list')), ('Gifts', reverse('catalogue:gift_list')), ('Brands', reverse('catalogue:brand_list'))]
        return ctx


class CategoryDetailView(BaseCategoryDetailView):
    parent_model = Category
    parent_qs = parent_model.objects.filter(type=1)
    back_link = (_('All Categories'), 'catalogue:category_list')


class GiftDetailView(BaseCategoryDetailView):
    back_link = (_('All Gifts'), 'catalogue:gift_list')
    parent_model = Category
    parent_qs = parent_model.objects.filter(type=2)


class BrandDetailView(BaseCategoryDetailView):
    parent_model = Brand
    parent_qs = parent_model
    back_link = (_('All Brands'), 'catalogue:brand_list')


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