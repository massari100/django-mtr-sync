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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('gender', models.CharField(max_length=255, verbose_name='gender', choices=[('M', 'Male'), ('F', 'Female')])),
                ('security_level', models.PositiveIntegerField(verbose_name='security level')),
            ],
            options={
                'verbose_name_plural': 'persons',
                'verbose_name': 'person',
            },
            bases=(models.Model,),
        ),
    ]
