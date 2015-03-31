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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='position', null=True)),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(default=10, verbose_name='step', choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')])),
                ('input_position', models.CharField(max_length=10, blank=True, verbose_name='mtr.sync:input position')),
                ('input_value', models.TextField(max_length=60000, blank=True, verbose_name='mtr.sync:input value', null=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(blank=True, verbose_name='position', null=True)),
                ('name', models.CharField(max_length=255, blank=True, verbose_name='name')),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
                ('converters', models.CharField(max_length=255, verbose_name='mtr.sync:converters')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', db_index=True)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, verbose_name='completed at', null=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(max_length=10, blank=True, verbose_name='start column')),
                ('start_row', models.PositiveIntegerField(blank=True, verbose_name='start row', null=True)),
                ('end_col', models.CharField(max_length=10, blank=True, verbose_name='end column')),
                ('end_row', models.PositiveIntegerField(blank=True, verbose_name='end row', null=True)),
                ('main_model', models.CharField(max_length=255, verbose_name='main model', choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')])),
                ('main_model_id', models.PositiveIntegerField(blank=True, verbose_name='main model object', null=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, verbose_name='format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(max_length=255, blank=True, verbose_name='worksheet page')),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(max_length=255, blank=True, verbose_name='custom filename')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', db_index=True)),
                ('queryset', models.CharField(max_length=255, blank=True, verbose_name='queryset')),
            ],
            options={
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='settings', to='mtrsync.Settings', related_name='reports', blank=True, null=True),
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
