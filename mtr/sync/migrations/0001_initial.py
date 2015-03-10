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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('position', models.PositiveSmallIntegerField(verbose_name='position', null=True, blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='step', default=10, choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('position', models.PositiveIntegerField(verbose_name='position', null=True, blank=True)),
                ('name', models.CharField(verbose_name='name', max_length=255, blank=True)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
            ],
            options={
                'verbose_name': 'field',
                'ordering': ['position'],
                'verbose_name_plural': 'fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('buffer_file', models.FileField(db_index=True, verbose_name='file', upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', default=1, choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='completed at', null=True, blank=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
            ],
            options={
                'verbose_name': 'report',
                'ordering': ('-id',),
                'verbose_name_plural': 'reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('start_col', models.CharField(verbose_name='start column', max_length=10, blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='start row', null=True, blank=True)),
                ('end_col', models.CharField(verbose_name='end column', max_length=10, blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='end row', null=True, blank=True)),
                ('main_model', models.CharField(verbose_name='main model', max_length=255, choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.ValueProcessor', 'Mtrsync | Mtr.Sync:Value Processor'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.ValueProcessorParams', 'Mtrsync | Mtr.Sync:Value Processor'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Office', 'App | Office'), ('app.models.Tag', 'App | Tag'), ('app.models.Person', 'App | Person')])),
                ('main_model_id', models.PositiveIntegerField(verbose_name='main model object', null=True, blank=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='format', max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='worksheet page', max_length=255, blank=True)),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(verbose_name='custom filename', max_length=255, blank=True)),
                ('buffer_file', models.FileField(db_index=True, verbose_name='file', upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('queryset', models.CharField(verbose_name='mtr.sync:queryset', max_length=255, choices=[('', '')], blank=True)),
            ],
            options={
                'verbose_name': 'settings',
                'ordering': ('-id',),
                'verbose_name_plural': 'settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('label', models.CharField(verbose_name='mtr.sync:label', max_length=255)),
                ('description', models.TextField(verbose_name='description', null=True, max_length=20000, blank=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:value processor',
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:value processors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueProcessorParams',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('position', models.PositiveIntegerField(verbose_name='position', null=True, blank=True)),
                ('field_related', models.ForeignKey(related_name='processor_params', to='mtrsync.Field')),
                ('processor_related', models.ForeignKey(verbose_name='filter', to='mtrsync.ValueProcessor')),
            ],
            options={
                'verbose_name': 'mtr.sync:value processor',
                'ordering': ['position'],
                'verbose_name_plural': 'mtr.sync:value processors',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(null=True, to='mtrsync.Settings', blank=True, verbose_name='settings', related_name='reports'),
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
            field=models.ForeignKey(to='mtrsync.Settings', verbose_name='settings', related_name='fields'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtrsync.Report'),
            preserve_default=True,
        ),
    ]
