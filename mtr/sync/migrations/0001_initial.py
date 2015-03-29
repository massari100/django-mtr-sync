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
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('message', models.TextField(verbose_name='message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(default=10, choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')], verbose_name='step')),
                ('input_position', models.CharField(blank=True, verbose_name='mtr.sync:input position', max_length=10)),
                ('input_value', models.TextField(null=True, blank=True, verbose_name='mtr.sync:input value', max_length=60000)),
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
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('name', models.CharField(blank=True, verbose_name='name', max_length=255)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, blank=True, verbose_name='file')),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], verbose_name='status')),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True, blank=True, verbose_name='completed at')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('start_col', models.CharField(blank=True, verbose_name='start column', max_length=10)),
                ('start_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='start row')),
                ('end_col', models.CharField(blank=True, verbose_name='end column', max_length=10)),
                ('end_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='end row')),
                ('main_model', models.CharField(choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.ValueProcessor', 'Mtrsync | Value Processor'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.ValueProcessorParams', 'Mtrsync | Value Processor'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')], verbose_name='main model', max_length=255)),
                ('main_model_id', models.PositiveIntegerField(null=True, blank=True, verbose_name='main model object')),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='format', max_length=255)),
                ('worksheet', models.CharField(blank=True, verbose_name='worksheet page', max_length=255)),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(blank=True, verbose_name='custom filename', max_length=255)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, blank=True, verbose_name='file')),
                ('queryset', models.CharField(blank=True, verbose_name='queryset', max_length=255)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('label', models.CharField(verbose_name='label', max_length=255)),
                ('description', models.TextField(null=True, blank=True, verbose_name='description', max_length=20000)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'value processor',
                'verbose_name_plural': 'value processors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessorParams',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('field_related', models.ForeignKey(to='mtrsync.Field', related_name='processor_params')),
                ('processor_related', models.ForeignKey(to='mtrsync.ValueProcessor', verbose_name='filter')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'value processor',
                'verbose_name_plural': 'value processors',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, verbose_name='settings', to='mtrsync.Settings', null=True, related_name='reports'),
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
