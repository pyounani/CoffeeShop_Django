# Generated by Django 4.1.3 on 2022-11-13 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_category_options_alter_company_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]