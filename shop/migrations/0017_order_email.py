# Generated by Django 2.1.5 on 2019-04-25 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20190425_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='', max_length=50),
        ),
    ]
