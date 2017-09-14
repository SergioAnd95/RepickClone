from django import forms
from django.utils.translation import ugettext_lazy as _

from haystack.forms import SearchForm


class ItemFilterForm(SearchForm):
    class OrderingVars:
        NEW = '-when_created'
        TRENDING = '-in_trend'
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

        self.items_qs = kwargs.pop('items_qs')
        super().__init__(*args, **kwargs)


    def filter_data(self):

        items = self.items_qs

        if not self.is_valid():
            return items.order_by(self.fields['order_by'].initial, '-when_created')

        order = self.cleaned_data.get('order_by')

        if order:
            items = items.order_by(order, '-when_created')

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

    def filter_data(self):
        items = self.items

        if not self.is_valid():
            return items.order_by(self.fields['order'].initial, '-when_created')

        order = self.cleaned_data.get('order')

        if order:
            items = items.order_by(order, '-when_created')

        return items


class ProccesItemForm(forms.Form):
    excel_file = forms.FileField()

