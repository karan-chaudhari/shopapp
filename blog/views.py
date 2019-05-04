from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from shop.models import Product
from .models import Post, Comment
from .utils import naturalDayTime
import json

cateprod = Product.objects.values('cate')
cates = {item['cate'] for item in cateprod}

def home(request):
	post = Post.objects.all()[::-1]
	post_detail = []
	for i in post:
		comment = Comment.objects.filter(post_id=i.slug)
		post_detail.append([i,naturalDayTime(i.timestamp),len(comment)])		
	paginator = Paginator(post_detail,6)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	context = {'posts':posts,'cate':cates}
	return render(request, 'blog/home.html', context)

def post(request, slug):
	recent_post = Post.objects.all()[::-1][0:3]
	post = Post.objects.filter(slug=slug)
	time = naturalDayTime(post[0].timestamp)
	comment = Comment.objects.filter(post_id=slug)
	if comment:
		cmnt = []
		for i in comment:
			cmnt.append([i,naturalDayTime(i.timestamp)])
		context = {'post':post[0],'time':time,'cate':cates,'recent_post':recent_post,'comment':cmnt,'cmnt_len':len(comment)}
		return render(request, 'blog/post.html', context)
	else:	
		context = {'post':post[0],'time':time,'cate':cates,'recent_post':recent_post}
		return render(request, 'blog/post.html', context)	

def comment(request, slug):
	if request.method == "POST":
		username = request.POST.get('username')
		cmnt = request.POST.get('cmnt')	
		if username:
			comment = Comment(post_id=slug, username=username, cmnt=cmnt)
			comment.save()
		if not username:
			name = request.POST.get('name')
			comment = Comment(post_id=slug, username=name, cmnt=cmnt)
			comment.save()
		try:
			cmnt_list = Comment.objects.filter(post_id=slug)
			usercmnt = []
			for i in cmnt_list:
				time = i.timestamp
				usercmnt.append({'username':i.username,'cmnt':i.cmnt,'timestamp':naturalDayTime(i.timestamp),'cmnt_len':len(cmnt_list)})
				response = json.dumps({'usercmnt':usercmnt}, default=str)
			return HttpResponse(response)
		except Exception as e:
			return HttpResponse(e)		
