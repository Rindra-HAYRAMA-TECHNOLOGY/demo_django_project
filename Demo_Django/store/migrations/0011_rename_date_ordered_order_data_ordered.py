# Generated by Django 4.2.10 on 2024-02-14 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_order_complete_alter_order_transaction_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_ordered',
            new_name='data_ordered',
        ),
    ]
