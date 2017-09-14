from django.contrib import admin
from django.conf.urls import url

from . import models
from . import admin_views
# Register your models here.


class RelatedItemsInline(admin.TabularInline):
    model = models.RelatedItems
    fk_name = 'primary'
    raw_id_fields = ['primary', 'recommendation']


@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Brand)
class BrandModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Item)
class ItemModelAdmin(admin.ModelAdmin):
    change_list_template = 'catalogue/admin/change_list.html'
    prepopulated_fields = {"slug": ("title",)}
    inlines = [RelatedItemsInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'import_items/$',
                self.admin_site.admin_view(admin_views.ProcessItemFormView.as_view()),
                name='import_from_file'
            )
        ]
        return custom_urls+urls