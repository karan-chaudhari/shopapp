from django.db import models
from django.utils import timezone

class Post(models.Model):
	title = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)
	category = models.CharField(max_length=100, blank=True)
	timestamp = models.DateTimeField(default=timezone.now)
	img = models.ImageField(upload_to='blog/images')
	content = models.TextField(max_length=2000)

	def __str__(self):
		return self.title