# Generated by Django 5.0.2 on 2024-02-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_user_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
