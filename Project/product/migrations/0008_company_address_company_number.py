# Generated by Django 4.1.3 on 2022-11-13 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_item_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='number',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
