from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    pub_date = models.DateField()
