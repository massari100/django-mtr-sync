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
                'verbose_name': 'mtr.sync:context',
                'verbose_name_plural': 'mtr.sync:contexts',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('update', models.BooleanField(verbose_name='mtr.sync:update', default=True)),
                ('update_value', models.CharField(verbose_name='mtr.sync:value', blank=True, max_length=255)),
                ('find', models.BooleanField(verbose_name='mtr.sync:find', default=False)),
                ('find_filter', models.CharField(choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte')], blank=True, verbose_name='mtr.sync:filter type', max_length=255)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', blank=True, max_length=255)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', blank=True, null=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:prepare queryset'), (1, 'mtr.sync:prepare data'), (2, 'mtr.sync:setup dimensions for file'), (3, 'mtr.sync:open file'), (4, 'mtr.sync:create file'), (5, 'mtr.sync:write header'), (6, 'mtr.sync:write data'), (7, 'mtr.sync:save file'), (8, 'mtr.sync:read file'), (9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')], verbose_name='mtr.sync:step', default=10)),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', blank=True, null=True, max_length=60000)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')], verbose_name='mtr.sync:type', default=0)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:message',
                'verbose_name_plural': 'mtr.sync:messages',
            },
            bases=(models.Model, mtr.sync.api.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Replacer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('value', models.TextField(verbose_name='mtr.sync:value', max_length=100000)),
                ('change_to', models.TextField(verbose_name='mtr.sync:change to', max_length=100000)),
                ('regex', models.TextField(verbose_name='mtr.sync:regex', max_length=1000)),
            ],
            options={
                'verbose_name': 'mtr.sync:replacer',
                'verbose_name_plural': 'mtr.sync:replacers',
            },
        ),
        migrations.CreateModel(
            name='ReplacerCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('model', models.CharField(choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Mtr.Sync:Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Mtr.Sync:Sequence'), ('mtr_sync.replacercategory', 'Mtr_Sync | Mtr.Sync:Replacer Category'), ('mtr_sync.replacer', 'Mtr_Sync | Mtr.Sync:Replacer'), ('mtr_sync.field', 'Mtr_Sync | Mtr.Sync:Field'), ('mtr_sync.context', 'Mtr_Sync | Mtr.Sync:Context'), ('mtr_sync.report', 'Mtr_Sync | Mtr.Sync:Report'), ('mtr_sync.message', 'Mtr_Sync | Mtr.Sync:Message')], blank=True, verbose_name='mtr.sync:model', max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:replacer category',
                'verbose_name_plural': 'mtr.sync:replacer categories',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action', db_index=True)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], verbose_name='mtr.sync:status', default=1)),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', blank=True, null=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:sequence',
                'verbose_name_plural': 'mtr.sync:sequences',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action', db_index=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=100)),
                ('start_col', models.CharField(verbose_name='mtr.sync:start column', blank=True, max_length=10)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', blank=True, null=True)),
                ('end_col', models.CharField(verbose_name='mtr.sync:end column', blank=True, max_length=10)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', blank=True, null=True)),
                ('model', models.CharField(choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Sequence'), ('mtr_sync.replacercategory', 'Mtr_Sync | Replacer Category'), ('mtr_sync.replacer', 'Mtr_Sync | Replacer'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.context', 'Mtr_Sync | Context'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.message', 'Mtr_Sync | Message')], blank=True, verbose_name='mtr.sync:model', max_length=255)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='mtr.sync:format', default='XlsxProcessor', max_length=255)),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
                ('dataset', models.CharField(choices=[('some_dataset', 'some description')], blank=True, verbose_name='mtr.sync:dataset', max_length=255)),
                ('data_action', models.CharField(choices=[('create', 'mtr.sync:Create only'), ('update', 'mtr.sync:Update only'), ('update_or_create', 'mtr.sync:Update or create')], blank=True, verbose_name='mtr.sync:data action', max_length=255)),
                ('filter_dataset', models.BooleanField(verbose_name='mtr.sync:filter custom dataset', default=True)),
                ('filter_querystring', models.CharField(verbose_name='mtr.sync:querystring', blank=True, max_length=255)),
                ('language', models.CharField(choices=[('de', 'German'), ('en', 'English')], blank=True, verbose_name='mtr.sync:language', max_length=255)),
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
            field=models.ManyToManyField(to='mtr_sync.Settings', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(related_name='reports', blank=True, to='mtr_sync.Settings', verbose_name='mtr.sync:settings', null=True),
        ),
        migrations.AddField(
            model_name='replacer',
            name='category',
            field=models.ForeignKey(related_name='replacers', blank=True, to='mtr_sync.ReplacerCategory', verbose_name='mtr.sync:category', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(related_name='errors', to='mtr_sync.Report'),
        ),
        migrations.AddField(
            model_name='field',
            name='replacer_category',
            field=models.ForeignKey(related_name='fields', blank=True, to='mtr_sync.ReplacerCategory', verbose_name='mtr.sync:replacer category', null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', to='mtr_sync.Settings', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(related_name='contexts', blank=True, to='mtr_sync.Settings', verbose_name='mtr.sync:settings', null=True),
        ),
    ]
