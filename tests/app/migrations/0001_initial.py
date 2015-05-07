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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('office', models.CharField(max_length=255, verbose_name=b'office')),
                ('address', models.CharField(max_length=255, verbose_name=b'address')),
            ],
            options={
                'verbose_name': 'office',
                'verbose_name_plural': 'offices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'name')),
                ('name_de', models.CharField(max_length=255, null=True, verbose_name=b'name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name=b'name')),
                ('surname', models.CharField(max_length=255, verbose_name=b'surname')),
                ('surname_de', models.CharField(max_length=255, null=True, verbose_name=b'surname')),
                ('surname_en', models.CharField(max_length=255, null=True, verbose_name=b'surname')),
                ('gender', models.CharField(max_length=255, verbose_name=b'gender', choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('security_level', models.PositiveIntegerField(verbose_name=b'security level')),
                ('some_excluded_field', models.DecimalField(null=True, verbose_name=b'some decimal', max_digits=10, decimal_places=3)),
                ('office', models.ForeignKey(blank=True, to='app.Office', null=True)),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'tag')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
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
