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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', default=10, choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', null=True, blank=True, max_length=60000)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', blank=True, null=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:report',
                'verbose_name_plural': 'mtr.sync:reports',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=100)),
                ('start_col', models.CharField(verbose_name='mtr.sync:start column', blank=True, max_length=10)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', blank=True, null=True)),
                ('end_col', models.CharField(verbose_name='mtr.sync:end column', blank=True, max_length=10)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', blank=True, null=True)),
                ('main_model', models.CharField(verbose_name='mtr.sync:main model', max_length=255, blank=True, choices=[('', 'mtr.sync:No model used'), ('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')])),
                ('main_model_id', models.PositiveIntegerField(verbose_name='mtr.sync:main model object', blank=True, null=True)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='mtr.sync:format', max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
                ('queryset', models.CharField(verbose_name='mtr.sync:queryset', blank=True, max_length=255)),
                ('data_action', models.CharField(verbose_name='mtr.sync:action', max_length=255, blank=True, choices=[('create', 'create')])),
            ],
            options={
                'verbose_name': 'mtr.sync:settings',
                'verbose_name_plural': 'mtr.sync:settings',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', blank=True, null=True, to='mtrsync.Settings', related_name='reports'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtrsync.Settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtrsync.Report'),
        ),
    ]
