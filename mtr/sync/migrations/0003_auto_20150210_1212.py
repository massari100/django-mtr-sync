# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mtr_sync', '0002_auto_20150210_1157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settings',
            old_name='end_column',
            new_name='end_col',
        ),
        migrations.RenameField(
            model_name='settings',
            old_name='start_column',
            new_name='start_col',
        ),
    ]
