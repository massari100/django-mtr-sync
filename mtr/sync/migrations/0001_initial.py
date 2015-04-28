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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='step', default=10, choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')])),
                ('input_position', models.CharField(verbose_name='input position', max_length=10, blank=True)),
                ('input_value', models.TextField(null=True, verbose_name='input value', max_length=60000, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('name', models.CharField(verbose_name='name', max_length=255, blank=True)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
                ('converters', models.CharField(verbose_name='converters', max_length=255)),
            ],
            options={
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('filter_type', models.CharField(verbose_name='filter type', max_length=255)),
                ('value', models.CharField(verbose_name='value', max_length=255)),
            ],
            options={
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('buffer_file', models.FileField(verbose_name='file', upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, blank=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', default=1, choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(verbose_name='started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True, verbose_name='completed at', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', choices=[(0, 'Export'), (1, 'Import')], db_index=True)),
                ('name', models.CharField(verbose_name='name', max_length=100, blank=True)),
                ('start_col', models.CharField(verbose_name='start column', max_length=10, blank=True)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='start row', blank=True)),
                ('end_col', models.CharField(verbose_name='end column', max_length=10, blank=True)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='end row', blank=True)),
                ('model', models.CharField(verbose_name='main model', max_length=255, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.filter', 'Mtr_Sync | Filter'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.error', 'Mtr_Sync | Error'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person')], blank=True)),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='format', max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='worksheet page', max_length=255, blank=True)),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(verbose_name='custom filename', max_length=255, blank=True)),
                ('buffer_file', models.FileField(verbose_name='file', upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, blank=True)),
                ('dataset', models.CharField(verbose_name='dataset', max_length=255, choices=[('some_dataset', 'some description')], blank=True)),
                ('filter_dataset', models.BooleanField(verbose_name='filter custom dataset', default=True)),
                ('data_action', models.CharField(verbose_name='data action', max_length=255, choices=[('create', 'Create instances without filter')], blank=True)),
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
            field=models.ForeignKey(null=True, to='mtr_sync.Settings', blank=True, verbose_name='settings', related_name='reports'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filter',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', verbose_name='settings', related_name='filters'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', verbose_name='settings', related_name='fields'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
            preserve_default=True,
        ),
    ]
