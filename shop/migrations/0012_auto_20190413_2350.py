# Generated by Django 2.1.5 on 2019-04-13 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_register'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='phone',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]