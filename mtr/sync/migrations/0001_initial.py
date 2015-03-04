# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings
import mtr.sync.api.exceptions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='position')),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], verbose_name='step', default=10)),
            ],
            options={
                'verbose_name_plural': 'errors',
                'verbose_name': 'error',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('name', models.CharField(max_length=255, blank=True, verbose_name='name')),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
            ],
            options={
                'verbose_name_plural': 'fields',
                'verbose_name': 'field',
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('label', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(null=True, max_length=20000, blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name_plural': 'filters',
                'verbose_name': 'filter',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterParams',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('field_related', models.ForeignKey(related_name='filter_params', to='mtrsync.Field')),
                ('filter_related', models.ForeignKey(to='mtrsync.Filter', verbose_name='filter')),
            ],
            options={
                'verbose_name_plural': 'filters',
                'verbose_name': 'filter',
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], verbose_name='action', db_index=True)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, verbose_name='file', db_index=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], verbose_name='status', default=1)),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(null=True, blank=True, verbose_name='completed at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name_plural': 'reports',
                'verbose_name': 'report',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], verbose_name='action', db_index=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(max_length=10, blank=True, verbose_name='start column')),
                ('start_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='start row')),
                ('end_col', models.CharField(max_length=10, blank=True, verbose_name='end column')),
                ('end_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='end row')),
                ('main_model', models.CharField(max_length=255, choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Filter', 'Mtrsync | Filter'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.FilterParams', 'Mtrsync | Filter'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')], verbose_name='main model')),
                ('main_model_id', models.PositiveIntegerField(null=True, blank=True, verbose_name='main model object')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='format')),
                ('worksheet', models.CharField(max_length=255, blank=True, verbose_name='worksheet page')),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(max_length=255, blank=True, verbose_name='custom filename')),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, verbose_name='file', db_index=True)),
                ('queryset', models.CharField(max_length=255, choices=[('', '')], verbose_name='mtr.sync:queryset', blank=True)),
            ],
            options={
                'verbose_name_plural': 'settings',
                'verbose_name': 'settings',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, null=True, related_name='reports', to='mtrsync.Settings', verbose_name='settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='filters',
            field=models.ManyToManyField(to='mtrsync.Filter', through='mtrsync.FilterParams'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', to='mtrsync.Settings', verbose_name='settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtrsync.Report'),
            preserve_default=True,
        ),
    ]
