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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('message', models.TextField(max_length=10000, verbose_name='message')),
                ('step', models.PositiveSmallIntegerField(default=10, choices=[(0, 'prepare queryset'), (1, 'prepare data'), (2, 'setup dimensions for file'), (3, 'open file'), (4, 'create file'), (5, 'write header'), (6, 'write data'), (7, 'save file'), (8, 'read file'), (9, 'import data'), (10, 'unexpected error')], verbose_name='step')),
                ('input_position', models.CharField(blank=True, max_length=10, verbose_name='input position')),
                ('input_value', models.TextField(null=True, blank=True, max_length=60000, verbose_name='input value')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='position')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('attribute', models.CharField(max_length=255, verbose_name='model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('find_filter', models.CharField(choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte')], blank=True, max_length=255, verbose_name='mtr.sync:filter type')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, db_index=True, verbose_name='file')),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')], verbose_name='status')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(null=True, blank=True, verbose_name='completed at')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'Export'), (1, 'Import')], db_index=True, verbose_name='action')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name')),
                ('start_col', models.CharField(blank=True, max_length=10, verbose_name='start column')),
                ('start_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='start row')),
                ('end_col', models.CharField(blank=True, max_length=10, verbose_name='end column')),
                ('end_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='end row')),
                ('model', models.CharField(choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.error', 'Mtr_Sync | Error')], blank=True, max_length=255, verbose_name='model')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(default='XlsxProcessor', choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], max_length=255, verbose_name='format')),
                ('worksheet', models.CharField(blank=True, max_length=255, verbose_name='worksheet page')),
                ('include_header', models.BooleanField(default=True, verbose_name='include header')),
                ('filename', models.CharField(blank=True, max_length=255, verbose_name='custom filename')),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, db_index=True, verbose_name='file')),
                ('dataset', models.CharField(choices=[('some_dataset', 'some description')], blank=True, max_length=255, verbose_name='dataset')),
                ('data_action', models.CharField(choices=[('create', 'Create instances without filter')], blank=True, max_length=255, verbose_name='data action')),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='filter custom dataset')),
                ('filter_querystring', models.CharField(blank=True, max_length=255, verbose_name='querystring')),
                ('language', models.CharField(choices=[('de', 'German'), ('en', 'English')], blank=True, max_length=255, verbose_name='language')),
                ('hide_translation_fields', models.BooleanField(default=True, verbose_name='Hide translation prefixed fields')),
                ('create_fields', models.BooleanField(default=True, verbose_name='Create settings for fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='Populate settings from file')),
                ('start_after_save', models.BooleanField(default=False, verbose_name='mtr.sync:Start action after saving')),
                ('include_related', models.BooleanField(default=True, verbose_name='mtr.sync:Include related fields')),
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
            field=models.ForeignKey(null=True, blank=True, to='mtr_sync.Settings', verbose_name='settings', related_name='reports'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='settings', related_name='fields', to='mtr_sync.Settings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
            preserve_default=True,
        ),
    ]
