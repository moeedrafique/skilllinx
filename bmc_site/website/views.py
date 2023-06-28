import json
from itertools import chain

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView
from .filters import *
import requests

from .models import *
# Create your views here.
def home(request):
    bannerimage = Banner.objects.all()
    category = Category.objects.all()
    institutionFinders = Courses.objects.select_related('city').prefetch_related('category').filter()
    myFilter = institutionFilter(request.GET, queryset=institutionFinders)
    institutionFinders = myFilter.qs
    context = {'institutionFinders': institutionFinders, 'myFilter': myFilter, "category": category, 'banner_image': bannerimage}
    return render(request, 'index.html', context)

def No(request):
    institutionFinders = Courses.objects.select_related('city').prefetch_related('category').filter()
    myFilter = institutionFilter(request.GET, queryset=institutionFinders)
    institutionFinders = myFilter.qs
    myFilter = institutionFilter(request.GET, queryset=institutionFinders)
    institutionFinders = myFilter.qs
    page = request.GET.get('page', 1)

    paginator = Paginator(institutionFinders, 2)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {'institutionFinders': institutionFinders, 'myFilter': myFilter, 'users':users}
    return render(request, 'course_finder.html', context)


def categoryDetail(request, slug):
    category = Category.objects.get(slug=slug)
    courses = Courses.objects.filter(category=category)
    context = {"category": category, 'courses':courses}
    return render(request, 'category_detail.html', context)


def courseDetail(request, slug):
    courses = Courses.objects.get(slug=slug)
    offer = CourseOffering.objects.filter(course=courses)
    # courses = Courses.objects.filter(category=category)
    context = {'courses':courses, 'offer':offer}
    return render(request, 'course_detail.html', context)


def courseOffering(request,id, slug, category_slug):
    category = Courses.objects.get(category__slug=category_slug, id=id, slug=slug)
    courses = CourseOffering.objects.get(course=category)
    # courses = Courses.objects.filter(category=category)
    context = {'courses':courses}
    return render(request, 'course_offering.html', context)
#
# class blogSearchView(ListView):
#     template_name = 'course_finder.html'
#     paginate_by = 20
#     count = 0
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['count'] = self.count or 0
#         context['query'] = self.request.GET.get('q')
#         return context
#     def get_queryset(self):
#         request = self.request
#         query = request.GET.get('q', None)
#         if query is not None:
#             post_results = Courses.objects.search(query)
#             query_chain = chain(post_results)
#             qs = sorted(query_chain,key=lambda instance: instance.pk, reverse=True)
#             self.count = len(qs)
#             return qs
#         return Courses.objects.none()
#

def Contact(request):
    return render(request, 'contact.html')

def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('email_template_contact.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        clientKey = request.POST['g-recaptcha-response']
        secretKey = '6LdKqWgbAAAAADz2434Dl_b6IohT21zEff4yRVNw'

        captchaData = {
            'secret': secretKey,
            'response': clientKey,
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']
        print('Your success is ', verify)
        if verify:
            email = EmailMessage(
                request.POST['message'],
                template,
                settings.EMAIL_HOST_USER,
                ['alimoeed15@gmail.com']
            )

            email.fail_silently = False
            email.send()
        else:
            return render(request, 'email_contact_fail.html')

    return render(request, 'email_contact_sent.html')