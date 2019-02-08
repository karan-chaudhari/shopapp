from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('productview/', views.productView, name='productView'),
    path('tracker/', views.tracker, name='tracker'),
    path('checkout/', views.checkout, name='checkout')
]
