# Generated by Django 5.0.7 on 2024-07-27 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_alter_customer_phone_number_and_more'),
        ('Customer', '0003_alter_shippinginfo_address2'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippinginfo',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Account.customer'),
        ),
    ]
