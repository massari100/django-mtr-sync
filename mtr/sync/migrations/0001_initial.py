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
            name='Context',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('cell', models.CharField(verbose_name='mtr.sync:cell', blank=True, max_length=1000)),
                ('value', models.CharField(verbose_name='mtr.sync:value', blank=True, max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:contexts',
                'verbose_name': 'mtr.sync:context',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('update_value', models.CharField(verbose_name='mtr.sync:value', blank=True, max_length=255)),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('find_filter', models.CharField(verbose_name='mtr.sync:filter type', blank=True, max_length=255, choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte')])),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:fields',
                'verbose_name': 'mtr.sync:field',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(default=10, verbose_name='mtr.sync:step', choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', blank=True, max_length=60000, null=True)),
                ('type', models.PositiveSmallIntegerField(default=0, verbose_name='mtr.sync:type', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')])),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:messages',
                'verbose_name': 'mtr.sync:message',
                'ordering': ('position',),
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='mtr.sync:status', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', blank=True, null=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:reports',
                'verbose_name': 'mtr.sync:report',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:sequences',
                'verbose_name': 'mtr.sync:sequence',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=100)),
                ('start_col', models.CharField(verbose_name='mtr.sync:start column', blank=True, max_length=10)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', blank=True, null=True)),
                ('end_col', models.CharField(verbose_name='mtr.sync:end column', blank=True, max_length=10)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', blank=True, null=True)),
                ('model', models.CharField(verbose_name='mtr.sync:model', blank=True, max_length=255, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Sequence'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.context', 'Mtr_Sync | Context'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.message', 'Mtr_Sync | Message')])),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(default='XlsxProcessor', verbose_name='mtr.sync:format', max_length=255, choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header')),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('dataset', models.CharField(verbose_name='mtr.sync:dataset', blank=True, max_length=255, choices=[('some_dataset', 'some description')])),
                ('data_action', models.CharField(verbose_name='mtr.sync:data action', blank=True, max_length=255, choices=[('create', 'mtr.sync:Create only'), ('update', 'mtr.sync:Update only'), ('update_or_create', 'mtr.sync:Update or create')])),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset')),
                ('filter_querystring', models.CharField(verbose_name='mtr.sync:querystring', blank=True, max_length=255)),
                ('language', models.CharField(verbose_name='mtr.sync:language', blank=True, max_length=255, choices=[('de', 'German'), ('en', 'English')])),
                ('hide_translation_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Hide translation prefixed fields')),
                ('create_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Create settings for fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='mtr.sync:Populate settings from file')),
                ('run_after_save', models.BooleanField(default=False, verbose_name='mtr.sync:Start action after saving')),
                ('include_related', models.BooleanField(default=True, verbose_name='mtr.sync:Include related fields')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:settings',
                'verbose_name': 'mtr.sync:settings',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='sequence',
            name='settings',
            field=models.ManyToManyField(to='mtr_sync.Settings', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', blank=True, to='mtr_sync.Settings', related_name='reports', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', blank=True, to='mtr_sync.Settings', related_name='contexts', null=True),
        ),
    ]
