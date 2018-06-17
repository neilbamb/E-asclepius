from haystack import indexes
import datetime
from hospital.models import Hospital
    
class HospIndex(indexes.SearchIndex, indexes.Indexable):
        text = indexes.CharField(document=True, use_template=True)
        phno = indexes.CharField(model_attr='user')

        def get_model(self):
            return Hospital



