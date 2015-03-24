# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Settings'
        db.create_table(u'sync_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_col', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('start_row', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('end_col', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('end_row', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('main_model', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('main_model_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('processor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('worksheet', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('include_header', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('buffer_file', self.gf('django.db.models.fields.files.FileField')(db_index=True, max_length=100, blank=True)),
            ('queryset', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'sync', ['Settings'])

        # Adding model 'ValueProcessor'
        db.create_table(u'sync_valueprocessor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=20000, null=True, blank=True)),
        ))
        db.send_create_signal(u'sync', ['ValueProcessor'])

        # Adding model 'Field'
        db.create_table(u'sync_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('skip', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['sync.Settings'])),
        ))
        db.send_create_signal(u'sync', ['Field'])

        # Adding model 'ValueProcessorParams'
        db.create_table(u'sync_valueprocessorparams', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('processor_related', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sync.ValueProcessor'])),
            ('field_related', self.gf('django.db.models.fields.related.ForeignKey')(related_name='processor_params', to=orm['sync.Field'])),
        ))
        db.send_create_signal(u'sync', ['ValueProcessorParams'])

        # Adding model 'Report'
        db.create_table(u'sync_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('buffer_file', self.gf('django.db.models.fields.files.FileField')(db_index=True, max_length=100, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('completed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reports', null=True, to=orm['sync.Settings'])),
        ))
        db.send_create_signal(u'sync', ['Report'])

        # Adding model 'Error'
        db.create_table(u'sync_error', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='errors', to=orm['sync.Report'])),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=10000)),
            ('step', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
            ('input_position', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('input_value', self.gf('django.db.models.fields.TextField')(max_length=60000, null=True, blank=True)),
        ))
        db.send_create_signal(u'sync', ['Error'])


    def backwards(self, orm):
        # Deleting model 'Settings'
        db.delete_table(u'sync_settings')

        # Deleting model 'ValueProcessor'
        db.delete_table(u'sync_valueprocessor')

        # Deleting model 'Field'
        db.delete_table(u'sync_field')

        # Deleting model 'ValueProcessorParams'
        db.delete_table(u'sync_valueprocessorparams')

        # Deleting model 'Report'
        db.delete_table(u'sync_report')

        # Deleting model 'Error'
        db.delete_table(u'sync_error')


    models = {
        u'sync.error': {
            'Meta': {'object_name': 'Error'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_position': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'input_value': ('django.db.models.fields.TextField', [], {'max_length': '60000', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'errors'", 'to': u"orm['sync.Report']"}),
            'step': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'})
        },
        u'sync.field': {
            'Meta': {'ordering': "['position']", 'object_name': 'Field'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'processors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sync.ValueProcessor']", 'through': u"orm['sync.ValueProcessorParams']", 'symmetrical': 'False'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['sync.Settings']"}),
            'skip': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'sync.report': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Report'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'buffer_file': ('django.db.models.fields.files.FileField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'completed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reports'", 'null': 'True', 'to': u"orm['sync.Settings']"}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'sync.settings': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Settings'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'buffer_file': ('django.db.models.fields.files.FileField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_col': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'end_row': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_header': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'main_model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'main_model_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'processor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'queryset': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'start_col': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'start_row': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'worksheet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'sync.valueprocessor': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'ValueProcessor'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '20000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sync.valueprocessorparams': {
            'Meta': {'ordering': "['position']", 'object_name': 'ValueProcessorParams'},
            'field_related': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'processor_params'", 'to': u"orm['sync.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'processor_related': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sync.ValueProcessor']"})
        }
    }

    complete_apps = ['sync']