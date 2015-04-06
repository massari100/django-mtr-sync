# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.api.exceptions
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:position')),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], verbose_name='mtr.sync:step', default=10)),
                ('input_position', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:input position')),
                ('input_value', models.TextField(null=True, blank=True, max_length=60000, verbose_name='mtr.sync:input value')),
            ],
            options={
                'verbose_name': 'mtr.sync:error',
                'verbose_name_plural': 'mtr.sync:errors',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:position')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:name')),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('converters', models.CharField(max_length=255, verbose_name='mtr.sync:converters')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], verbose_name='mtr.sync:action', db_index=True)),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', db_index=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], verbose_name='mtr.sync:status', default=1)),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:started at')),
                ('completed_at', models.DateTimeField(null=True, blank=True, verbose_name='mtr.sync:completed at')),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:report',
                'verbose_name_plural': 'mtr.sync:reports',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], verbose_name='mtr.sync:action', db_index=True)),
                ('name', models.CharField(max_length=100, verbose_name='mtr.sync:name')),
                ('start_col', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:start column')),
                ('start_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:start row')),
                ('end_col', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:end column')),
                ('end_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:end row')),
                ('main_model', models.CharField(max_length=255, choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')], verbose_name='mtr.sync:main model')),
                ('main_model_id', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:main model object')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='mtr.sync:format')),
                ('worksheet', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:worksheet page')),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:custom filename')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', db_index=True)),
                ('queryset', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:queryset')),
                ('data_action', models.CharField(max_length=255, verbose_name='mtr.sync:action')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:settings',
                'verbose_name_plural': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, to='mtrsync.Settings', null=True, related_name='reports', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', to='mtrsync.Settings', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtrsync.Report'),
        ),
    ]
