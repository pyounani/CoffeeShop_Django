# Generated by Django 4.1.3 on 2022-11-13 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_category_company_item_category_item_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Catogories'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
