# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-30 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('border_results', '0002_auto_20160629_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_isolate', models.BooleanField(default=True)),
                ('border_quality', models.IntegerField(choices=[(0, 'Precise'), (10, 'Approximate'), (20, 'Not Useable')])),
            ],
        ),
        migrations.AddField(
            model_name='processresult',
            name='evaluation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='border_results.Evaluation'),
        ),
    ]
