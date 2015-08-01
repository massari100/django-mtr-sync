# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.lib.exceptions
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, default=1, blank=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('update', models.BooleanField(verbose_name='mtr.sync:update', default=True)),
                ('find', models.BooleanField(verbose_name='mtr.sync:find', default=False)),
                ('set_filter', models.CharField(choices=[('not', 'mtr.sync:Not create or update instance if empty cell')], verbose_name='mtr.sync:set filter type', blank=True, max_length=255)),
                ('set_value', models.CharField(verbose_name='mtr.sync:set value', blank=True, max_length=255)),
                ('find_filter', models.CharField(choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte'), ('not', 'not')], verbose_name='mtr.sync:find filter type', default='exact', blank=True, max_length=255)),
                ('find_value', models.CharField(verbose_name='mtr.sync:find value', blank=True, max_length=255)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
                'abstract': False,
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.sync:position', null=True, default=1, blank=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', default=10, choices=[(9, 'mtr.sync:import data'), (10, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', null=True, blank=True, max_length=60000)),
                ('type', models.PositiveSmallIntegerField(verbose_name='mtr.sync:type', default=0, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')])),
            ],
            options={
                'verbose_name': 'mtr.sync:message',
                'verbose_name_plural': 'mtr.sync:messages',
                'abstract': False,
                'ordering': ('position',),
            },
            bases=(models.Model, mtr.sync.lib.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Replacer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('model', models.CharField(choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Mtr.Sync:Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Mtr.Sync:Sequence'), ('mtr_sync.replacercategory', 'Mtr_Sync | Mtr.Sync:Replacer Category'), ('mtr_sync.replacer', 'Mtr_Sync | Mtr.Sync:Replacer'), ('mtr_sync.field', 'Mtr_Sync | Mtr.Sync:Field'), ('mtr_sync.context', 'Mtr_Sync | Mtr.Sync:Context'), ('mtr_sync.report', 'Mtr_Sync | Mtr.Sync:Report'), ('mtr_sync.message', 'Mtr_Sync | Mtr.Sync:Message')], verbose_name='mtr.sync:model', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:replacer category',
                'verbose_name_plural': 'mtr.sync:replacer categories',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', db_index=True, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', null=True, blank=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:report',
                'verbose_name_plural': 'mtr.sync:reports',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:sequence',
                'verbose_name_plural': 'mtr.sync:sequences',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', db_index=True, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('name', models.CharField(help_text='mtr.sync:Small description of operation', verbose_name='mtr.sync:name', blank=True, max_length=100)),
                ('start_row', models.PositiveIntegerField(help_text='mtr.sync:Reading or writing start index (including itself)', verbose_name='mtr.sync:start row', null=True, blank=True)),
                ('end_row', models.PositiveIntegerField(help_text='mtr.sync:Reading or writing end index (including itself)', verbose_name='mtr.sync:end row', null=True, blank=True)),
                ('model', models.CharField(help_text='mtr.sync:Choose database model if action need it', choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Sequence'), ('mtr_sync.replacercategory', 'Mtr_Sync | Replacer Category'), ('mtr_sync.replacer', 'Mtr_Sync | Replacer'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.context', 'Mtr_Sync | Context'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.message', 'Mtr_Sync | Message')], verbose_name='mtr.sync:model', blank=True, max_length=255)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('processor', models.CharField(help_text='mtr.sync:Choose file type', choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='mtr.sync:format', default='XlsxProcessor', max_length=255)),
                ('worksheet', models.CharField(help_text='mtr.sync:Page name of sheet book', verbose_name='mtr.sync:worksheet page', blank=True, max_length=255)),
                ('include_header', models.BooleanField(help_text='mtr.sync:Check it if you need to write field names in export or skip it in import', verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(help_text='mtr.sync:Custom filename for export', verbose_name='mtr.sync:custom filename', blank=True, max_length=255)),
                ('buffer_file', models.FileField(help_text='mtr.sync:File for import action', verbose_name='mtr.sync:file', db_index=True, blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('dataset', models.CharField(help_text='mtr.sync:Custom registered dataset if you import or export data from different source, for example network or ftp server', choices=[('some_dataset', 'some description')], verbose_name='mtr.sync:dataset', blank=True, max_length=255)),
                ('data_action', models.CharField(help_text='mtr.sync:What will be done with data, for example, create or some custom opeartion eg. download image from server', choices=[('create', 'mtr.sync:Create only'), ('create_or_update', 'mtr.sync:Create or update'), ('update', 'mtr.sync:Update only')], verbose_name='mtr.sync:data action', blank=True, max_length=255)),
                ('filter_dataset', models.BooleanField(help_text='mtr.sync:Check it if you have custom queryset and want to filter from querystring, for example from admin button', verbose_name='mtr.sync:filter custom dataset', default=True)),
                ('filter_querystring', models.CharField(help_text='mtr.sync:Querystring from admin or other source, if you choose import action this params will be used for updating!', verbose_name='mtr.sync:querystring', blank=True, max_length=255)),
                ('language', models.CharField(help_text='mtr.sync:Activates language before action, for example if you want you have modeltranslation app and you need to export or import only for choosed language', choices=[('de', 'German'), ('en', 'English')], verbose_name='mtr.sync:language', blank=True, max_length=255)),
                ('hide_translation_fields', models.BooleanField(help_text="mtr.sync:If you don't want to create _lang field settings and dublicate in attribute list, handy if you using modeltranslation", verbose_name='mtr.sync:Hide translation prefixed fields', default=True)),
                ('create_fields', models.BooleanField(help_text='mtr.sync:Automaticaly creates all settings for model fields', verbose_name='mtr.sync:Create settings for fields', default=True)),
                ('populate_from_file', models.BooleanField(help_text='mtr.sync:Read start row, end row and first worksheet page from given file', verbose_name='mtr.sync:Populate settings from file', default=False)),
                ('include_related', models.BooleanField(help_text="mtr.sync:Include ForeignKey and ManyToManyField fields when using 'create fields' option", verbose_name='mtr.sync:Include related fields', default=True)),
                ('edit_attributes', models.BooleanField(help_text='mtr.sync:If you want to add custom attributes for custom action, by checking this option, you can edit attributes', verbose_name='mtr.sync:Edit field attributes', default=False)),
            ],
            options={
                'verbose_name': 'mtr.sync:settings',
                'verbose_name_plural': 'mtr.sync:settings',
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
            field=models.ForeignKey(verbose_name='mtr.sync:settings', null=True, blank=True, to='mtr_sync.Settings', related_name='reports'),
        ),
        migrations.AddField(
            model_name='replacer',
            name='category',
            field=models.ForeignKey(verbose_name='mtr.sync:category', null=True, blank=True, to='mtr_sync.ReplacerCategory', related_name='replacers'),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='messages'),
        ),
        migrations.AddField(
            model_name='field',
            name='replacer_category',
            field=models.ForeignKey(verbose_name='mtr.sync:replacer category', null=True, blank=True, to='mtr_sync.ReplacerCategory', related_name='fields'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', null=True, blank=True, to='mtr_sync.Settings', related_name='contexts'),
        ),
    ]
