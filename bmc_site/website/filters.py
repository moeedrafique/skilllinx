import django_filters
from django_filters import CharFilter, ChoiceFilter, ModelChoiceFilter
from .models import *
from django import forms
from django.forms.widgets import TextInput, ChoiceWidget, Select


class institutionFilter(django_filters.FilterSet):
    #course_short = django_filters.ModelMultipleChoiceFilter(queryset=Courses.objects.select_related('category').all().order_by('course_short'), required=True,
                                                           # widget=forms.Select)
    course_name = CharFilter(field_name='name', lookup_expr="icontains", label='Name',
                      widget=TextInput(attrs={'placeholder': 'Search Universites'}))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all().order_by('category'),required=True,
    widget=forms.Select)
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all() ,required=True,
                                                    widget=forms.Select)
    #category = django_filters.ChoiceFilter(choices=CATEGORY_CHOICES, required=False, widget=forms.Select)

    class Meta:
        model = Courses
        fields = ['category', 'city', 'course_name' ]
        widgets = {
            'category': forms.Select(),
            'city': forms.Select(),

        }
