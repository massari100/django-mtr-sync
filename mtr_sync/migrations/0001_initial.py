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
                ('position', models.PositiveIntegerField(verbose_name='mtr.utils:position', null=True, blank=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', blank=True, max_length=255)),
                ('attribute', models.CharField(verbose_name='mtr.sync:model attribute', max_length=255)),
                ('skip', models.BooleanField(default=False, verbose_name='mtr.sync:skip')),
                ('update', models.BooleanField(default=True, verbose_name='mtr.sync:update')),
                ('find', models.BooleanField(default=False, verbose_name='mtr.sync:find')),
                ('set_filter', models.CharField(verbose_name='mtr.sync:set filter type', choices=[('not', 'mtr.sync:Not create or update instance if empty cell')], blank=True, max_length=255)),
                ('set_value', models.CharField(verbose_name='mtr.sync:set value', blank=True, max_length=255)),
                ('find_filter', models.CharField(default='exact', verbose_name='mtr.sync:find filter type', choices=[('icontains', 'icontains'), ('contains', 'contains'), ('iexact', 'iexact'), ('exact', 'exact'), ('in', 'in'), ('gt', 'gt'), ('gte', 'gte'), ('lt', 'lt'), ('lte', 'lte'), ('not', 'not')], blank=True, max_length=255)),
                ('find_value', models.CharField(verbose_name='mtr.sync:find value', blank=True, max_length=255)),
                ('converters', models.CharField(verbose_name='mtr.sync:converters', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
                'ordering': ('position',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('position', models.PositiveIntegerField(verbose_name='mtr.utils:position', null=True, blank=True)),
                ('message', models.TextField(verbose_name='mtr.sync:message', max_length=10000)),
                ('step', models.PositiveSmallIntegerField(default=1, verbose_name='mtr.sync:step', choices=[(0, 'mtr.sync:import data'), (1, 'mtr.sync:unexpected error')])),
                ('input_position', models.CharField(verbose_name='mtr.sync:input position', blank=True, max_length=10)),
                ('input_value', models.TextField(verbose_name='mtr.sync:input value', null=True, blank=True, max_length=60000)),
                ('type', models.PositiveSmallIntegerField(default=0, verbose_name='mtr.sync:type', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Info')])),
            ],
            options={
                'verbose_name': 'mtr.sync:message',
                'verbose_name_plural': 'mtr.sync:messages',
                'ordering': ('position',),
                'abstract': False,
            },
            bases=(models.Model, mtr.sync.lib.exceptions.ErrorChoicesMixin),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, default=0, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action')),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='mtr.sync:status', choices=[(0, 'mtr.sync:Error'), (1, 'mtr.sync:Running'), (2, 'mtr.sync:Success')])),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='mtr.sync:name', max_length=255)),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path, blank=True)),
                ('description', models.TextField(verbose_name='mtr.sync:description', null=True, blank=True)),
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
                ('action', models.PositiveSmallIntegerField(db_index=True, default=0, choices=[(0, 'mtr.sync:Export'), (1, 'mtr.sync:Import')], verbose_name='mtr.sync:action')),
                ('name', models.CharField(verbose_name='mtr.sync:name', help_text='mtr.sync:Small description of operation', blank=True, max_length=100)),
                ('start_row', models.PositiveIntegerField(verbose_name='mtr.sync:start row', help_text='mtr.sync:Reading or writing start index (including itself)', null=True, blank=True)),
                ('end_row', models.PositiveIntegerField(verbose_name='mtr.sync:end row', help_text='mtr.sync:Reading or writing end index (including itself)', null=True, blank=True)),
                ('model', models.CharField(verbose_name='mtr.sync:model', help_text='mtr.sync:Choose database model if action need it', blank=True, max_length=255)),
                ('created_at', models.DateTimeField(verbose_name='mtr.sync:created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='mtr.sync:updated at', auto_now=True)),
                ('show_in_quick_menu', models.BooleanField(default=False, verbose_name='mtr.sync:show in quick menu list')),
                ('processor', models.CharField(default='XlsxProcessor', verbose_name='mtr.sync:format', help_text='mtr.sync:Choose file type', max_length=255)),
                ('worksheet', models.CharField(verbose_name='mtr.sync:worksheet page', help_text='mtr.sync:Page name of sheet book', blank=True, max_length=255)),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header', help_text='mtr.sync:Check it if you need to write field names in export or skip it in import')),
                ('filename', models.CharField(verbose_name='mtr.sync:custom filename', help_text='mtr.sync:Custom filename for export', blank=True, max_length=255)),
                ('buffer_file', models.FileField(db_index=True, verbose_name='mtr.sync:file', upload_to=mtr.sync.settings.get_buffer_file_path, blank=True, help_text='mtr.sync:File for import action')),
                ('dataset', models.CharField(verbose_name='mtr.sync:dataset', help_text='mtr.sync:Custom registered dataset if you import or export data from different source, for example network or ftp server', blank=True, max_length=255)),
                ('data_action', models.CharField(verbose_name='mtr.sync:data action', help_text='mtr.sync:What will be done with data, for example, create or some custom opeartion eg. download image from server', blank=True, max_length=255)),
                ('filter_dataset', models.BooleanField(default=True, verbose_name='mtr.sync:filter custom dataset', help_text='mtr.sync:Check it if you have custom queryset and want to filter from querystring, for example from admin button')),
                ('filter_querystring', models.CharField(verbose_name='mtr.sync:querystring', help_text='mtr.sync:Querystring from admin or other source, if you choose import action this params will be used for updating!', blank=True, max_length=255)),
                ('language', models.CharField(verbose_name='mtr.sync:language', choices=[('de', 'German'), ('en', 'English')], help_text='mtr.sync:Activates language before action, for example if you want you have modeltranslation app and you need to export or import only for choosed language', blank=True, max_length=255)),
                ('hide_translation_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Hide translation prefixed fields', help_text="mtr.sync:If you don't want to create _lang field settings and dublicate in attribute list, handy if you using modeltranslation")),
                ('create_fields', models.BooleanField(default=True, verbose_name='mtr.sync:Create settings for fields', help_text='mtr.sync:Automaticaly creates all settings for model fields')),
                ('populate_from_file', models.BooleanField(default=False, verbose_name='mtr.sync:Populate settings from file', help_text='mtr.sync:Read start row, end row and first worksheet page from given file')),
                ('include_related', models.BooleanField(default=True, verbose_name='mtr.sync:Include related fields', help_text="mtr.sync:Include ForeignKey and ManyToManyField fields when using 'create fields' option")),
                ('edit_attributes', models.BooleanField(default=False, verbose_name='mtr.sync:Edit field attributes', help_text='mtr.sync:If you want to add custom attributes for custom action, by checking this option, you can edit attributes')),
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
            field=models.ManyToManyField(verbose_name='mtr.sync:settings', related_name='sequences', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', null=True, blank=True, related_name='reports', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='message',
            name='report',
            field=models.ForeignKey(to='mtr_sync.Report', related_name='messages'),
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', related_name='fields', to='mtr_sync.Settings'),
        ),
        migrations.AddField(
            model_name='context',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', null=True, blank=True, related_name='contexts', to='mtr_sync.Settings'),
        ),
    ]
