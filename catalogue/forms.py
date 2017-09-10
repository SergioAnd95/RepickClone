from django import forms
from django.utils.translation import ugettext_lazy as _

from haystack.forms import SearchForm


class ItemFilterForm(SearchForm):
    class OrderingVars:
        NEW = '-in_trend'
        TRENDING = '-when_created'
        POPULAR = '-total_likes'
        EXPENSIVE = '-price'
        CHEAP = 'price'

        ORDERING_CHOICES = (
            (NEW, _('New')),
            (TRENDING, _('Trending')),
            (POPULAR, _('Popular')),
            (EXPENSIVE, _('$$$')),
            (CHEAP, _('$'))
        )

    order_by = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=OrderingVars.ORDERING_CHOICES,
        required=False,
        initial=OrderingVars.NEW
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

        order_by = self.cleaned_data.get('order_by')
        if order_by:
            items = items.order_by(order_by)

        return items


class MainPageItemFilter(forms.Form):
    class OrderingChoices:
        TRENDING = '-in_trend'
        NEW = '-when_created'
        POPULAR = '-total_likes'
        ORDERING_CHOICES = (
            (TRENDING, 'Trending'),
            (NEW, 'New'),
            (POPULAR, 'Popular')
        )

    order = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=OrderingChoices.ORDERING_CHOICES,
        required=False,
        initial=OrderingChoices.TRENDING
    )

    def __init__(self, *args, **kwargs):
        self.items = kwargs.pop('items_qs')
        super().__init__(*args, **kwargs)

    def clean_order(self):
        if not self['order'].html_name in self.data:
            return self.fields['order'].initial
        return self.cleaned_data['order']

    def filter_data(self):
        order = self.cleaned_data.get('order')
        print(order, 'order')
        items = self.items
        if order:
            items = items.order_by(order, '-when_created')

        return items
