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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.utils:position', default=0, blank=True, null=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(verbose_name='mtr.sync:skip', default=False)),
                ('update', models.BooleanField(verbose_name='mtr.sync:update', default=True)),
                ('find', models.BooleanField(verbose_name='mtr.sync:find', default=False)),
                ('set_filter', models.CharField(verbose_name='mtr.sync:set filter type', blank=True, choices=[('not', 'mtr.sync:Not create or update instance if empty cell')], max_length=255)),
                ('set_value', models.CharField(verbose_name='mtr.sync:set value', blank=True, max_length=255)),
                ('find_filter', models.CharField(verbose_name='mtr.sync:find filter type', default='exact', blank=True, choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte'), ('not', 'not')], max_length=255)),
                ('find_value', models.CharField(verbose_name='mtr.sync:find value', blank=True, max_length=255)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'ordering': ('position',),
                'abstract': False,
                'verbose_name_plural': 'mtr.sync:fields',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.utils:position', default=0, blank=True, null=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(verbose_name='mtr.sync:step', default=1, choices=[(0, 'mtr.sync:import data'), (1, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', blank=True, null=True, max_length=60000)),
                ('type', models.PositiveSmallIntegerField(verbose_name='mtr.sync:type', default=0, choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')])),
            ],
            options={
                'verbose_name': 'mtr.sync:message',
                'ordering': ('position',),
                'abstract': False,
                'verbose_name_plural': 'mtr.sync:messages',
            },
            bases=(models.Model, mtr.sync.lib.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', db_index=True, default=0, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
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
            name='Sequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('description', models.TextField(verbose_name='mtr.sync:description', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'mtr.sync:sequence',
                'verbose_name_plural': 'mtr.sync:sequences',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(verbose_name='mtr.sync:action', db_index=True, default=0, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')])),
                ('name', models.CharField(verbose_name='mtr.sync:name', help_text='mtr.sync:Small description of operation', blank=True, max_length=100)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', help_text='mtr.sync:Reading or writing start index (including itself)', blank=True, null=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', help_text='mtr.sync:Reading or writing end index (including itself)', blank=True, null=True)),
                ('model', models.CharField(verbose_name='mtr.sync:model', help_text='mtr.sync:Choose database model if action need it', blank=True, max_length=255)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('show_in_quick_menu', models.BooleanField(verbose_name='mtr.sync:show in quick menu list', default=False)),
                ('processor', models.CharField(verbose_name='mtr.sync:format', help_text='mtr.sync:Choose file type', default='XlsxProcessor', max_length=255)),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', help_text='mtr.sync:Page name of sheet book', blank=True, max_length=255)),
                ('include_header', models.BooleanField(verbose_name='mtr.sync:include header', help_text='mtr.sync:Check it if you need to write field names in export or skip it in import', default=True)),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', help_text='mtr.sync:Custom filename for export', blank=True, max_length=255)),
                ('buffer_file', models.FileField(verbose_name='mtr.sync:file', db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, help_text='mtr.sync:File for import action', blank=True)),
                ('dataset', models.CharField(verbose_name='mtr.sync:dataset', help_text='mtr.sync:Custom registered dataset if you import or export data from different source, for example network or ftp server', blank=True, max_length=255)),
                ('data_action', models.CharField(verbose_name='mtr.sync:data action', help_text='mtr.sync:What will be done with data, for example, create or some custom opeartion eg. download image from server', blank=True, max_length=255)),
                ('filter_dataset', models.BooleanField(verbose_name='mtr.sync:filter custom dataset', help_text='mtr.sync:Check it if you have custom queryset and want to filter from querystring, for example from admin button', default=True)),
                ('filter_querystring', models.CharField(verbose_name='mtr.sync:querystring', help_text='mtr.sync:Querystring from admin or other source, if you choose import action this params will be used for updating!', blank=True, max_length=255)),
                ('language', models.CharField(verbose_name='mtr.sync:language', help_text='mtr.sync:Activates language before action, for example if you want you have modeltranslation app and you need to export or import only for choosed language', blank=True, choices=[('de', 'German'), ('en', 'English')], max_length=255)),
                ('hide_translation_fields', models.BooleanField(verbose_name='mtr.sync:Hide translation prefixed fields', help_text="mtr.sync:If you don't want to create _lang field settings and dublicate in attribute list, handy if you using modeltranslation", default=True)),
                ('create_fields', models.BooleanField(verbose_name='mtr.sync:Create settings for fields', help_text='mtr.sync:Automaticaly creates all settings for model fields', default=True)),
                ('populate_from_file', models.BooleanField(verbose_name='mtr.sync:Populate settings from file', help_text='mtr.sync:Read start row, end row and first worksheet page from given file', default=False)),
                ('include_related', models.BooleanField(verbose_name='mtr.sync:Include related fields', help_text="mtr.sync:Include ForeignKey and ManyToManyField fields when using 'create fields' option", default=True)),
                ('edit_attributes', models.BooleanField(verbose_name='mtr.sync:Edit field attributes', help_text='mtr.sync:If you want to add custom attributes for custom action, by checking this option, you can edit attributes', default=False)),
            ],
            options={
                'verbose_name': 'mtr.sync:settings',
                'ordering': ('-id',),
                'verbose_name_plural': 'mtr.sync:settings',
            },
        ),
        migrations.AddField(
            model_name='sequence',
            name='settings',
            field=models.ManyToManyField(verbose_name='mtr.sync:settings', related_name='sequences', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', blank=True, null=True, related_name='reports'),
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
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings', blank=True, null=True, related_name='contexts'),
        ),
    ]
