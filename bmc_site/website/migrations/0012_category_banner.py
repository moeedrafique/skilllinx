# Generated by Django 4.2.2 on 2023-07-03 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_city_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='category_banners/'),
        ),
    ]
