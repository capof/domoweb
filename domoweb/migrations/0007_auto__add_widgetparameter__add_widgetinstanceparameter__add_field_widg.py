# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WidgetParameter'
        db.create_table('domoweb_widgetparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('domoweb', ['WidgetParameter'])

        # Adding model 'WidgetInstanceParameter'
        db.create_table('domoweb_widgetinstanceparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('domoweb', ['WidgetInstanceParameter'])

        # Adding field 'Widget.version'
        db.add_column('domoweb_widget', 'version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.package'
        db.add_column('domoweb_widget', 'package',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.name'
        db.add_column('domoweb_widget', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.height'
        db.add_column('domoweb_widget', 'height',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'Widget.width'
        db.add_column('domoweb_widget', 'width',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Deleting field 'WidgetInstance.feature_id'
        db.delete_column('domoweb_widgetinstance', 'feature_id')

        # Deleting field 'WidgetInstance.order'
        db.delete_column('domoweb_widgetinstance', 'order')


    def backwards(self, orm):
        # Deleting model 'WidgetParameter'
        db.delete_table('domoweb_widgetparameter')

        # Deleting model 'WidgetInstanceParameter'
        db.delete_table('domoweb_widgetinstanceparameter')

        # Deleting field 'Widget.version'
        db.delete_column('domoweb_widget', 'version')

        # Deleting field 'Widget.package'
        db.delete_column('domoweb_widget', 'package')

        # Deleting field 'Widget.name'
        db.delete_column('domoweb_widget', 'name')

        # Deleting field 'Widget.height'
        db.delete_column('domoweb_widget', 'height')

        # Deleting field 'Widget.width'
        db.delete_column('domoweb_widget', 'width')

        # Adding field 'WidgetInstance.feature_id'
        db.add_column('domoweb_widgetinstance', 'feature_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'WidgetInstance.order'
        db.add_column('domoweb_widgetinstance', 'order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        'domoweb.page': {
            'Meta': {'object_name': 'Page'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.PageIcon']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'right': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.PageTheme']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'})
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
            'height': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'package': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'domoweb.widgetinstance': {
            'Meta': {'object_name': 'WidgetInstance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Page']"}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Widget']", 'on_delete': 'models.DO_NOTHING'})
        },
        'domoweb.widgetinstanceparameter': {
            'Meta': {'object_name': 'WidgetInstanceParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.WidgetInstance']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'domoweb.widgetparameter': {
            'Meta': {'object_name': 'WidgetParameter'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Widget']"})
        }
    }

    complete_apps = ['domoweb']