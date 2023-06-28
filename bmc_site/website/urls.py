from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact-us/', views.Contact, name='contact'),
    path('send/query/', views.sendEmail, name='send_email'),
    path('results/', views.No, name='results'),
    path('training/<slug:slug>/', views.categoryDetail, name='category_detail'),
    path('course/<slug:slug>/', views.courseDetail, name='course_detail'),
    path('course/<slug:category_slug>/<int:id>/<slug:slug>/', views.courseOffering, name='course_offer'),

]