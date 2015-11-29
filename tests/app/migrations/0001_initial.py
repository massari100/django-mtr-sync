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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('office', models.CharField(max_length=255, verbose_name='office')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
            ],
            options={
                'verbose_name_plural': 'offices',
                'verbose_name': 'office',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('name_de', models.CharField(null=True, max_length=255, verbose_name='name')),
                ('name_en', models.CharField(null=True, max_length=255, verbose_name='name')),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('surname_de', models.CharField(null=True, max_length=255, verbose_name='surname')),
                ('surname_en', models.CharField(null=True, max_length=255, verbose_name='surname')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=255, verbose_name='gender')),
                ('security_level', models.PositiveIntegerField(verbose_name='security level')),
                ('some_excluded_field', models.DecimalField(decimal_places=3, null=True, max_digits=10, verbose_name='some decimal')),
                ('office', models.ForeignKey(blank=True, null=True, to='app.Office')),
            ],
            options={
                'verbose_name_plural': 'persons',
                'verbose_name': 'person',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='tag')),
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
