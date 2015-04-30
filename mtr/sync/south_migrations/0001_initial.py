# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Settings'
        db.create_table(u'mtr_sync_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('start_col', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('start_row', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('end_col', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('end_row', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('processor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('worksheet', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('include_header', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('buffer_file', self.gf('django.db.models.fields.files.FileField')(db_index=True, max_length=100, blank=True)),
            ('dataset', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('filter_dataset', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data_action', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('mtr_sync', ['Settings'])

        # Adding model 'Field'
        db.create_table(u'mtr_sync_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('skip', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('converters', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['mtr_sync.Settings'])),
        ))
        db.send_create_signal('mtr_sync', ['Field'])

        # Adding model 'Filter'
        db.create_table(u'mtr_sync_filter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filter_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filters', to=orm['mtr_sync.Settings'])),
        ))
        db.send_create_signal('mtr_sync', ['Filter'])

        # Adding model 'Report'
        db.create_table(u'mtr_sync_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('buffer_file', self.gf('django.db.models.fields.files.FileField')(db_index=True, max_length=100, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('completed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='reports', null=True, to=orm['mtr_sync.Settings'])),
        ))
        db.send_create_signal('mtr_sync', ['Report'])

        # Adding model 'Error'
        db.create_table(u'mtr_sync_error', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='errors', to=orm['mtr_sync.Report'])),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=10000)),
            ('step', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
            ('input_position', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('input_value', self.gf('django.db.models.fields.TextField')(max_length=60000, null=True, blank=True)),
        ))
        db.send_create_signal('mtr_sync', ['Error'])


    def backwards(self, orm):
        # Deleting model 'Settings'
        db.delete_table(u'mtr_sync_settings')

        # Deleting model 'Field'
        db.delete_table(u'mtr_sync_field')

        # Deleting model 'Filter'
        db.delete_table(u'mtr_sync_filter')

        # Deleting model 'Report'
        db.delete_table(u'mtr_sync_report')

        # Deleting model 'Error'
        db.delete_table(u'mtr_sync_error')


    models = {
        'mtr_sync.error': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Error'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_position': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'input_value': ('django.db.models.fields.TextField', [], {'max_length': '60000', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'errors'", 'to': "orm['mtr_sync.Report']"}),
            'step': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'})
        },
        'mtr_sync.field': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Field'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'converters': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': "orm['mtr_sync.Settings']"}),
            'skip': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mtr_sync.filter': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Filter'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filter_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filters'", 'to': "orm['mtr_sync.Settings']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mtr_sync.report': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Report'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'buffer_file': ('django.db.models.fields.files.FileField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'completed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reports'", 'null': 'True', 'to': "orm['mtr_sync.Settings']"}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'mtr_sync.settings': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Settings'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'}),
            'buffer_file': ('django.db.models.fields.files.FileField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_action': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end_col': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'end_row': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'filter_dataset': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_header': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'processor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_col': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'start_row': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'worksheet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['mtr_sync']