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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('office', models.CharField(verbose_name='office', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255)),
            ],
            options={
                'verbose_name': 'office',
                'verbose_name_plural': 'offices',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('name_de', models.CharField(verbose_name='name', null=True, max_length=255)),
                ('name_en', models.CharField(verbose_name='name', null=True, max_length=255)),
                ('surname', models.CharField(verbose_name='surname', max_length=255)),
                ('surname_de', models.CharField(verbose_name='surname', null=True, max_length=255)),
                ('surname_en', models.CharField(verbose_name='surname', null=True, max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], verbose_name='gender', max_length=255)),
                ('security_level', models.PositiveIntegerField(verbose_name='security level')),
                ('some_excluded_field', models.DecimalField(decimal_places=3, verbose_name='some decimal', null=True, max_digits=10)),
                ('office', models.ForeignKey(blank=True, to='app.Office', null=True)),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='tag', max_length=255)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=models.ManyToManyField(to='app.Tag'),
        ),
    ]
