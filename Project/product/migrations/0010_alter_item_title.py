# Generated by Django 4.1.3 on 2022-11-13 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_company_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
