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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(default=10, verbose_name='step', choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')])),
                ('input_position', models.CharField(verbose_name='input position', blank=True, max_length=10)),
                ('input_value', models.TextField(null=True, verbose_name='input value', blank=True, max_length=60000)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('name', models.CharField(verbose_name='name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
                ('converters', models.CharField(verbose_name='converters', max_length=255)),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', db_index=True, choices=[(0, 'Export'), (1, 'Import')])),
                ('buffer_file', models.FileField(verbose_name='file', db_index=True, blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(null=True, verbose_name='completed at', blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'report',
                'verbose_name_plural': 'reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', db_index=True, choices=[(0, 'Export'), (1, 'Import')])),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('start_col', models.CharField(verbose_name='start column', blank=True, max_length=10)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='start row', blank=True)),
                ('end_col', models.CharField(verbose_name='end column', blank=True, max_length=10)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='end row', blank=True)),
                ('main_model', models.CharField(verbose_name='main model', choices=[('', 'No model used'), ('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')], blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(verbose_name='format', max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(verbose_name='custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(verbose_name='file', db_index=True, blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('dataset', models.CharField(verbose_name='dataset', choices=[('some_dataset', 'some_dataset')], blank=True, max_length=255)),
                ('data_action', models.CharField(verbose_name='data action', choices=[('create', 'create')], blank=True, max_length=255)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='settings', blank=True, related_name='reports', to='mtrsync.Settings', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='settings', related_name='fields', to='mtrsync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(to='mtrsync.Report', related_name='errors'),
            preserve_default=True,
        ),
    ]
