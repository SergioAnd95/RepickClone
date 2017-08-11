from django.views.generic import ListView, DetailView

from .models import Item, Category
# Create your views here.


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalogue/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=1)


class CategoryListView(ListView):
    model = Category
    template_name = 'catalogue/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=1)