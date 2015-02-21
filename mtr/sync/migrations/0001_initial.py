# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(verbose_name='order', null=True, blank=True)),
                ('name', models.CharField(verbose_name='name', max_length=255, blank=True)),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
            ],
            options={
                'verbose_name_plural': 'fields',
                'ordering': ['order'],
                'verbose_name': 'field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', null=True, max_length=20000, blank=True)),
                ('template', models.TextField(max_length=50000, verbose_name='template')),
            ],
            options={
                'verbose_name_plural': 'filters',
                'ordering': ('-id',),
                'verbose_name': 'filter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterParams',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(verbose_name='order', null=True, blank=True)),
                ('field_related', models.ForeignKey(related_name='filter_params', to='mtr/sync.Field')),
                ('filter_related', models.ForeignKey(to='mtr/sync.Filter', verbose_name='filter')),
            ],
            options={
                'verbose_name_plural': 'filters',
                'ordering': ['order'],
                'verbose_name': 'filter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file', blank=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], default=1, verbose_name='status')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(verbose_name='completed at', null=True, blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name_plural': 'reports',
                'ordering': ('-id',),
                'verbose_name': 'report',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(verbose_name='start column', max_length=10, blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='start row', null=True, blank=True)),
                ('end_col', models.CharField(verbose_name='end column', max_length=10, blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='end row', null=True, blank=True)),
                ('main_model', models.CharField(choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtr/Sync | Settings'), ('mtr.sync.models.Filter', 'Mtr/Sync | Filter'), ('mtr.sync.models.Field', 'Mtr/Sync | Field'), ('mtr.sync.models.FilterParams', 'Mtr/Sync | Filter'), ('mtr.sync.models.Report', 'Mtr/Sync | Report'), ('app.models.Person', 'App | Person')], max_length=255, verbose_name='main model')),
                ('main_model_id', models.PositiveIntegerField(verbose_name='main model object', null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML')], max_length=255, verbose_name='format')),
                ('worksheet', models.CharField(verbose_name='worksheet page', max_length=255, blank=True)),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(verbose_name='custom filename', max_length=255, blank=True)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file', blank=True)),
            ],
            options={
                'verbose_name_plural': 'settings',
                'ordering': ('-id',),
                'verbose_name': 'settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(to='mtr/sync.Settings', verbose_name='used settings', related_name='reports', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='filters',
            field=models.ManyToManyField(through='mtr/sync.FilterParams', to='mtr/sync.Filter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(to='mtr/sync.Settings', verbose_name='settings', related_name='fields'),
            preserve_default=True,
        ),
    ]
