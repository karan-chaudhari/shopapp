from django.shortcuts import render
from django.core.paginator import Paginator
from shop.models import Product
from .models import Post

cateprod = Product.objects.values('cate')
cates = {item['cate'] for item in cateprod}

def home(request):
	post = Post.objects.all()[::-1]
	paginator = Paginator(post,6)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	context = {'posts':posts,'cate':cates}
	return render(request, 'blog/home.html', context)

def post(request, slug):
	recent_post = Post.objects.all()[::-1][0:3]
	post = Post.objects.filter(slug=slug)
	context = {'post':post[0],'cate':cates,'recent_post':recent_post}
	return render(request, 'blog/post.html', context)	