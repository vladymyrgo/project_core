from haystack import indexes
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')
    date_joined = indexes.DateTimeField(model_attr='date_joined')

    def get_model(self):
        return User
