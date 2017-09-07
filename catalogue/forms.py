from django import forms
from django.utils.translation import ugettext_lazy as _

from haystack.forms import SearchForm


class ItemFilterForm(SearchForm):
    class OrderingVars:
        TRENDING = '-when_created'
        POPULAR = '-total_likes'
        EXPENSIVE = '-price'
        CHEAP = 'price'

        ORDERING_CHOICES = (
            (TRENDING, _('New')),
            (POPULAR, _('Popular')),
            (EXPENSIVE, _('$$$')),
            (CHEAP, _('$'))
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


class MainPageItemFilter(forms.Form):
    class OrderingChoices:
        TRENDING = '-when_created'
        NEW = '-when_created'
        POPULAR = '-total_likes'
        ORDERING_CHOICES = (
            (TRENDING, 'Trending'),
            (NEW, 'New'),
            (POPULAR, 'Popular')
        )

    order_by = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=OrderingChoices.ORDERING_CHOICES,
        required=False,
        initial=OrderingChoices.TRENDING
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
