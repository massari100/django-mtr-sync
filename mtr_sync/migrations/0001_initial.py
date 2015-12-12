# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mtr.sync.settings
import mtr.sync.lib.exceptions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('cell', models.CharField(verbose_name='mtr.sync:cell', max_length=1000, blank=True)),
                ('value', models.CharField(verbose_name='mtr.sync:value', max_length=1000, blank=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:contexts',
                'verbose_name': 'mtr.sync:context',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.utils:position', null=True, blank=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255, blank=True)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('update', models.BooleanField(verbose_name='mtr.sync:update', default=True)),
                ('find', models.BooleanField(verbose_name='mtr.sync:find', default=False)),
                ('set_filter', models.CharField(verbose_name='mtr.sync:set filter type', max_length=255, blank=True, choices=[('not', 'mtr.sync:Not create or update instance if empty cell')])),
                ('set_value', models.CharField(verbose_name='mtr.sync:set value', max_length=255, blank=True)),
                ('find_filter', models.CharField(max_length=255, verbose_name='mtr.sync:find filter type', default='exact', blank=True, choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte'), ('not', 'not')])),
                ('find_value', models.CharField(verbose_name='mtr.sync:find value', max_length=255, blank=True)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', max_length=255, blank=True, choices=[('decimal', 'mtr.sync:Decimal'), ('string', 'mtr.sync:String'), ('comalist', 'mtr.sync:Coma separated list'), ('boolean', 'mtr.sync:Boolean'), ('filepath', 'mtr.sync:File path'), ('integer', 'mtr.sync:Integer'), ('none', 'mtr.sync:None')])),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.utils:position', null=True, blank=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', default=1, choices=[(0, 'mtr.sync:import data'), (1, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', max_length=10, blank=True)),
                ('input_value', models.TextField(null=True, verbose_name='mtr.sync:input value', max_length=60000, blank=True)),
                ('type', models.PositiveSmallIntegerField(verbose_name='mtr.sync:type', default=0, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')])),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:status', default=1, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:started at')),
                ('completed_at', models.DateTimeField(verbose_name='mtr.sync:completed at', null=True, blank=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', blank=True, upload_to=mtr.sync.settings.get_buffer_file_path)),
                ('description', models.TextField(verbose_name='mtr.sync:description', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:sequences',
                'verbose_name': 'mtr.sync:sequence',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=100, help_text='mtr.sync:Small description of operation', blank=True)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', null=True, help_text='mtr.sync:Reading or writing start index (including itself)', blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', null=True, help_text='mtr.sync:Reading or writing end index (including itself)', blank=True)),
                ('model', models.CharField(verbose_name='mtr.sync:model', max_length=255, help_text='mtr.sync:Choose database model if action need it', blank=True, choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Sequence'), ('mtr_sync.field', 'Mtr_Sync | Field'), ('mtr_sync.context', 'Mtr_Sync | Context'), ('mtr_sync.report', 'Mtr_Sync | Report'), ('mtr_sync.message', 'Mtr_Sync | Message')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('show_in_quick_menu', models.BooleanField(verbose_name='mtr.sync:show in quick menu list', default=False)),
                ('processor', models.CharField(max_length=255, verbose_name='mtr.sync:format', default='XlsxProcessor', help_text='mtr.sync:Choose file type', choices=[('XlsxProcessor', '.xlsx | Microsoft Excel 2007/2010/2013 XML'), ('XlsProcessor', '.xls | Microsoft Excel 97/2000/XP/2003'), ('OdsProcessor', '.ods | ODF Spreadsheet'), ('CsvProcessor', '.csv | CSV')])),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', max_length=255, help_text='mtr.sync:Page name of sheet book', blank=True)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', default=True, help_text='mtr.sync:Check it if you need to write field names in export or skip it in import')),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', max_length=255, help_text='mtr.sync:Custom filename for export', blank=True)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, db_index=True, verbose_name='mtr.sync:file', help_text='mtr.sync:File for import action', blank=True)),
                ('dataset', models.CharField(verbose_name='mtr.sync:dataset', max_length=255, help_text='mtr.sync:Custom registered dataset if you import or export data from different source, for example network or ftp server', blank=True, choices=[('some_dataset', 'some description')])),
                ('data_action', models.CharField(verbose_name='mtr.sync:data action', max_length=255, help_text='mtr.sync:What will be done with data, for example, create or some custom opeartion eg. download image from server', blank=True, choices=[('create', 'mtr.sync:Create only'), ('create_or_update', 'mtr.sync:Create or update'), ('update', 'mtr.sync:Update only')])),
                ('filter_dataset', models.BooleanField(verbose_name='mtr.sync:filter custom dataset', default=True, help_text='mtr.sync:Check it if you have custom queryset and want to filter from querystring, for example from admin button')),
                ('filter_querystring', models.CharField(verbose_name='mtr.sync:querystring', max_length=255, help_text='mtr.sync:Querystring from admin or other source, if you choose import action this params will be used for updating!', blank=True)),
                ('language', models.CharField(verbose_name='mtr.sync:language', max_length=255, help_text='mtr.sync:Activates language before action, for example if you want you have modeltranslation app and you need to export or import only for choosed language', blank=True, choices=[('de', 'German'), ('en', 'English')])),
                ('hide_translation_fields', models.BooleanField(verbose_name='mtr.sync:Hide translation prefixed fields', default=True, help_text="mtr.sync:If you don't want to create _lang field settings and dublicate in attribute list, handy if you using modeltranslation")),
                ('create_fields', models.BooleanField(verbose_name='mtr.sync:Create settings for fields', default=True, help_text='mtr.sync:Automaticaly creates all settings for model fields')),
                ('populate_from_file', models.BooleanField(verbose_name='mtr.sync:Populate settings from file', default=False, help_text='mtr.sync:Read start row, end row and first worksheet page from given file')),
                ('include_related', models.BooleanField(verbose_name='mtr.sync:Include related fields', default=True, help_text="mtr.sync:Include ForeignKey and ManyToManyField fields when using 'create fields' option")),
                ('edit_attributes', models.BooleanField(verbose_name='mtr.sync:Edit field attributes', default=False, help_text='mtr.sync:If you want to add custom attributes for custom action, by checking this option, you can edit attributes')),
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
            field=models.ManyToManyField(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='sequences'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(null=True, to='mtr_sync.Settings', verbose_name='mtr.sync:settings', related_name='reports', blank=True),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(related_name='messages', to='mtr_sync.Report'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(to='mtr_sync.Settings', related_name='fields', verbose_name='mtr.sync:settings'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(null=True, to='mtr_sync.Settings', verbose_name='mtr.sync:settings', related_name='contexts', blank=True),
        ),
    ]
