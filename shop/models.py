from django.db import models
from django.utils import timezone

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

class Order(models.Model):
    user_id = models.CharField(max_length=50, default="")
    items_json = models.TextField(max_length=5000)
    cartItem = models.CharField(max_length=5000, default="")
    amount = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default="")
    address = models.TextField(max_length=200)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id) + ". " + self.name

class OrderUpdate(models.Model):
    OrderId = models.CharField(max_length=50)
    update_desc = models.CharField(max_length=5000) 
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.OrderId)+ " . " + self.update_desc[0:10] + "...."
        
class UserProfile(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.TextField(max_length=500)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user_id