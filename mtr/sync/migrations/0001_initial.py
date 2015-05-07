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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(default=10, verbose_name='step', choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')])),
                ('input_position', models.CharField(max_length=10, verbose_name='input position', blank=True)),
                ('input_value', models.TextField(max_length=60000, null=True, verbose_name='input value', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', blank=True)),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('find_filter', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:filter type', choices=[(b'icontains', b'icontains'), (b'contains', b'contains'), (b'iexact', b'iexact'), (b'exact', b'exact'), (b'in', b'in'), (b'gt', b'gt'), (b'gte', b'gte'), (b'lt', b'lt'), (b'lte', b'lte')])),
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
                ('name', models.CharField(max_length=100, verbose_name='name', blank=True)),
                ('start_col', models.CharField(max_length=10, verbose_name='start column', blank=True)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='start row', blank=True)),
                ('end_col', models.CharField(max_length=10, verbose_name='end column', blank=True)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='end row', blank=True)),
                ('model', models.CharField(blank=True, max_length=255, verbose_name='model', choices=[(b'', b'---------'), (b'admin.logentry', b'Admin | Log Entry'), (b'auth.permission', b'Auth | Permission'), (b'auth.group', b'Auth | Group'), (b'auth.user', b'Auth | User'), (b'contenttypes.contenttype', b'Contenttypes | Content Type'), (b'sessions.session', b'Sessions | Session'), (b'app.office', b'App | Office'), (b'app.tag', b'App | Tag'), (b'app.person', b'App | Person'), (b'mtr_sync.settings', b'Mtr_Sync | Settings'), (b'mtr_sync.field', b'Mtr_Sync | Field'), (b'mtr_sync.report', b'Mtr_Sync | Report'), (b'mtr_sync.error', b'Mtr_Sync | Error')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, verbose_name='format', choices=[(b'XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), (b'XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), (b'OdsProcessor', '.ods | ODF Spreadsheet'), (b'CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(max_length=255, verbose_name='worksheet page', blank=True)),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(max_length=255, verbose_name='custom filename', blank=True)),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', blank=True)),
                ('dataset', models.CharField(blank=True, max_length=255, verbose_name='dataset', choices=[(b'some_dataset', b'some description')])),
                ('data_action', models.CharField(blank=True, max_length=255, verbose_name='data action', choices=[(b'create', 'Create instances without filter')])),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='filter custom dataset')),
                ('filter_querystring', models.CharField(max_length=255, verbose_name='querystring', blank=True)),
                ('language', models.CharField(blank=True, max_length=255, verbose_name='language', choices=[(b'de', b'German'), (b'en', b'English')])),
                ('language_attributes', models.BooleanField(default=True, verbose_name='Hide translation prefixed fields')),
                ('create_fields', models.BooleanField(default=True, verbose_name='Create settings for fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='Populate settings from file')),
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
            field=models.ForeignKey(related_name=b'reports', verbose_name='settings', blank=True, to='mtr_sync.Settings', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name=b'fields', verbose_name='settings', to='mtr_sync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name=b'errors', to='mtr_sync.Report'),
            preserve_default=True,
        ),
    ]
