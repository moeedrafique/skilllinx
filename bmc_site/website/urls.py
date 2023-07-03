from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact-us/', views.Contact, name='contact'),
    path('public-programs/', views.publicPrograms, name='pp'),
    path('customized-training/', views.customizedTraining, name='ct'),
    path('research/', views.research, name='research'),
    path('consulting/', views.consulting, name='consult'),
    path('inhouse-training/', views.inhouseTraining, name='inhouse_train'),
    path('privacy-policy/', views.privacyPolicy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('send/query/', views.sendEmail, name='send_email'),
    path('results/', views.No, name='results'),
    path('training/<slug:slug>/', views.categoryDetail, name='category_detail'),
    path('course/<slug:slug>/', views.courseDetail, name='course_detail'),
    path('location/<slug:slug>/', views.city_course_offerings, name='location'),
    path('courses-in-<slug:slug>-in-<slug:category_slug>/', views.category_course_offerings, name='location'),
    path('course/<slug:category_slug>/<int:id>/<slug:slug>/', views.courseOffering, name='course_offer'),
    path('course/<slug:category_slug>/<int:id>/<slug:slug>/register/', views.registerForm, name='register'),

]