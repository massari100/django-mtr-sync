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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('position', models.PositiveIntegerField(verbose_name='position', blank=True, null=True)),
                ('message', models.TextField(verbose_name='message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='step', choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')], default=10)),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', max_length=10, blank=True)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', max_length=60000, blank=True, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('position', models.PositiveIntegerField(verbose_name='position', blank=True, null=True)),
                ('name', models.CharField(verbose_name='name', max_length=255, blank=True)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('buffer_file', models.FileField(verbose_name='file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], default=1)),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='completed at', blank=True, null=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('start_col', models.CharField(verbose_name='start column', max_length=10, blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='start row', blank=True, null=True)),
                ('end_col', models.CharField(verbose_name='end column', max_length=10, blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='end row', blank=True, null=True)),
                ('main_model', models.CharField(verbose_name='main model', choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.ValueProcessor', 'Mtrsync | Value Processor'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.ValueProcessorParams', 'Mtrsync | Value Processor'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')], max_length=255)),
                ('main_model_id', models.PositiveIntegerField(verbose_name='main model object', blank=True, null=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], max_length=255)),
                ('worksheet', models.CharField(verbose_name='worksheet page', max_length=255, blank=True)),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(verbose_name='custom filename', max_length=255, blank=True)),
                ('buffer_file', models.FileField(verbose_name='file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('queryset', models.CharField(verbose_name='queryset', max_length=255, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('label', models.CharField(verbose_name='label', max_length=255)),
                ('description', models.TextField(verbose_name='description', max_length=20000, blank=True, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('position', models.PositiveIntegerField(verbose_name='position', blank=True, null=True)),
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
            field=models.ForeignKey(verbose_name='settings', to='mtrsync.Settings', related_name='reports', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='processors',
            field=models.ManyToManyField(through='mtrsync.ValueProcessorParams', to='mtrsync.ValueProcessor'),
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
