# Generated by Django 5.0.7 on 2024-07-27 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0002_alter_shippinginfo_paymenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippinginfo',
            name='address2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]