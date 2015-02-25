# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(default=0, verbose_name='mtr.sync:step', choices=[(0, 'mtr.sync:file format')])),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:errors',
                'verbose_name': 'mtr.sync:error',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('name', models.CharField(blank=True, verbose_name='name', max_length=255)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description', max_length=20000)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='mtr.sync:position')),
                ('field_related', models.ForeignKey(related_name='filter_params', to='mtrsync.Field')),
                ('filter_related', models.ForeignKey(verbose_name='filter', to='mtrsync.Filter')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('buffer_file', models.FileField(blank=True, verbose_name='file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='completed at')),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(blank=True, verbose_name='start column', max_length=10)),
                ('start_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='start row')),
                ('end_col', models.CharField(blank=True, verbose_name='end column', max_length=10)),
                ('end_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='end row')),
                ('main_model', models.CharField(max_length=255, verbose_name='main model', choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtrsync | Settings'), ('mtr.sync.models.Filter', 'Mtrsync | Filter'), ('mtr.sync.models.Field', 'Mtrsync | Field'), ('mtr.sync.models.FilterParams', 'Mtrsync | Filter'), ('mtr.sync.models.Report', 'Mtrsync | Report'), ('mtr.sync.models.Error', 'Mtrsync | Mtr.Sync:Error'), ('app.models.Person', 'App | Person')])),
                ('main_model_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='main model object')),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('processor', models.CharField(max_length=255, verbose_name='format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML')])),
                ('worksheet', models.CharField(blank=True, verbose_name='worksheet page', max_length=255)),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(blank=True, verbose_name='custom filename', max_length=255)),
                ('buffer_file', models.FileField(blank=True, verbose_name='file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('processing_method', models.PositiveSmallIntegerField(default=0, verbose_name='mtr.sync:processing method', choices=[(0, 'mtr.sync:bulk'), (1, 'mtr.sync:separate')])),
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
            field=models.ForeignKey(blank=True, null=True, verbose_name='settings', related_name='reports', to='mtrsync.Settings'),
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
            field=models.ForeignKey(verbose_name='settings', related_name='fields', to='mtrsync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(to='mtrsync.Report'),
            preserve_default=True,
        ),
    ]
