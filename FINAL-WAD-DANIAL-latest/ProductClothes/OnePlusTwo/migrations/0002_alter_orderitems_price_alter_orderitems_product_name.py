# Generated by Django 5.1.3 on 2025-02-12 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnePlusTwo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='product_name',
            field=models.CharField(max_length=255),
        ),
    ]
