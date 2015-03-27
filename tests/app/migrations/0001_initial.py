# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.CharField(max_length=255, verbose_name='office')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
            ],
            options={
                'verbose_name_plural': 'offices',
                'verbose_name': 'office',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('gender', models.CharField(max_length=255, choices=[('M', 'Male'), ('F', 'Female')], verbose_name='gender')),
                ('security_level', models.PositiveIntegerField(verbose_name='security level')),
                ('some_excluded_field', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='some decimal', null=True)),
                ('office', models.ForeignKey(to='app.Office', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'persons',
                'verbose_name': 'person',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='tag')),
            ],
            options={
                'verbose_name_plural': 'tags',
                'verbose_name': 'tag',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=models.ManyToManyField(to='app.Tag'),
            preserve_default=True,
        ),
    ]
