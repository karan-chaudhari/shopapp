from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    phone = models.CharField(max_length=15)
    msg = models.TextField(max_length=500)

    def __str__(self):
        return self.name

class Feature_Product(models.Model):
    product_name = models.CharField(max_length=50)
    cate = models.CharField(max_length=50, default="", blank=True)
    subcate = models.CharField(max_length=50, default="", blank=True)
    img = models.ImageField(upload_to='shop/images',default="")
    price = models.CharField(max_length=20, default="")
    desc = models.TextField(max_length=1000, blank=True)
    pub_date = models.DateField()

    def __str__(self):
        return self.product_name

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    cate = models.CharField(max_length=50, default="", blank=True)
    subcate = models.CharField(max_length=50, default="", blank=True)
    img = models.ImageField(upload_to='shop/images',default="")
    price = models.CharField(max_length=20, default="")
    desc = models.TextField(max_length=1000, blank=True)
    pub_date = models.DateField()

    def __str__(self):
        return self.product_name        