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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('office', models.CharField(max_length=255, verbose_name='office')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
            ],
            options={
                'verbose_name': 'office',
                'verbose_name_plural': 'offices',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('name_de', models.CharField(verbose_name='name', max_length=255, null=True)),
                ('name_en', models.CharField(verbose_name='name', max_length=255, null=True)),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('surname_de', models.CharField(verbose_name='surname', max_length=255, null=True)),
                ('surname_en', models.CharField(verbose_name='surname', max_length=255, null=True)),
                ('gender', models.CharField(verbose_name='gender', choices=[('M', 'Male'), ('F', 'Female')], max_length=255)),
                ('security_level', models.PositiveIntegerField(verbose_name='security level')),
                ('some_excluded_field', models.DecimalField(max_digits=10, decimal_places=3, null=True, verbose_name='some decimal')),
                ('office', models.ForeignKey(null=True, blank=True, to='app.Office')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='tag')),
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
