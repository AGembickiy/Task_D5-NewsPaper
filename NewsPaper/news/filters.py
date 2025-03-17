from django_filters import FilterSet, DateFilter, CharFilter
from django.forms.widgets import TextInput
from .models import Post


class PostFilter(FilterSet):
    date_time_creation = DateFilter(field_name='date_time_creation', lookup_expr='startswith', widget=TextInput(attrs={'type': 'date'}))
    author__user__first_name = CharFilter(field_name='author__user__first_name', lookup_expr='icontains')
    author__user__last_name = CharFilter(field_name='author__user__last_name', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['date_time_creation', 'author__user__first_name', 'author__user__last_name' ]





