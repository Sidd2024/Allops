from .models import *
import django_filters
from django.forms import CheckboxSelectMultiple

#Interest filter and Search keyword in title filter for opportunities
class opportunityFilter(django_filters.FilterSet):
    interest = django_filters.MultipleChoiceFilter(field_name='interest', lookup_expr='icontains',choices=my_fields, widget=CheckboxSelectMultiple)
    title = django_filters.CharFilter(field_name='head', lookup_expr='icontains')
    class Meta:
        model = opportunity
        fields = ['interest','head']
