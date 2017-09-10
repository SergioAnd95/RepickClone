from django.contrib import admin
from . import models
# Register your models here.


class IssueCellInline(admin.TabularInline):
    model = models.IssueCell
    extra = 1


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IssueRaw)
class IssueRawAdmin(admin.ModelAdmin):
    inlines = [
        IssueCellInline,
    ]
