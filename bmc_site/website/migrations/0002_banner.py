# Generated by Django 4.2.2 on 2023-06-28 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='home_main_banners/')),
            ],
            options={
                'verbose_name': 'Banner Image',
                'verbose_name_plural': 'University Images',
            },
        ),
    ]