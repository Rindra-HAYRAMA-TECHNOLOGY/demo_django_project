# Generated by Django 4.2.10 on 2024-02-19 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_order_transaction_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='data_ordered',
            new_name='date_ordered',
        ),
    ]
