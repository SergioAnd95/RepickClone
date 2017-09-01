from haystack import indexes

from .models import Item


class PersonIndexes(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    brand = indexes.CharField(model_attr='brand__name')

    def get_model(self):
        return Item