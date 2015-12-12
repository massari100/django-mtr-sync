# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('office', models.CharField(verbose_name='office', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'offices',
                'verbose_name': 'office',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('name_de', models.CharField(null=True, verbose_name='name', max_length=255)),
                ('name_en', models.CharField(null=True, verbose_name='name', max_length=255)),
                ('surname', models.CharField(verbose_name='surname', max_length=255)),
                ('surname_de', models.CharField(null=True, verbose_name='surname', max_length=255)),
                ('surname_en', models.CharField(null=True, verbose_name='surname', max_length=255)),
                ('gender', models.CharField(verbose_name='gender', max_length=255, choices=[('M', 'Male'), ('F', 'Female')])),
                ('security_level', models.PositiveIntegerField(verbose_name='security level')),
                ('some_excluded_field', models.DecimalField(max_digits=10, verbose_name='some decimal', null=True, decimal_places=3)),
                ('office', models.ForeignKey(null=True, to='app.Office', blank=True)),
            ],
            options={
                'verbose_name_plural': 'persons',
                'verbose_name': 'person',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='tag', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'tags',
                'verbose_name': 'tag',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=models.ManyToManyField(to='app.Tag'),
        ),
    ]
