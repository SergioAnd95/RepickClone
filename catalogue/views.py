from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Item, Category, Brand
from .forms import ItemFilterForm

from taggit.models import Tag
# Create your views here.


class BaseDetailView(DetailView):
    model = Category
    template_name = 'catalogue/category_detail.html'
    ajax_template_name = 'catalogue/item_list.html'
    context_object_name = 'category'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        filter_form = ItemFilterForm(self.request.GET, category=self.object, initial={'order_by': ItemFilterForm.OrderingVars.TRENDING})

        if filter_form.is_valid():
            items_list = filter_form.filter_data()
        else:
            items_list = self.object.items.all()

        paginator = Paginator(items_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        ctx['items'] = items
        ctx['paginator'] = paginator
        ctx['filter_form'] = filter_form
        return ctx

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return render(self.request, self.ajax_template_name, context)

        return super().render_to_response(context, **response_kwargs)


class CategoryDetailView(BaseDetailView):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=1)


class GiftDetailView(BaseDetailView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=2)


class BrandDetailView(BaseDetailView):
    model = Brand


class BaseCategoryListView(ListView):
    model = Category
    template_name = 'catalogue/category_list.html'
    context_object_name = 'categories'


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