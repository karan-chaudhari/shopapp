# Generated by Django 2.1.5 on 2019-04-24 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20190423_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
