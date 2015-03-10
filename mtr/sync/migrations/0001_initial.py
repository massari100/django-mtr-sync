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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='position', null=True, blank=True)),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(default=10, verbose_name='step', choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')])),
                ('input_position', models.CharField(max_length=10, verbose_name='mtr.sync:input position', blank=True)),
                ('input_value', models.TextField(max_length=60000, verbose_name='mtr.sync:input value', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'error',
                'verbose_name_plural': 'errors',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='position', null=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
            ],
            options={
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', db_index=True, blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='completed at', null=True, blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'report',
                'verbose_name_plural': 'reports',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(max_length=10, verbose_name='start column', blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='start row', null=True, blank=True)),
                ('end_col', models.CharField(max_length=10, verbose_name='end column', blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='end row', null=True, blank=True)),
                ('main_model', models.CharField(max_length=255, verbose_name='main model', choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.ValueProcessor', 'Mtrsync | Value Processor'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.ValueProcessorParams', 'Mtrsync | Value Processor'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')])),
                ('main_model_id', models.PositiveIntegerField(verbose_name='main model object', null=True, blank=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, verbose_name='format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(max_length=255, verbose_name='worksheet page', blank=True)),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(max_length=255, verbose_name='custom filename', blank=True)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', db_index=True, blank=True)),
                ('queryset', models.CharField(max_length=255, verbose_name='queryset', blank=True, choices=[('', '')])),
            ],
            options={
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('label', models.CharField(max_length=255, verbose_name='label')),
                ('description', models.TextField(max_length=20000, verbose_name='description', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'value processor',
                'verbose_name_plural': 'value processors',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessorParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='position', null=True, blank=True)),
                ('field_related', models.ForeignKey(related_name='processor_params', to='mtrsync.Field')),
                ('processor_related', models.ForeignKey(verbose_name='filter', to='mtrsync.ValueProcessor')),
            ],
            options={
                'verbose_name': 'value processor',
                'verbose_name_plural': 'value processors',
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(related_name='reports', verbose_name='settings', to='mtrsync.Settings', null=True, blank=True),
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
            field=models.ForeignKey(verbose_name='settings', to='mtrsync.Settings', related_name='fields'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtrsync.Report'),
            preserve_default=True,
        ),
    ]
