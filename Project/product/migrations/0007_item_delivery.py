# Generated by Django 4.1.3 on 2022-11-13 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_tag_item_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='delivery',
            field=models.TextField(null=True),
        ),
    ]
