# Generated by Django 3.0.6 on 2020-05-23 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(default='avater.jpg', upload_to='media/'),
        ),
    ]
