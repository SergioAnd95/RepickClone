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

    order_by = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=OrderingVars.ORDERING_CHOICES,
        required=False,
        initial=OrderingVars.TRENDING
    )

    def __init__(self, *args, **kwargs):
        tags_qs = kwargs.pop('tags_qs')
        self.items_qs = kwargs.pop('items_qs')
        super().__init__(*args, **kwargs)

        self.generate_tags_filter(tags_qs)

    def generate_tags_filter(self, tags_qs):
        self.fields['tags'] = \
            forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                choices=[(tag.id, tag.name) for tag in tags_qs],
                required=False
            )

    def filter_data(self):
        items = self.items_qs

        tags = self.cleaned_data.get('tags')
        if tags:
            items = items.filter(tags__id__in=tags).distinct()

        order_by = self.cleaned_data.get('order_by')
        if order_by:
            items = items.order_by(order_by)

        return items


a = forms.RadioSelect
class SwitchButtonSelect(forms.RadioSelect):
    template_name = ''

# TODO: create widgets

class MainPageItemFilter(forms.Form):
    class OrderingChoices:
        RECENT = '-when_created'
        POPULAR = '-total_likes'
        ORDERING_CHOICES = (
            (RECENT, 'recent'),
            (POPULAR, 'popular')
        )

    order_by = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=OrderingChoices.ORDERING_CHOICES,
        required=False,
        initial=OrderingChoices.RECENT
    )

    def __init__(self, *args, **kwargs):
        self.items = kwargs.pop('items_qs')
        super().__init__(*args, **kwargs)

    def filter_data(self):
        order_by = self.cleaned_data.get('order_by')
        items = self.items
        if order_by:
            items = items.order_by(order_by)

        return items
