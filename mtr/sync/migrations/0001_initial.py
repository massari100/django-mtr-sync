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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('cell', models.CharField(max_length=1000, blank=True, verbose_name='mtr.sync:cell')),
                ('value', models.CharField(max_length=1000, blank=True, verbose_name='mtr.sync:value')),
            ],
            options={
                'verbose_name': 'mtr.sync:context',
                'verbose_name_plural': 'mtr.sync:contexts',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(blank=True, default=0, verbose_name='utils:position', null=True)),
                ('name', models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:name')),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('update', models.BooleanField(verbose_name='mtr.sync:update', default=True)),
                ('find', models.BooleanField(verbose_name='mtr.sync:find', default=False)),
                ('set_filter', models.CharField(max_length=255, blank=True, choices=[('not', 'mtr.sync:Not create or update instance if empty cell')], verbose_name='mtr.sync:set filter type')),
                ('set_value', models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:set value')),
                ('find_filter', models.CharField(max_length=255, blank=True, choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte'), ('not', 'not')], verbose_name='mtr.sync:find filter type', default='exact')),
                ('find_value', models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:find value')),
                ('converters', models.CharField(max_length=255, blank=True, choices=[('decimal', 'mtr.sync:Decimal'), ('string', 'mtr.sync:String'), ('comalist', 'mtr.sync:Coma separated list'), ('boolean', 'mtr.sync:Boolean'), ('filepath', 'mtr.sync:File path'), ('integer', 'mtr.sync:Integer'), ('none', 'mtr.sync:None')], verbose_name='mtr.sync:converters')),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:fields',
                'verbose_name': 'mtr.sync:field',
                'abstract': False,
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('position', models.PositiveIntegerField(blank=True, default=0, verbose_name='utils:position', null=True)),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:import data'), (1, 'mtr.sync:unexpected error')], verbose_name='mtr.sync:step', default=1)),
                ('input_position', models.CharField(max_length=10, blank=True, verbose_name='mtr.sync:input position')),
                ('input_value', models.TextField(max_length=60000, blank=True, verbose_name='mtr.sync:input value', null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')], verbose_name='mtr.sync:type', default=0)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:messages',
                'verbose_name': 'mtr.sync:message',
                'abstract': False,
                'ordering': ('position',),
            },
            bases=(models.Model, mtr.sync.lib.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action')),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, verbose_name='mtr.sync:file')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')], verbose_name='mtr.sync:status', default=1)),
                ('started_at', models.DateTimeField(verbose_name='mtr.sync:started at', auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, verbose_name='mtr.sync:completed at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, verbose_name='mtr.sync:file')),
                ('description', models.TextField(blank=True, verbose_name='mtr.sync:description', null=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:sequence',
                'verbose_name_plural': 'mtr.sync:sequences',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action')),
                ('name', models.CharField(help_text='mtr.sync:Small description of operation', blank=True, verbose_name='mtr.sync:name', max_length=100)),
                ('start_row', models.PositiveIntegerField(help_text='mtr.sync:Reading or writing start index (including itself)', blank=True, verbose_name='mtr.sync:start row', null=True)),
                ('end_row', models.PositiveIntegerField(help_text='mtr.sync:Reading or writing end index (including itself)', blank=True, verbose_name='mtr.sync:end row', null=True)),
                ('model', models.CharField(help_text='mtr.sync:Choose database model if action need it', blank=True, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Sequence'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.context', 'Mtr_Sync | Context'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.message', 'Mtr_Sync | Message')], verbose_name='mtr.sync:model', max_length=255)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
                ('show_in_quick_menu', models.BooleanField(verbose_name='mtr.sync:show in quick menu list', default=False)),
                ('processor', models.CharField(default='XlsxProcessor', help_text='mtr.sync:Choose file type', choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')], verbose_name='mtr.sync:format', max_length=255)),
                ('worksheet', models.CharField(help_text='mtr.sync:Page name of sheet book', blank=True, verbose_name='mtr.sync:worksheet page', max_length=255)),
                ('include_header', models.BooleanField(help_text='mtr.sync:Check it if you need to write field names in export or skip it in import', verbose_name='mtr.sync:include header', default=True)),
                ('filename', models.CharField(help_text='mtr.sync:Custom filename for export', blank=True, verbose_name='mtr.sync:custom filename', max_length=255)),
                ('buffer_file', models.FileField(db_index=True, help_text='mtr.sync:File for import action', blank=True, verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('dataset', models.CharField(help_text='mtr.sync:Custom registered dataset if you import or export data from different source, for example network or ftp server', blank=True, choices=[('some_dataset', 'some description')], verbose_name='mtr.sync:dataset', max_length=255)),
                ('data_action', models.CharField(help_text='mtr.sync:What will be done with data, for example, create or some custom opeartion eg. download image from server', blank=True, choices=[('create', 'mtr.sync:Create only'), ('create_or_update', 'mtr.sync:Create or update'), ('update', 'mtr.sync:Update only')], verbose_name='mtr.sync:data action', max_length=255)),
                ('filter_dataset', models.BooleanField(help_text='mtr.sync:Check it if you have custom queryset and want to filter from querystring, for example from admin button', verbose_name='mtr.sync:filter custom dataset', default=True)),
                ('filter_querystring', models.CharField(help_text='mtr.sync:Querystring from admin or other source, if you choose import action this params will be used for updating!', blank=True, verbose_name='mtr.sync:querystring', max_length=255)),
                ('language', models.CharField(help_text='mtr.sync:Activates language before action, for example if you want you have modeltranslation app and you need to export or import only for choosed language', blank=True, choices=[('de', 'German'), ('en', 'English')], verbose_name='mtr.sync:language', max_length=255)),
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
            field=models.ManyToManyField(to='mtr_sync.Settings', verbose_name='mtr.sync:settings', related_name='sequences'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', blank=True, verbose_name='mtr.sync:settings', null=True, related_name='reports'),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='messages'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', verbose_name='mtr.sync:settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', blank=True, verbose_name='mtr.sync:settings', null=True, related_name='contexts'),
        ),
    ]
