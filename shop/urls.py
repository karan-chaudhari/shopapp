from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:cate>', views.category, name='category'),
    path('product/<int:myid>', views.product, name='productView'),
    path('fea-product/<int:myid>', views.fea_product, name='fea_productView'),
    path('tracker/', views.tracker, name='tracker'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
