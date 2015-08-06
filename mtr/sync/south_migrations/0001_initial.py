# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReplacerCategory'
        db.create_table(u'sync_replacercategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'sync', ['ReplacerCategory'])


    def backwards(self, orm):
        # Deleting model 'ReplacerCategory'
        db.delete_table(u'sync_replacercategory')


    models = {
        u'sync.replacercategory': {
            'Meta': {'object_name': 'ReplacerCategory'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['sync']