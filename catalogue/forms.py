from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Item


class ItemFilterForm(forms.Form):
    class OrderingVars:
        TRENDING = '-when_created'
        POPULAR = '-total_likes'
        EXPENSIVE = '-price'
        CHEAP = 'price'

        ORDERING_CHOICES = (
            (TRENDING, _('Новые')),
            (POPULAR, _('Популярные')),
            (EXPENSIVE, _('Дорогие')),
            (CHEAP, _('Дешевые'))
        )

    order_by = forms.ChoiceField(choices=OrderingVars.ORDERING_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super().__init__(*args, **kwargs)

        self.generate_tags_filter(self.category.get_tags)

    def generate_tags_filter(self, tags_qs):
        self.fields['tags'] = \
            forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                choices=[(tag.id, tag.name) for tag in tags_qs],
                required=False
            )

    def filter_data(self):
        items = self.category.items.all()

        tags = self.cleaned_data.get('tags')
        if tags:
            items = items.filter(tags__id__in=tags).distinct()

        order_by = self.cleaned_data.get('order_by')
        if order_by:
            items = items.order_by(order_by)

        return items