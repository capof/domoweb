# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GraphEngine'
        db.create_table('domoweb_graphengine', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('domoweb', ['GraphEngine'])

        # Adding model 'GraphEngineCSS'
        db.create_table('domoweb_graphenginecss', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graphengine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.GraphEngine'])),
            ('src', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('media', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('domoweb', ['GraphEngineCSS'])

        # Adding model 'GraphEngineJS'
        db.create_table('domoweb_graphenginejs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graphengine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.GraphEngine'])),
            ('src', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('domoweb', ['GraphEngineJS'])


    def backwards(self, orm):
        # Deleting model 'GraphEngine'
        db.delete_table('domoweb_graphengine')

        # Deleting model 'GraphEngineCSS'
        db.delete_table('domoweb_graphenginecss')

        # Deleting model 'GraphEngineJS'
        db.delete_table('domoweb_graphenginejs')


    models = {
        'domoweb.graphengine': {
            'Meta': {'object_name': 'GraphEngine'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.graphenginecss': {
            'Meta': {'object_name': 'GraphEngineCSS'},
            'graphengine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.GraphEngine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'src': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'domoweb.graphenginejs': {
            'Meta': {'object_name': 'GraphEngineJS'},
            'graphengine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.GraphEngine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'domoweb.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'theme_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'domoweb.pageicon': {
            'Meta': {'object_name': 'PageIcon'},
            'icon_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'iconset_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'iconset_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.pagetheme': {
            'Meta': {'object_name': 'PageTheme'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'domoweb.widget': {
            'Meta': {'object_name': 'Widget'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        'domoweb.widgetinstance': {
            'Meta': {'object_name': 'WidgetInstance'},
            'feature_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'page_id': ('django.db.models.fields.IntegerField', [], {}),
            'widget_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['domoweb']