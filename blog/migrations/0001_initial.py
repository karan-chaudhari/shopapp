# Generated by Django 2.1.5 on 2019-05-02 19:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('img', models.ImageField(upload_to='blog/images')),
                ('content', models.TextField(max_length=2000)),
            ],
        ),
    ]
