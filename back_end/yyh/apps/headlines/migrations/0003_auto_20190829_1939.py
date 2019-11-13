# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-08-29 11:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('headlines', '0002_auto_20190829_1939'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='headlinescollections',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='headlines',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='headlines',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='headlines.Categories', verbose_name='头条分类'),
        ),
        migrations.AddField(
            model_name='headlines',
            name='labels',
            field=models.ManyToManyField(related_name='headlines', through='headlines.HeadlinesLabel', to='questions.AskLables'),
        ),
        migrations.AddField(
            model_name='comments',
            name='headlines',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='headlines.Headlines', verbose_name='头条'),
        ),
        migrations.AddField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='headlines.Comments', verbose_name='父评论'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='broswinghistory',
            name='headlines',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='headlines.Headlines', verbose_name='浏览记录'),
        ),
        migrations.AddField(
            model_name='broswinghistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]