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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('cell', models.CharField(max_length=1000, verbose_name='mtr.sync:cell', blank=True)),
                ('value', models.CharField(max_length=1000, verbose_name='mtr.sync:value', blank=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:contexts',
                'verbose_name': 'mtr.sync:context',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(default=0, blank=True, verbose_name='utils:position', null=True)),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name', blank=True)),
                ('attribute', models.CharField(max_length=255, verbose_name='mtr.sync:model attribute')),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('set_filter', models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:set filter type', choices=[('not', 'mtr.sync:Not create or update instance if empty cell')])),
                ('set_value', models.CharField(max_length=255, verbose_name='mtr.sync:set value', blank=True)),
                ('find_filter', models.CharField(max_length=255, default='exact', blank=True, verbose_name='mtr.sync:find filter type', choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte'), ('not', 'not')])),
                ('find_value', models.CharField(max_length=255, verbose_name='mtr.sync:find value', blank=True)),
                ('converters', models.CharField(max_length=255, verbose_name='mtr.sync:converters', blank=True)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name_plural': 'mtr.sync:fields',
                'abstract': False,
                'verbose_name': 'mtr.sync:field',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('position', models.PositiveIntegerField(default=0, blank=True, verbose_name='utils:position', null=True)),
                ('message', models.TextField(max_length=10000, verbose_name='mtr.sync:message')),
                ('step', models.PositiveSmallIntegerField(default=1, verbose_name='mtr.sync:step', choices=[(0, 'mtr.sync:import data'), (1, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(max_length=10, verbose_name='mtr.sync:input position', blank=True)),
                ('input_value', models.TextField(max_length=60000, blank=True, verbose_name='mtr.sync:input value', null=True)),
                ('type', models.PositiveSmallIntegerField(default=0, verbose_name='mtr.sync:type', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')])),
            ],
            options={
                'ordering': ('position',),
                'verbose_name_plural': 'mtr.sync:messages',
                'abstract': False,
                'verbose_name': 'mtr.sync:message',
            },
            bases=(models.Model, mtr.sync.lib.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='mtr.sync:status', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:started at')),
                ('completed_at', models.DateTimeField(blank=True, verbose_name='mtr.sync:completed at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:reports',
                'verbose_name': 'mtr.sync:report',
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:file', blank=True)),
                ('description', models.TextField(blank=True, verbose_name='mtr.sync:description', null=True)),
            ],
            options={
                'verbose_name_plural': 'mtr.sync:sequences',
                'verbose_name': 'mtr.sync:sequence',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:action', choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('name', models.CharField(max_length=100, verbose_name='mtr.sync:name', help_text='mtr.sync:Small description of operation', blank=True)),
                ('start_row', models.PositiveIntegerField(blank=True, verbose_name='mtr.sync:start row', help_text='mtr.sync:Reading or writing start index (including itself)', null=True)),
                ('end_row', models.PositiveIntegerField(blank=True, verbose_name='mtr.sync:end row', help_text='mtr.sync:Reading or writing end index (including itself)', null=True)),
                ('model', models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:model', help_text='mtr.sync:Choose database model if action need it', choices=[('', '---------'), ('admin.logentry', 'Admin | Log Entry'), ('auth.permission', 'Auth | Permission'), ('auth.group', 'Auth | Group'), ('auth.user', 'Auth | User'), ('contenttypes.contenttype', 'Contenttypes | Content Type'), ('sessions.session', 'Sessions | Session'), ('app.office', 'App | Office'), ('app.tag', 'App | Tag'), ('app.person', 'App | Person'), ('mtr_sync.settings', 'Mtr_Sync | Mtr.Sync:Settings'), ('mtr_sync.sequence', 'Mtr_Sync | Mtr.Sync:Sequence'), ('mtr_sync.field', 'Mtr_Sync | Mtr.Sync:Field'), ('mtr_sync.context', 'Mtr_Sync | Mtr.Sync:Context'), ('mtr_sync.report', 'Mtr_Sync | Mtr.Sync:Report'), ('mtr_sync.message', 'Mtr_Sync | Mtr.Sync:Message')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:updated at')),
                ('processor', models.CharField(max_length=255, default='XlsxProcessor', verbose_name='mtr.sync:format', help_text='mtr.sync:Choose file type')),
                ('worksheet', models.CharField(max_length=255, verbose_name='mtr.sync:worksheet page', help_text='mtr.sync:Page name of sheet book', blank=True)),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header', help_text='mtr.sync:Check it if you need to write field names in export or skip it in import')),
                ('filename', models.CharField(max_length=255, verbose_name='mtr.sync:custom filename', help_text='mtr.sync:Custom filename for export', blank=True)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, help_text='mtr.sync:File for import action', blank=True)),
                ('dataset', models.CharField(max_length=255, verbose_name='mtr.sync:dataset', help_text='mtr.sync:Custom registered dataset if you import or export data from different source, for example network or ftp server', blank=True)),
                ('data_action', models.CharField(max_length=255, verbose_name='mtr.sync:data action', help_text='mtr.sync:What will be done with data, for example, create or some custom opeartion eg. download image from server', blank=True)),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset', help_text='mtr.sync:Check it if you have custom queryset and want to filter from querystring, for example from admin button')),
                ('filter_querystring', models.CharField(max_length=255, verbose_name='mtr.sync:querystring', help_text='mtr.sync:Querystring from admin or other source, if you choose import action this params will be used for updating!', blank=True)),
                ('language', models.CharField(max_length=255, blank=True, verbose_name='mtr.sync:language', help_text='mtr.sync:Activates language before action, for example if you want you have modeltranslation app and you need to export or import only for choosed language', choices=[('de', 'German'), ('en', 'English')])),
                ('hide_translation_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Hide translation prefixed fields', help_text="mtr.sync:If you don't want to create _lang field settings and dublicate in attribute list, handy if you using modeltranslation")),
                ('create_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Create settings for fields', help_text='mtr.sync:Automaticaly creates all settings for model fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='mtr.sync:Populate settings from file', help_text='mtr.sync:Read start row, end row and first worksheet page from given file')),
                ('include_related', models.BooleanField(default=True, verbose_name='mtr.sync:Include related fields', help_text="mtr.sync:Include ForeignKey and ManyToManyField fields when using 'create fields' option")),
                ('edit_attributes', models.BooleanField(default=False, verbose_name='mtr.sync:Edit field attributes', help_text='mtr.sync:If you want to add custom attributes for custom action, by checking this option, you can edit attributes')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:settings',
                'verbose_name': 'mtr.sync:settings',
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
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', null=True, related_name='reports', blank=True),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='messages'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', related_name='fields'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', null=True, related_name='contexts', blank=True),
        ),
    ]
