# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_remove_item_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='text',
            field=models.TextField(default=''),
        ),
    ]