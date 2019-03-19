from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from .models import Product, Contact, Feature_Product
from math import ceil

def index(request):    
    feat_prods = Feature_Product.objects.all()[::-1]
    allProd = []
    cateprod = Product.objects.values('cate','id')
    cates = {item['cate'] for item in cateprod}
    for cate in cates:
        prod = Product.objects.filter(cate=cate)[::-1]
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProd.append([prod, nSlides])
    context = {'allProd':allProd, 'feat_prods':feat_prods}            
    return render(request, 'shop/index.html', context)


def about(request):
    return render(request, 'shop/about.html')

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

def product(request, myid):
    product = Product.objects.filter(id=myid)
    context = {'i':product[0]}
    return render(request, 'shop/product.html', context)

def fea_product(request, myid):
    fprod = Feature_Product.objects.filter(id=myid)
    context = {'fprod':fprod[0]}
    return render(request, 'shop/product.html', context)

def search(request, cate=None):
    if 'search' in request.GET:
        search_prod = request.GET["search"]
        prod = Product.objects.filter(Q(product_name__icontains=search_prod)|Q(cate__icontains=search_prod)|Q(subcate__icontains=search_prod))     
        if not prod:
            messages.info(request,"Sorry, no results found!")
        context = {'prod':prod,'search_prod':search_prod}
        return render(request, 'shop/search.html',context)    

def tracker(request):
    return HttpResponse('Tracker')
    
def checkout(request):
    return render(request, 'shop/checkout.html')