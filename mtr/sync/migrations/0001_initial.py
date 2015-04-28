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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='position')),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')], verbose_name='step', default=10)),
                ('input_position', models.CharField(blank=True, max_length=10, verbose_name='input position')),
                ('input_value', models.TextField(blank=True, max_length=60000, null=True, verbose_name='input value')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='position')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
                ('converters', models.CharField(max_length=255, verbose_name='converters')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True, verbose_name='position')),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('filter_type', models.CharField(max_length=255, verbose_name='mtr.sync:filter type')),
                ('value', models.CharField(max_length=255, verbose_name='mtr.sync:value')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:filter',
                'verbose_name_plural': 'mtr.sync:filters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], verbose_name='action', db_index=True)),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], verbose_name='status', default=1)),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='completed at')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], verbose_name='action', db_index=True)),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name')),
                ('start_col', models.CharField(blank=True, max_length=10, verbose_name='start column')),
                ('start_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='start row')),
                ('end_col', models.CharField(blank=True, max_length=10, verbose_name='end column')),
                ('end_row', models.PositiveIntegerField(blank=True, null=True, verbose_name='end row')),
                ('model', models.CharField(blank=True, max_length=255, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('mtrsync.settings', 'Mtrsync | Settings'), ('mtrsync.field', 'Mtrsync | Field'), ('mtrsync.filter', 'Mtrsync | Mtr.Sync:Filter'), ('mtrsync.report', 'Mtrsync | Report'), ('mtrsync.error', 'Mtrsync | Error'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person')], verbose_name='main model')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='format')),
                ('worksheet', models.CharField(blank=True, max_length=255, verbose_name='worksheet page')),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='custom filename')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file')),
                ('dataset', models.CharField(blank=True, max_length=255, choices=[('some_dataset', 'some description')], verbose_name='dataset')),
                ('filter_dataset', models.BooleanField(verbose_name='mtr.sync:filter custom dataset', default=True)),
                ('data_action', models.CharField(blank=True, max_length=255, choices=[('create', 'Create instances without filter')], verbose_name='data action')),
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
            field=models.ForeignKey(blank=True, related_name='reports', to='mtrsync.Settings', verbose_name='settings', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filter',
            name='settings',
            field=models.ForeignKey(to='mtrsync.Settings', verbose_name='settings', related_name='filters'),
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
