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
                ('name', models.CharField(max_length=255, verbose_name='mtr.sync:name')),
                ('model', models.CharField(max_length=255, verbose_name='mtr.sync:model')),
                ('column', models.CharField(max_length=255, verbose_name='mtr.sync:column')),
            ],
            options={
                'verbose_name': 'mtr.sync:field',
                'verbose_name_plural': 'mtr.sync:fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file', db_index=True)),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('completed_at', models.DateTimeField(null=True, verbose_name='completed at', blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'get_latest_by': '-started_at',
                'verbose_name': 'log entry',
                'verbose_name_plural': 'log entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'mtr.actions:Export'), (1, 'mtr.actions:Import')])),
                ('name', models.CharField(max_length=100, verbose_name='mtr.sync:name')),
                ('start_column', models.CharField(max_length=10, verbose_name='mtr.sync:start column', blank=True)),
                ('start_row', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:start row', blank=True)),
                ('end_column', models.CharField(max_length=10, verbose_name='mtr.sync:end column', blank=True)),
                ('end_row', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:end row', blank=True)),
                ('limit_upload_data', models.BooleanField(default=False, verbose_name='mtr.sync:limit upload data')),
                ('main_model', models.CharField(max_length=255, verbose_name='mtr.sync:main model', blank=True)),
                ('main_model_id', models.PositiveIntegerField(null=True, verbose_name='mtr.sync:main model object', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'mtr.sync:settings',
                'verbose_name_plural': 'mtr.sync:settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='log',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:used settings', blank=True, to='mtr_sync.Settings', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:settings', to='mtr_sync.Settings'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='field',
            order_with_respect_to='settings',
        ),
    ]
