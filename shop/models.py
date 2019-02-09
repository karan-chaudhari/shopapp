from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_cate = models.CharField(max_length=50)
    img = models.ImageField()
    price = models.CharField(max_length=20)
    desc = models.TextField(max_length=1000)
    pub_date = models.DateField()
