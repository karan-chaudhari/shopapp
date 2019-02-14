from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    cate = models.CharField(max_length=50, default="")
    subcate = models.CharField(max_length=50, default="")
    img = models.ImageField(upload_to='shop/images',default="")
    price = models.CharField(max_length=20, default="")
    desc = models.TextField(max_length=1000, blank=True)
    pub_date = models.DateField()

    def __str__(self):
        return self.product_name