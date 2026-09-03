from django.contrib import admin
from django.urls import path
from TechApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('service/',views.service, name='service'),
    path('contact/',views.contact, name='contact'),
    path('main/',views.main, name='main'),
]

