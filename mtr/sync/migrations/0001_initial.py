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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', default=10, choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', blank=True, max_length=60000, null=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:error',
                'ordering': ('position',),
                'verbose_name_plural': 'mtr.sync:errors',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'ordering': ('position',),
                'verbose_name_plural': 'mtr.sync:fields',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', blank=True, null=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:report',
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:reports',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], db_index=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=100)),
                ('start_col', models.CharField(verbose_name='mtr.sync:start column', blank=True, max_length=10)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', blank=True, null=True)),
                ('end_col', models.CharField(verbose_name='mtr.sync:end column', blank=True, max_length=10)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', blank=True, null=True)),
                ('model', models.CharField(verbose_name='mtr.sync:model', blank=True, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.error', 'Mtr_Sync | Error')], max_length=255)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='mtr.sync:format', choices=[('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], max_length=255)),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header')),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('dataset', models.CharField(verbose_name='mtr.sync:dataset', blank=True, choices=[('some_dataset', 'some description')], max_length=255)),
                ('data_action', models.CharField(verbose_name='mtr.sync:data action', blank=True, choices=[('create', 'mtr.sync:Create instances without filter')], max_length=255)),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset')),
                ('filter_querystring', models.CharField(verbose_name='mtr.sync:querystring', blank=True, max_length=255)),
                ('language', models.CharField(verbose_name='mtr.sync:language', blank=True, choices=[('de', 'German'), ('en', 'English')], max_length=255)),
                ('language_attributes', models.BooleanField(default=True, verbose_name='mtr.sync:Hide translation prefixed fields')),
                ('create_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Create settings for fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='mtr.sync:Populate settings from file')),
            ],
            options={
                'verbose_name': 'mtr.sync:settings',
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, null=True, verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='reports'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='errors'),
        ),
    ]
