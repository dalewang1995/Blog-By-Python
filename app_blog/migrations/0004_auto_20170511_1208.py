# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0003_article_auth_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(default='\u672a\u77e5', max_length=10, verbose_name='\u7c7b\u522b'),
        ),
    ]
