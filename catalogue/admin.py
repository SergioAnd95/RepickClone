from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Brand)
class BrandModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Item)
class ItemModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}