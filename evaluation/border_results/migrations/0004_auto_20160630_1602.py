# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-30 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('border_results', '0003_auto_20160630_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='processresult',
            name='json_file',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Json File'),
        ),
        migrations.AlterField(
            model_name='processresult',
            name='evaluation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='border_results.Evaluation'),
        ),
    ]
