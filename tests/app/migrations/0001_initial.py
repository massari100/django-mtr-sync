# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'name')),
                ('surname', models.CharField(max_length=255, verbose_name=b'surname')),
                ('gender', models.CharField(max_length=255, verbose_name=b'gender', choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('security_level', models.PositiveIntegerField(verbose_name=b'security level')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
            },
            bases=(models.Model,),
        ),
    ]
