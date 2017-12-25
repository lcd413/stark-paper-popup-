# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-22 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20171221_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.IntegerField(unique=True, verbose_name='部门编号'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Department', to_field='code', verbose_name='部门'),
        ),
    ]
