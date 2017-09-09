from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm as FF, FlatPageAdmin as FA, FlatPage
from django.forms import CharField

from froala_editor.widgets import FroalaEditor

# Register your models here.

admin.site.unregister(FlatPage)


class FlatpageForm(FF):
    content = CharField(widget=FroalaEditor)


@admin.register(FlatPage)
class FlatpageAdmin(FA):
    form = FlatpageForm