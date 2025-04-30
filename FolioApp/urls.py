from django.contrib import admin
from django.urls import path
from FolioApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('service/',views.service, name='service'),
    path('contact/',views.contact, name='contact'),
    path('starter/',views.starter),
    path('hire-me/', views.paypal_page, name='paypal_page'),
    path('paypal/capture/', views.paypal_capture, name='paypal_capture'),
    path('paypal/receipt/<int:payment_id>/', views.receipt, name='paypal_receipt'),
]

