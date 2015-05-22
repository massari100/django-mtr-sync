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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='mtr.sync.name', max_length=255)),
                ('cell', models.CharField(verbose_name='mtr.sync:field', max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:context',
                'verbose_name_plural': 'mtr.sync:contexts',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, blank=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255, blank=True)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('update', models.BooleanField(verbose_name='mtr.sync:update', default=True)),
                ('update_value', models.CharField(verbose_name='mtr.sync:value', max_length=255, blank=True)),
                ('find', models.BooleanField(verbose_name='mtr.sync:find', default=False)),
                ('find_filter', models.CharField(verbose_name='mtr.sync:filter type', choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte')], max_length=255, blank=True)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', max_length=255, blank=True)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, blank=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], default=10)),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', max_length=10, blank=True)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', null=True, max_length=60000, blank=True)),
                ('type', models.PositiveSmallIntegerField(verbose_name='mtr.sync:type', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')], default=0)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:message',
                'verbose_name_plural': 'mtr.sync:messages',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], verbose_name='mtr.sync:action')),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, verbose_name='mtr.sync:file')),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], default=1)),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', null=True, blank=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:report',
                'verbose_name_plural': 'mtr.sync:reports',
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, verbose_name='mtr.sync:file')),
            ],
            options={
                'verbose_name': 'mtr.sync:sequence',
                'verbose_name_plural': 'mtr.sync:sequences',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')], verbose_name='mtr.sync:action')),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=100, blank=True)),
                ('start_col', models.CharField(verbose_name='mtr.sync:start column', max_length=10, blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', null=True, blank=True)),
                ('end_col', models.CharField(verbose_name='mtr.sync:end column', max_length=10, blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', null=True, blank=True)),
                ('model', models.CharField(verbose_name='mtr.sync:model', choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Mtr.Sync:Sequence'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.context', 'Mtr_Sync | Mtr.Sync:Context'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.message', 'Mtr_Sync | Message')], max_length=255, blank=True)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(verbose_name='mtr.sync:format', choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], max_length=255, default='XlsxProcessor')),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', max_length=255, blank=True)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', max_length=255, blank=True)),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, verbose_name='mtr.sync:file')),
                ('dataset', models.CharField(verbose_name='mtr.sync:dataset', choices=[('some_dataset', 'some description')], max_length=255, blank=True)),
                ('data_action', models.CharField(verbose_name='mtr.sync:data action', choices=[('create', 'mtr.sync:Create only'), ('update', 'mtr.sync:Update only'), ('update_or_create', 'mtr.sync:Update or create')], max_length=255, blank=True)),
                ('filter_dataset', models.BooleanField(verbose_name='mtr.sync:filter custom dataset', default=True)),
                ('filter_querystring', models.CharField(verbose_name='mtr.sync:querystring', max_length=255, blank=True)),
                ('language', models.CharField(verbose_name='mtr.sync:language', choices=[('de', 'German'), ('en', 'English')], max_length=255, blank=True)),
                ('hide_translation_fields', models.BooleanField(verbose_name='mtr.sync:Hide translation prefixed fields', default=True)),
                ('create_fields', models.BooleanField(verbose_name='mtr.sync:Create settings for fields', default=True)),
                ('populate_from_file', models.BooleanField(verbose_name='mtr.sync:Populate settings from file', default=False)),
                ('run_after_save', models.BooleanField(verbose_name='mtr.sync:Start action after saving', default=False)),
                ('include_related', models.BooleanField(verbose_name='mtr.sync:Include related fields', default=True)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:settings',
                'verbose_name_plural': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='sequence',
            name='settings',
            field=models.ManyToManyField(verbose_name='mtr.sync:settings', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(related_name='reports', verbose_name='mtr.sync:settings', null=True, blank=True, to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='errors'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', verbose_name='mtr.sync:settings', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(related_name='contexts', verbose_name='mtr.sync:settings', null=True, blank=True, to='mtr_sync.Settings'),
        ),
    ]
