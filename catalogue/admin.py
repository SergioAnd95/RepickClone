from django.contrib import admin

from . import models
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
    prepopulated_fields = {"slug": ("title",)}
    inlines = [RelatedItemsInline]