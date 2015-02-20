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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(verbose_name='order', null=True, blank=True)),
                ('name', models.CharField(verbose_name='name', max_length=255, blank=True)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
            ],
            options={
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('description', models.TextField(verbose_name='description', null=True, blank=True, max_length=20000)),
                ('template', models.TextField(verbose_name='template', max_length=50000)),
            ],
            options={
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(verbose_name='order', null=True, blank=True)),
                ('field_related', models.ForeignKey(related_name='filter_params', to='mtr/sync.Field')),
                ('filter_related', models.ForeignKey(verbose_name='filter', to='mtr/sync.Filter')),
            ],
            options={
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('buffer_file', models.FileField(verbose_name='file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], default=1)),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='completed at', null=True, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('start_col', models.CharField(verbose_name='start column', max_length=10, blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='start row', null=True, blank=True)),
                ('end_col', models.CharField(verbose_name='end column', max_length=10, blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='end row', null=True, blank=True)),
                ('main_model', models.CharField(verbose_name='main model', choices=[('django.contrib.admin.models.LogEntry', 'Admin | Log Entry'), ('django.contrib.auth.models.Permission', 'Auth | Permission'), ('django.contrib.auth.models.Group', 'Auth | Group'), ('django.contrib.auth.models.User', 'Auth | User'), ('django.contrib.contenttypes.models.ContentType', 'Contenttypes | Content Type'), ('django.contrib.sessions.models.Session', 'Sessions | Session'), ('mtr.sync.models.Settings', 'Mtr/Sync | Settings'), ('mtr.sync.models.Filter', 'Mtr/Sync | Filter'), ('mtr.sync.models.Field', 'Mtr/Sync | Field'), ('mtr.sync.models.FilterParams', 'Mtr/Sync | Filter'), ('mtr.sync.models.Report', 'Mtr/Sync | Report'), ('app.models.Person', 'App | Person')], max_length=255)),
                ('main_model_id', models.PositiveIntegerField(verbose_name='main model object', null=True, blank=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML')], max_length=255)),
                ('worksheet', models.CharField(verbose_name='worksheet page', max_length=255, blank=True)),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(verbose_name='custom filename', max_length=255, blank=True)),
                ('buffer_file', models.FileField(verbose_name='file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
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
            field=models.ForeignKey(null=True, blank=True, to='mtr/sync.Settings', verbose_name='used settings', related_name='reports'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='filters',
            field=models.ManyToManyField(through='mtr/sync.FilterParams', to='mtr/sync.Filter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', to='mtr/sync.Settings', verbose_name='settings'),
            preserve_default=True,
        ),
    ]
