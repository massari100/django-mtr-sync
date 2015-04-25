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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='position', blank=True, null=True)),
                ('message', models.TextField(verbose_name='message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='step', default=10, choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')])),
                ('input_position', models.CharField(verbose_name='input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='input value', blank=True, null=True, max_length=60000)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='position', blank=True, null=True)),
                ('name', models.CharField(verbose_name='name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='skip', default=False)),
                ('converters', models.CharField(verbose_name='converters', max_length=255)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', db_index=True, choices=[(0, 'Export'), (1, 'Import')])),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', blank=True, db_index=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', default=1, choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(verbose_name='action', db_index=True, choices=[(0, 'Export'), (1, 'Import')])),
                ('name', models.CharField(verbose_name='name', blank=True, max_length=100)),
                ('start_col', models.CharField(verbose_name='start column', blank=True, max_length=10)),
                ('start_row', models.PositiveIntegerField(verbose_name='start row', blank=True, null=True)),
                ('end_col', models.CharField(verbose_name='end column', blank=True, max_length=10)),
                ('end_row', models.PositiveIntegerField(verbose_name='end row', blank=True, null=True)),
                ('model', models.CharField(verbose_name='main model', blank=True, max_length=255, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('mtrsync.settings', 'Mtrsync | Settings'), ('mtrsync.field', 'Mtrsync | Field'), ('mtrsync.report', 'Mtrsync | Report'), ('mtrsync.error', 'Mtrsync | Error'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person')])),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='format', max_length=255, choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(verbose_name='include header', default=True)),
                ('filename', models.CharField(verbose_name='custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', blank=True, db_index=True)),
                ('dataset', models.CharField(verbose_name='dataset', blank=True, max_length=255, choices=[('some_dataset', 'some description')])),
                ('data_action', models.CharField(verbose_name='data action', blank=True, max_length=255, choices=[('create', 'Create instances without filter')])),
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
            field=models.ForeignKey(verbose_name='settings', to='mtrsync.Settings', related_name='reports', blank=True, null=True),
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
            field=models.ForeignKey(related_name='errors', to='mtrsync.Report'),
            preserve_default=True,
        ),
    ]
