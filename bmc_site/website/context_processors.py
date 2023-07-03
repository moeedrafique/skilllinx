from django.shortcuts import get_object_or_404
import json
from .filters import *
# from .forms import *
from .models import *


def advertise(request):
    cat = Category.objects.all().order_by('-id')
    city = City.objects.all()
    institutionFinders = CourseOffering.objects.select_related('course').prefetch_related('city').filter()
    myFilter = institutionFilter(request.GET, queryset=institutionFinders)
    institutionFinders = myFilter.qs
    context = {'cat' : cat, 'city': city, 'institutionFinders': institutionFinders, 'myFilter': myFilter}
    return context