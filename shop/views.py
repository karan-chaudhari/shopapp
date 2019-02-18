from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Contact
from math import ceil

def index(request):    
    allProd = []
    cateprod = Product.objects.values('cate','id')
    cates = {item['cate'] for item in cateprod}
    for cate in cates:
        prod = Product.objects.filter(cate=cate)[::-1]
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProd.append([prod, range(1,nSlides), nSlides])
    context = {'allProd':allProd}            
    return render(request, 'shop/index.html', context)

def about(request):
    return HttpResponse('About Shop')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        msg = request.POST.get('msg')
        contact = Contact(name=name, email=email, phone=phone, msg=msg)
        contact.save()
        messages.success(request, 'Your details has been submitted. We will response you very soon. Thank you so much.')
    return render(request, 'shop/contact.html') 

def productView(request):
    return HttpResponse('Our Products')

def tracker(request):
    return HttpResponse('Tracker')

def checkout(request):
    return HttpResponse('Check Out')