# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mtr_sync', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filter',
            options={'ordering': ('-id',), 'verbose_name': 'filter', 'verbose_name_plural': 'filters'},
        ),
        migrations.RenameField(
            model_name='settings',
            old_name='limit_upload_data',
            new_name='limit_data',
        ),
        migrations.AddField(
            model_name='settings',
            name='include_header',
            field=models.BooleanField(default=True, verbose_name='mtr.sync:include header'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='settings',
            name='worksheet',
            field=models.CharField(max_length=255, verbose_name='mtr.sync:worksheet page', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filter',
            name='description',
            field=models.TextField(max_length=20000, null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filter',
            name='template',
            field=models.TextField(max_length=50000, verbose_name='template'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='settings',
            name='processor',
            field=models.CharField(max_length=255, verbose_name='processor'),
            preserve_default=True,
        ),
    ]
