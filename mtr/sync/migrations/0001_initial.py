# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buffer_file', models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='mtr.sync:LogEntry.file')),
                ('status', models.PositiveSmallIntegerField(verbose_name='mtr.sync:LogEntry.status', choices=[(0, 'mtr.sync:LogEntry.status.Error'), (1, 'mtr.sync:LogEntry.status.Running'), (2, 'mtr.sync:LogEntry.status.Success')])),
                ('action', models.PositiveSmallIntegerField(db_index=True, verbose_name='mtr.sync:LogEntry.action', choices=[(0, 'mtr.sync:LogEntry.action.Export'), (1, 'mtr.sync:LogEntry.action.Import')])),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='mtr.sync:LogEntry.started at')),
                ('completed_at', models.DateTimeField(null=True, verbose_name='mtr.sync:LogEntry.completed at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.sync:LogEntry.updated at')),
            ],
            options={
                'get_latest_by': '-started_at',
                'verbose_name': 'mtr.sync:LogEntry.log entry',
                'verbose_name_plural': 'mtr.sync:LogEntry.log entries',
            },
            bases=(models.Model,),
        ),
    ]
