from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def index(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'shop/index.html', context)

def about(request):
    return HttpResponse('About Shop')

def contact(request):
    return HttpResponse('Contact Shop') 

def productView(request):
    return HttpResponse('Our Products')

def tracker(request):
    return HttpResponse('Tracker')

def checkout(request):
    return HttpResponse('Check Out')