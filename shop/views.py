from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil

def index(request):    
    allProd = []
    cateprod = Product.objects.values('cate','id')
    cates = {item['cate'] for item in cateprod}
    for cate in cates:
        prod = Product.objects.filter(cate=cate)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProd.append([prod, range(1,nSlides), nSlides])
    context = {'allProd':allProd}            
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