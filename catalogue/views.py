from django.views.generic import ListView, DetailView

from .models import Item, Category, Brand

from taggit.models import Tag
# Create your views here.


class BaseDetailView(DetailView):
    model = Category
    template_name = 'catalogue/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category_tags'] = Tag.objects.filter(item__categories__in=[self.object]).distinct()
        return ctx


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

    def get_context_data(self, **kwargs):
        ctx = super(BaseDetailView, self).get_context_data(**kwargs)
        ctx['category_tags'] = Tag.objects.filter(item__brand__in=[self.object]).distinct()
        return ctx


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