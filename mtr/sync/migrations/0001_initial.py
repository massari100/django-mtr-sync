# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings
import mtr.sync.lib.exceptions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('cell', models.CharField(blank=True, max_length=1000, verbose_name='mtr.sync:cell')),
                ('value', models.CharField(blank=True, max_length=1000, verbose_name='mtr.sync:value')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:contexts',
                'verbose_name': 'mtr.sync:context',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='position')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:name')),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('set_filter', models.CharField(blank=True, max_length=255, choices=[('not', 'mtr.sync:Not create or update instance if empty cell')], verbose_name='mtr.sync:set filter type')),
                ('set_value', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:set value')),
                ('find_filter', models.CharField(blank=True, max_length=255, default='exact', choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte'), ('not', 'not')], verbose_name='mtr.sync:find filter type')),
                ('find_value', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:find value')),
                ('converters', models.CharField(blank=True, max_length=255, verbose_name='mtr.sync:converters')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:fields',
                'abstract': False,
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:field',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='position')),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(default=1, choices=[(0, 'mtr.sync:import data'), (1, 'mtr.sync:unexpected error')], verbose_name='mtr.sync:step')),
                ('input_position', models.CharField(blank=True, max_length=10, verbose_name='mtr.sync:input position')),
                ('input_value', models.TextField(blank=True, max_length=60000, null=True, verbose_name='mtr.sync:input value')),
                ('type', models.PositiveSmallIntegerField(default=0, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')], verbose_name='mtr.sync:type')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:messages',
                'abstract': False,
                'ordering': ('position',),
                'verbose_name': 'mtr.sync:message',
            },
            bases=(models.Model, mtr.sync.lib.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Replacer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(max_length=100000, verbose_name='mtr.sync:value')),
                ('change_to', models.TextField(max_length=100000, verbose_name='mtr.sync:change to')),
                ('regex', models.TextField(max_length=1000, verbose_name='mtr.sync:regex')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:replacers',
                'verbose_name': 'mtr.sync:replacer',
            },
        ),
        migrations.CreateModel(
            name='ReplacerCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('model', models.CharField(blank=True, max_length=255, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Mtr.Sync:Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Mtr.Sync:Sequence'), ('mtr_sync.replacercategory', 'Mtr_Sync | Mtr.Sync:Replacer Category'), ('mtr_sync.replacer', 'Mtr_Sync | Mtr.Sync:Replacer'), ('mtr_sync.field', 'Mtr_Sync | Mtr.Sync:Field'), ('mtr_sync.context', 'Mtr_Sync | Mtr.Sync:Context'), ('mtr_sync.report', 'Mtr_Sync | Mtr.Sync:Report'), ('mtr_sync.message', 'Mtr_Sync | Mtr.Sync:Message')], verbose_name='mtr.sync:model')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:replacer categories',
                'verbose_name': 'mtr.sync:replacer category',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action', db_index=True)),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', db_index=True)),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], verbose_name='mtr.sync:status')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:started at')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='mtr.sync:completed at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:reports',
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:report',
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('buffer_file', models.FileField(blank=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', db_index=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:sequences',
                'verbose_name': 'mtr.sync:sequence',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action', db_index=True)),
                ('name', models.CharField(blank=True, help_text='mtr.sync:Small description of operation', verbose_name='mtr.sync:name', max_length=100)),
                ('start_row', models.PositiveIntegerField(blank=True, help_text='mtr.sync:Reading or writing start index (including itself)', null=True, verbose_name='mtr.sync:start row')),
                ('end_row', models.PositiveIntegerField(blank=True, help_text='mtr.sync:Reading or writing end index (including itself)', null=True, verbose_name='mtr.sync:end row')),
                ('model', models.CharField(blank=True, help_text='mtr.sync:Choose database model if action need it', choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Mtr.Sync:Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Mtr.Sync:Sequence'), ('mtr_sync.replacercategory', 'Mtr_Sync | Mtr.Sync:Replacer Category'), ('mtr_sync.replacer', 'Mtr_Sync | Mtr.Sync:Replacer'), ('mtr_sync.field', 'Mtr_Sync | Mtr.Sync:Field'), ('mtr_sync.context', 'Mtr_Sync | Mtr.Sync:Context'), ('mtr_sync.report', 'Mtr_Sync | Mtr.Sync:Report'), ('mtr_sync.message', 'Mtr_Sync | Mtr.Sync:Message')], verbose_name='mtr.sync:model', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
                ('processor', models.CharField(help_text='mtr.sync:Choose file type', default='XlsxProcessor', choices=[('XlsxProcessor', '.xlsx | mtr.sync:Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | mtr.sync:Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | mtr.sync:ODF Spreadsheet'), ('CsvProcessor', '.csv | mtr.sync:CSV')], verbose_name='mtr.sync:format', max_length=255)),
                ('worksheet', models.CharField(blank=True, help_text='mtr.sync:Page name of sheet book', verbose_name='mtr.sync:worksheet page', max_length=255)),
                ('include_header', models.BooleanField(help_text='mtr.sync:Check it if you need to write field names in export or skip it in import', default=True, verbose_name='mtr.sync:include header')),
                ('filename', models.CharField(blank=True, help_text='mtr.sync:Custom filename for export', verbose_name='mtr.sync:custom filename', max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', blank=True, help_text='mtr.sync:File for import action', upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True)),
                ('dataset', models.CharField(blank=True, help_text='mtr.sync:Custom registered dataset if you import or export data from different source, for example network or ftp server', choices=[('some_dataset', 'some description')], verbose_name='mtr.sync:dataset', max_length=255)),
                ('data_action', models.CharField(blank=True, help_text='mtr.sync:What will be done with data, for example, create or some custom opeartion eg. download image from server', choices=[('create', 'mtr.sync:Create only'), ('create_or_update', 'mtr.sync:Create or update'), ('update', 'mtr.sync:Update only')], verbose_name='mtr.sync:data action', max_length=255)),
                ('filter_dataset', models.BooleanField(help_text='mtr.sync:Check it if you have custom queryset and want to filter from querystring, for example from admin button', default=True, verbose_name='mtr.sync:filter custom dataset')),
                ('filter_querystring', models.CharField(blank=True, help_text='mtr.sync:Querystring from admin or other source, if you choose import action this params will be used for updating!', verbose_name='mtr.sync:querystring', max_length=255)),
                ('language', models.CharField(blank=True, help_text='mtr.sync:Activates language before action, for example if you want you have modeltranslation app and you need to export or import only for choosed language', choices=[('de', 'German'), ('en', 'English')], verbose_name='mtr.sync:language', max_length=255)),
                ('hide_translation_fields', models.BooleanField(help_text="mtr.sync:If you don't want to create _lang field settings and dublicate in attribute list, handy if you using modeltranslation", default=True, verbose_name='mtr.sync:Hide translation prefixed fields')),
                ('create_fields', models.BooleanField(help_text='mtr.sync:Automaticaly creates all settings for model fields', default=True, verbose_name='mtr.sync:Create settings for fields')),
                ('populate_from_file', models.BooleanField(help_text='mtr.sync:Read start row, end row and first worksheet page from given file', default=False, verbose_name='mtr.sync:Populate settings from file')),
                ('include_related', models.BooleanField(help_text="mtr.sync:Include ForeignKey and ManyToManyField fields when using 'create fields' option", default=True, verbose_name='mtr.sync:Include related fields')),
                ('edit_attributes', models.BooleanField(help_text='mtr.sync:If you want to add custom attributes for custom action, by checking this option, you can edit attributes', default=False, verbose_name='mtr.sync:Edit field attributes')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:settings',
                'ordering': ('-id',),
                'verbose_name': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='sequence',
            name='settings',
            field=models.ManyToManyField(related_name='sequences', verbose_name='mtr.sync:settings', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', blank=True, to='mtr_sync.Settings', related_name='reports', null=True),
        ),
        migrations.AddField(
            model_name='replacer',
            name='category',
            field=models.ForeignKey(verbose_name='mtr.sync:category', blank=True, to='mtr_sync.ReplacerCategory', related_name='replacers', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='messages'),
        ),
        migrations.AddField(
            model_name='field',
            name='replacer_category',
            field=models.ForeignKey(verbose_name='mtr.sync:replacer category', blank=True, to='mtr_sync.ReplacerCategory', related_name='fields', null=True),
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
