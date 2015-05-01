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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')], verbose_name='step', default=10)),
                ('input_position', models.CharField(verbose_name='input position', blank=True, max_length=10)),
                ('input_value', models.TextField(null=True, verbose_name='input value', blank=True, max_length=60000)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'error',
                'verbose_name_plural': 'errors',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('name', models.CharField(verbose_name='name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
                ('converters', models.CharField(verbose_name='converters', max_length=255)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('filter_type', models.CharField(verbose_name='filter type', max_length=255)),
                ('value', models.CharField(verbose_name='value', max_length=255)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], verbose_name='action', db_index=True)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file', blank=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], verbose_name='status', default=1)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], verbose_name='action', db_index=True)),
                ('name', models.CharField(verbose_name='name', blank=True, max_length=100)),
                ('start_col', models.CharField(verbose_name='start column', blank=True, max_length=10)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='start row', blank=True)),
                ('end_col', models.CharField(verbose_name='end column', blank=True, max_length=10)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='end row', blank=True)),
                ('model', models.CharField(choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.filter', 'Mtr_Sync | Filter'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.error', 'Mtr_Sync | Error')], verbose_name='main model', blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='format', max_length=255)),
                ('worksheet', models.CharField(verbose_name='worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(verbose_name='custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='file', blank=True)),
                ('dataset', models.CharField(choices=[('some_dataset', 'some description')], verbose_name='dataset', blank=True, max_length=255)),
                ('filter_dataset', models.BooleanField(verbose_name='filter custom dataset', default=True)),
                ('data_action', models.CharField(choices=[('create', 'Create instances without filter')], verbose_name='data action', blank=True, max_length=255)),
                ('language', models.CharField(choices=[('de', 'German'), ('en', 'English')], verbose_name='mtr.sync:language', blank=True, max_length=255)),
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
            field=models.ForeignKey(related_name='reports', verbose_name='settings', to='mtr_sync.Settings', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filter',
            name='settings',
            field=models.ForeignKey(related_name='filters', verbose_name='settings', to='mtr_sync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', verbose_name='settings', to='mtr_sync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
            preserve_default=True,
        ),
    ]
