from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.LikeList)
class LikeListModelAdmin(admin.ModelAdmin):
    list_display = ('when_created', )
    readonly_fields = ('when_created', )