# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
        ('mtr_sync', '0002_auto_20150207_0106'),
    ]

    operations = [
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
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='LogEntry',
        ),
        migrations.AddField(
            model_name='log',
            name='settings',
            field=models.ForeignKey(verbose_name='mtr.sync:used settings', blank=True, to='mtr_sync.Settings', null=True),
            preserve_default=True,
        ),
    ]
