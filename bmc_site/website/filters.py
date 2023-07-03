import django_filters
from django_filters import CharFilter, ChoiceFilter, ModelChoiceFilter
from .models import *
from django import forms
from django.forms.widgets import TextInput, ChoiceWidget, Select
from django.db.models import DateTimeField
from django.db.models.functions import ExtractMonth, ExtractYear
from django_filters import FilterSet, CharFilter
from django.db.models import Q


class institutionFilter(django_filters.FilterSet):
    #course_short = django_filters.ModelMultipleChoiceFilter(queryset=Courses.objects.select_related('category').all().order_by('course_short'), required=True,
                                                           # widget=forms.Select)
    search_query  = CharFilter(method='filter_by_search', label='Name',
                      widget=TextInput(attrs={'placeholder': 'Search Courses'}))
    category = django_filters.ModelChoiceFilter(empty_label='All Categories', queryset=Category.objects.all().order_by('category'),
    widget=forms.Select)
    month = CharFilter(field_name='datetime_field', method='filter_by_month')
    year = django_filters.CharFilter(method='filter_by_year')
    city = django_filters.ModelChoiceFilter(empty_label='All Cities', queryset=City.objects.all(),
                                                    widget=forms.Select, to_field_name='id')
    duration = django_filters.ChoiceFilter(
        choices=[    ('One Week', 'One Week'),
    ('Two Weeks', 'Two Weeks'),
    ('Three Weeks', 'Three Weeks'),
    ('Four Weeks', 'Four Weeks'),],
        empty_label='All Durations'
    )
    #category = django_filters.ChoiceFilter(choices=CATEGORY_CHOICES, required=False, widget=forms.Select)

    def filter_by_search(self, queryset, name, value):
        queryset = queryset.filter(
            Q(course__course_code__icontains=value) |
            Q(course__course_name__icontains=value) |
            Q(course__category__category__icontains=value)
        )
        return queryset

    def filter_by_month(self, queryset, name, value):
        month_names = {
            'january': 1,
            'february': 2,
            'march': 3,
            'april': 4,
            'may': 5,
            'june': 6,
            'july': 7,
            'august': 8,
            'september': 9,
            'october': 10,
            'november': 11,
            'december': 12,
        }

        month = month_names.get(value.lower())
        if not month:
            return queryset.none()

        event_time_ids = CourseOffering.objects.filter(start_date__month=month).values_list('id', flat=True)
        queryset = queryset.filter(courseoffering__id__in=event_time_ids)

        return queryset

    def filter_by_year(self, queryset, name, value):
        try:
            year = int(value)
        except ValueError:
            return queryset.none()

        queryset = queryset.filter(courseoffering__start_date__year=year)

        return queryset
    class Meta:
        model = CourseOffering
        fields = ['search_query', 'category', 'month', 'year', 'duration', 'city']
        widgets = {
            'category': forms.Select(),
            'city': forms.Select(),

        }

