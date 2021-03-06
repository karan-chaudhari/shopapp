# Generated by Django 2.1.5 on 2019-02-12 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cate',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='subcate',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
