# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mtr.sync.settings


class Migration(migrations.Migration):

    dependencies = [
        ('mtr_sync', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logentry',
            options={'get_latest_by': '-started_at', 'verbose_name': 'log entry', 'verbose_name_plural': 'log entries'},
        ),
        migrations.AlterField(
            model_name='logentry',
            name='action',
            field=models.PositiveSmallIntegerField(db_index=True, verbose_name='action', choices=[(0, 'Export'), (1, 'Import')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='buffer_file',
            field=models.FileField(upload_to=mtr.sync.settings.get_buffer_file_path, verbose_name='file'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='completed_at',
            field=models.DateTimeField(null=True, verbose_name='completed at', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='started_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='started at'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='status', choices=[(0, 'Error'), (1, 'Running'), (2, 'Success')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='logentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
            preserve_default=True,
        ),
    ]
