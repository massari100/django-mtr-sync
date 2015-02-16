# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(null=True, verbose_name='order', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(max_length=20000, null=True, verbose_name='description', blank=True)),
                ('template', models.TextField(max_length=50000, verbose_name='template')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(null=True, verbose_name='order', blank=True)),
                ('field_related', models.ForeignKey(related_name='filter_params', to='mtr/sync.Field')),
                ('filter_related', models.ForeignKey(verbose_name='filter', to='mtr/sync.Filter')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(max_length=10, verbose_name='start column', blank=True)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='start row', blank=True)),
                ('end_col', models.CharField(max_length=10, verbose_name='mtr.sync:end column', blank=True)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='end row', blank=True)),
                ('main_model', models.CharField(max_length=255, verbose_name='main model', choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtr/Sync | Settings'), ('mtr.sync.models.Filter', 'Mtr/Sync | Filter'), ('mtr.sync.models.Field', 'Mtr/Sync | Field'), ('mtr.sync.models.FilterParams', 'Mtr/Sync | Filter'), ('mtr.sync.models.Report', 'Mtr/Sync | Report'), ('app.models.Person', 'App | Person')])),
                ('main_model_id', models.PositiveIntegerField(null=True, verbose_name='main model object', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, verbose_name='format', choices=[(b'XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), (b'XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML')])),
                ('worksheet', models.CharField(max_length=255, verbose_name='worksheet page', blank=True)),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(max_length=255, verbose_name='custom filename', blank=True)),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', blank=True)),
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
            field=models.ForeignKey(related_name='reports', verbose_name='used settings', blank=True, to='mtr/sync.Settings', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='filters',
            field=models.ManyToManyField(to='mtr/sync.Filter', through='mtr/sync.FilterParams'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', verbose_name='settings', to='mtr/sync.Settings'),
            preserve_default=True,
        ),
    ]
