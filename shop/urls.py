from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:cate>', views.category, name='category'),
    path('product/<int:myid>', views.product, name='productView'),
    path('tracker/', views.tracker, name='tracker'),
    path('order_tracker/<int:order_id>', views.order_tracker, name='order_tracker'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('update/<int:id>', views.update_profile, name='update'),
    path('order/<int:id>', views.order, name='order'),
]
