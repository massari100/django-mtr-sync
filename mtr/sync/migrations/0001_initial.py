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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:position')),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', default=10, choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(blank=True, verbose_name='mtr.sync:input position', max_length=10)),
                ('input_value', models.TextField(null=True, blank=True, verbose_name='mtr.sync:input value', max_length=60000)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:errors',
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:error',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('position', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:position')),
                ('name', models.CharField(blank=True, verbose_name='mtr.sync:name', max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:fields',
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:field',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, blank=True, verbose_name='mtr.sync:file')),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:started at')),
                ('completed_at', models.DateTimeField(null=True, blank=True, verbose_name='mtr.sync:completed at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:reports',
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:report',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('name', models.CharField(blank=True, verbose_name='mtr.sync:name', max_length=100)),
                ('start_col', models.CharField(blank=True, verbose_name='mtr.sync:start column', max_length=10)),
                ('start_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:start row')),
                ('end_col', models.CharField(blank=True, verbose_name='mtr.sync:end column', max_length=10)),
                ('end_row', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:end row')),
                ('model', models.CharField(blank=True, verbose_name='mtr.sync:model', max_length=255, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Mtr.Sync:Settings'), ('mtr_sync.field', 'Mtr_Sync | Mtr.Sync:Field'), ('mtr_sync.report', 'Mtr_Sync | Mtr.Sync:Report'), ('mtr_sync.error', 'Mtr_Sync | Mtr.Sync:Error')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
                ('processor', models.CharField(verbose_name='mtr.sync:format', max_length=255, choices=[('XlsProcessor', '.xls | mtr.sync:Microsoft Excel 97/2000/XP/2003'), ('XlsxProcessor', '.xlsx | mtr.sync:Microsoft Excel 2007/2010/2013 XML'), ('OdsProcessor', '.ods | mtr.sync:ODF Spreadsheet'), ('CsvProcessor', '.csv | mtr.sync:CSV')])),
                ('worksheet', models.CharField(blank=True, verbose_name='mtr.sync:worksheet page', max_length=255)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(blank=True, verbose_name='mtr.sync:custom filename', max_length=255)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, blank=True, verbose_name='mtr.sync:file')),
                ('dataset', models.CharField(blank=True, verbose_name='mtr.sync:dataset', max_length=255, choices=[('some_dataset', 'some description')])),
                ('data_action', models.CharField(blank=True, verbose_name='mtr.sync:data action', max_length=255, choices=[('create', 'mtr.sync:Create instances without filter')])),
                ('filter_dataset', models.BooleanField(verbose_name='mtr.sync:filter custom dataset', default=True)),
                ('filter_querystring', models.CharField(blank=True, verbose_name='mtr.sync:querystring', max_length=255)),
                ('language', models.CharField(blank=True, verbose_name='mtr.sync:language', max_length=255, choices=[('de', 'German'), ('en', 'English')])),
                ('language_attributes', models.BooleanField(verbose_name='mtr.sync:Hide translation prefixed fields', default=True)),
                ('create_fields', models.BooleanField(verbose_name='mtr.sync:Create settings for fields', default=True)),
                ('populate_from_file', models.BooleanField(verbose_name='mtr.sync:Populate settings from file', default=False)),
                ('related_field', models.CharField(blank=True, verbose_name='mtr.sync:related field', max_length=255)),
                ('related_id', models.PositiveIntegerField(null=True, blank=True, verbose_name='mtr.sync:related id')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:settings',
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(blank=True, related_name='reports', to='mtr_sync.Settings', null=True, verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', to='mtr_sync.Settings', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='error',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='errors'),
        ),
    ]
