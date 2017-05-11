# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField('id', primary_key=True)
    permission = models.IntegerField('权限')
    auth = models.CharField('作者', max_length=40)
    pwd = models.CharField('密码', max_length=256)
    email = models.CharField('邮箱', max_length=40)

    def __str__(self):
        return self.auth


class Article(models.Model):
    id = models.AutoField('id', primary_key=True)
    auth_id = models.ForeignKey(User)
    auth_name = models.CharField('作者', max_length=10, default='admin')
    category = models.CharField('类别', max_length=10, default='未知')
    title = models.CharField('标题', max_length=256)
    content = models.TextField('内容', default='', blank=True)
    published = models.BooleanField('正式发布', default=True)
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.title
