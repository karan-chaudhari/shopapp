from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog'),
    path('post/<str:slug>', views.post, name='blog_post'),
]
