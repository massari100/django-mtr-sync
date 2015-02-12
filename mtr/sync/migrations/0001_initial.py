# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('model', models.CharField(max_length=255, verbose_name='model')),
                ('column', models.CharField(max_length=255, verbose_name='column')),
            ],
            options={
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(max_length=20000, null=True, verbose_name='description', blank=True)),
                ('template', models.TextField(max_length=50000, verbose_name='template')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'filter',
                'verbose_name_plural': 'filters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_related', models.ForeignKey(related_name='filter_params', to='mtr_sync.Field')),
                ('filter_related', models.ForeignKey(to='mtr_sync.Filter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('buffer_file', models.FileField(db_index=True, upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(null=True, verbose_name='completed at', blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'report',
                'verbose_name_plural': 'reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')])),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('start_col', models.CharField(max_length=10, verbose_name='start column', blank=True)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='start row', blank=True)),
                ('end_col', models.CharField(max_length=10, verbose_name='end column', blank=True)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='end row', blank=True)),
                ('limit_data', models.BooleanField(default=False, verbose_name='limit upload data')),
                ('main_model', models.CharField(max_length=255, verbose_name='main model', choices=[(b'django.contrib.admin.models', 'log entry'), (b'django.contrib.auth.models', 'permission'), (b'django.contrib.auth.models', 'group'), (b'django.contrib.auth.models', 'user'), (b'django.contrib.contenttypes.models', 'content type'), (b'django.contrib.sessions.models', 'session'), (b'mtr.sync.models', 'settings'), (b'mtr.sync.models', 'filter'), (b'mtr.sync.models', 'field'), (b'mtr.sync.models', 'filter params'), (b'mtr.sync.models', 'report')])),
                ('main_model_id', models.PositiveIntegerField(null=True, verbose_name='main model object', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('processor', models.CharField(max_length=255, verbose_name='processor')),
                ('worksheet', models.CharField(max_length=255, verbose_name='mtr.sync:worksheet page', blank=True)),
                ('include_header', models.BooleanField(default=True, verbose_name='mtr.sync:include header')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='settings',
            field=models.ForeignKey(verbose_name='used settings', blank=True, to='mtr_sync.Settings', null=True),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='filterparams',
            order_with_respect_to='field_related',
        ),
        migrations.AddField(
            model_name='field',
            name='filters',
            field=models.ManyToManyField(to='mtr_sync.Filter', through='mtr_sync.FilterParams'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(related_name='fields', verbose_name='settings', to='mtr_sync.Settings'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='field',
            order_with_respect_to='settings',
        ),
    ]
