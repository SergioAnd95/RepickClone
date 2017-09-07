from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IssueRaw)
class IssueRawAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IssueCell)
class IssueCellAdmin(admin.ModelAdmin):
    pass