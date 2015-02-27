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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='position')),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(default=10, verbose_name='step', choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('name', models.CharField(max_length=255, blank=True, verbose_name='name')),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
            ],
            options={
                'verbose_name_plural': 'fields',
                'verbose_name': 'field',
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(null=True, blank=True, verbose_name='description', max_length=20000)),
                ('template', models.TextField(max_length=50000, verbose_name='template')),
            ],
            options={
                'verbose_name_plural': 'filters',
                'verbose_name': 'filter',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('field_related', models.ForeignKey(related_name='filter_params', to='mtrsync.Field')),
                ('filter_related', models.ForeignKey(to='mtrsync.Filter', verbose_name='filter')),
            ],
            options={
                'verbose_name_plural': 'filters',
                'verbose_name': 'filter',
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('buffer_file', models.FileField(blank=True, db_index=True, verbose_name='file', upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(null=True, blank=True, verbose_name='completed at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name_plural': 'reports',
                'verbose_name': 'report',
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
                ('start_col', models.CharField(max_length=10, blank=True, verbose_name='start column')),
                ('start_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='start row')),
                ('end_col', models.CharField(max_length=10, blank=True, verbose_name='end column')),
                ('end_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='end row')),
                ('main_model', models.CharField(max_length=255, verbose_name='main model', choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Filter', 'Mtrsync | Filter'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.FilterParams', 'Mtrsync | Filter'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Error'), ('app.models.Person', 'App | Person')])),
                ('main_model_id', models.PositiveIntegerField(null=True, blank=True, verbose_name='main model object')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, verbose_name='format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML')])),
                ('worksheet', models.CharField(max_length=255, blank=True, verbose_name='worksheet page')),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(max_length=255, blank=True, verbose_name='custom filename')),
                ('buffer_file', models.FileField(blank=True, db_index=True, verbose_name='file', upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('queryset', models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:queryset', choices=[('', '')])),
            ],
            options={
                'verbose_name_plural': 'settings',
                'verbose_name': 'settings',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(null=True, related_name='reports', verbose_name='settings', blank=True, to='mtrsync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='filters',
            field=models.ManyToManyField(to='mtrsync.Filter', through='mtrsync.FilterParams'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', verbose_name='settings', to='mtrsync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtrsync.Report'),
            preserve_default=True,
        ),
    ]
