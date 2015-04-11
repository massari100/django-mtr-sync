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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:position', blank=True)),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], default=10)),
                ('input_position', models.CharField(max_length=10, verbose_name='mtr.sync:input position', blank=True)),
                ('input_value', models.TextField(max_length=60000, verbose_name='mtr.sync:input value', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:errors',
                'verbose_name': 'mtr.sync:error',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:position', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name', blank=True)),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('converters', models.CharField(max_length=255, verbose_name='mtr.sync:converters')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:fields',
                'verbose_name': 'mtr.sync:field',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', db_index=True, blank=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], default=1)),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True, verbose_name='mtr.sync:completed at', blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:reports',
                'verbose_name': 'mtr.sync:report',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('name', models.CharField(max_length=100, verbose_name='mtr.sync:name')),
                ('start_col', models.CharField(max_length=10, verbose_name='mtr.sync:start column', blank=True)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:start row', blank=True)),
                ('end_col', models.CharField(max_length=10, verbose_name='mtr.sync:end column', blank=True)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:end row', blank=True)),
                ('main_model', models.CharField(max_length=255, verbose_name='mtr.sync:main model', choices=[('', 'mtr.sync:No model used'), ('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')], blank=True)),
                ('main_model_id', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:main model object', blank=True)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
                ('processor', models.CharField(max_length=255, verbose_name='mtr.sync:format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(max_length=255, verbose_name='mtr.sync:worksheet page', blank=True)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(max_length=255, verbose_name='mtr.sync:custom filename', blank=True)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', db_index=True, blank=True)),
                ('queryset', models.CharField(max_length=255, verbose_name='mtr.sync:queryset', blank=True)),
                ('data_action', models.CharField(max_length=255, verbose_name='mtr.sync:action', choices=[('create', 'create')], blank=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:settings',
                'verbose_name': 'mtr.sync:settings',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', related_name='reports', null=True, blank=True, to='mtrsync.Settings'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', related_name='fields', to='mtrsync.Settings'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(to='mtrsync.Report', related_name='errors'),
        ),
    ]
