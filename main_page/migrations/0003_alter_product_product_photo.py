# Generated by Django 4.2 on 2023-05-05 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_photo',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
