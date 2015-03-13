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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='position')),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(default=10, choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')], verbose_name='step')),
                ('input_position', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:input position')),
                ('input_value', models.TextField(blank=True, max_length=60000, null=True, verbose_name='mtr.sync:input value')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='position')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
            ],
            options={
                'verbose_name_plural': 'fields',
                'ordering': ['position'],
                'verbose_name': 'field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file')),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], verbose_name='status')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='completed at')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(blank=True, max_length=10, verbose_name='start column')),
                ('start_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='start row')),
                ('end_col', models.CharField(blank=True, max_length=10, verbose_name='end column')),
                ('end_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='end row')),
                ('main_model', models.CharField(max_length=255, choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.ValueProcessor', 'Mtrsync | Value Processor'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.ValueProcessorParams', 'Mtrsync | Value Processor'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')], verbose_name='main model')),
                ('main_model_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='main model object')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='format')),
                ('worksheet', models.CharField(blank=True, max_length=255, verbose_name='worksheet page')),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='custom filename')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file')),
                ('queryset', models.CharField(blank=True, max_length=255, verbose_name='queryset')),
            ],
            options={
                'verbose_name_plural': 'settings',
                'ordering': ('-id',),
                'verbose_name': 'settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('label', models.CharField(max_length=255, verbose_name='label')),
                ('description', models.TextField(blank=True, max_length=20000, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name_plural': 'value processors',
                'ordering': ('-id',),
                'verbose_name': 'value processor',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessorParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='position')),
                ('field_related', models.ForeignKey(to='mtrsync.Field', related_name='processor_params')),
                ('processor_related', models.ForeignKey(to='mtrsync.ValueProcessor', verbose_name='filter')),
            ],
            options={
                'verbose_name_plural': 'value processors',
                'ordering': ['position'],
                'verbose_name': 'value processor',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, to='mtrsync.Settings', related_name='reports', null=True, verbose_name='settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='processors',
            field=models.ManyToManyField(to='mtrsync.ValueProcessor', through='mtrsync.ValueProcessorParams'),
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
            field=models.ForeignKey(to='mtrsync.Report', related_name='errors'),
            preserve_default=True,
        ),
    ]
