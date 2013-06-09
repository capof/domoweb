# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WidgetInstanceSensor'
        db.create_table('domoweb_widgetinstancesensor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Sensor'], on_delete=models.DO_NOTHING)),
        ))
        db.send_create_signal('domoweb', ['WidgetInstanceSensor'])

        # Adding model 'WidgetInstanceCommand'
        db.create_table('domoweb_widgetinstancecommand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Command'], on_delete=models.DO_NOTHING)),
        ))
        db.send_create_signal('domoweb', ['WidgetInstanceCommand'])

        # Adding model 'Sensor'
        db.create_table('domoweb_sensor', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Device'])),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datatype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.DataType'], on_delete=models.DO_NOTHING)),
            ('last_value', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_received', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('domoweb', ['Sensor'])

        # Adding model 'DataType'
        db.create_table('domoweb_datatype', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('parameters', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('domoweb', ['DataType'])

        # Adding model 'XPLCmd'
        db.create_table('domoweb_xplcmd', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('device_id', self.gf('django.db.models.fields.IntegerField')()),
            ('json_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('domoweb', ['XPLCmd'])

        # Adding model 'XPLStat'
        db.create_table('domoweb_xplstat', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('device_id', self.gf('django.db.models.fields.IntegerField')()),
            ('json_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('domoweb', ['XPLStat'])

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

        # Adding model 'WidgetCSS'
        db.create_table('domoweb_widgetcss', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
        ))
        db.send_create_signal('domoweb', ['WidgetCSS'])

        # Adding model 'WidgetJS'
        db.create_table('domoweb_widgetjs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
        ))
        db.send_create_signal('domoweb', ['WidgetJS'])

        # Adding model 'CommandParam'
        db.create_table('domoweb_commandparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Command'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datatype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.DataType'], on_delete=models.DO_NOTHING)),
        ))
        db.send_create_signal('domoweb', ['CommandParam'])

        # Adding model 'Command'
        db.create_table('domoweb_command', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Device'])),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('return_confirmation', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('domoweb', ['Command'])

        # Adding model 'Device'
        db.create_table('domoweb_device', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.DeviceType'], null=True, on_delete=models.DO_NOTHING, blank=True)),
        ))
        db.send_create_signal('domoweb', ['Device'])

        # Adding model 'WidgetSensorParameter'
        db.create_table('domoweb_widgetsensorparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('types', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filters', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('domoweb', ['WidgetSensorParameter'])

        # Adding model 'DeviceType'
        db.create_table('domoweb_devicetype', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('plugin_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('domoweb', ['DeviceType'])

        # Adding model 'WidgetCommandParameter'
        db.create_table('domoweb_widgetcommandparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('types', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filters', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('domoweb', ['WidgetCommandParameter'])

        # Adding model 'WidgetInstanceParam'
        db.create_table('domoweb_widgetinstanceparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('domoweb', ['WidgetInstanceParam'])

        # Adding field 'Widget.version'
        db.add_column('domoweb_widget', 'version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.set_id'
        db.add_column('domoweb_widget', 'set_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.set_name'
        db.add_column('domoweb_widget', 'set_name',
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

        # Adding field 'Widget.template'
        db.add_column('domoweb_widget', 'template',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'WidgetInstance.feature_id'
        db.delete_column('domoweb_widgetinstance', 'feature_id')


    def backwards(self, orm):
        # Deleting model 'WidgetInstanceSensor'
        db.delete_table('domoweb_widgetinstancesensor')

        # Deleting model 'WidgetInstanceCommand'
        db.delete_table('domoweb_widgetinstancecommand')

        # Deleting model 'Sensor'
        db.delete_table('domoweb_sensor')

        # Deleting model 'DataType'
        db.delete_table('domoweb_datatype')

        # Deleting model 'XPLCmd'
        db.delete_table('domoweb_xplcmd')

        # Deleting model 'XPLStat'
        db.delete_table('domoweb_xplstat')

        # Deleting model 'WidgetParameter'
        db.delete_table('domoweb_widgetparameter')

        # Deleting model 'WidgetCSS'
        db.delete_table('domoweb_widgetcss')

        # Deleting model 'WidgetJS'
        db.delete_table('domoweb_widgetjs')

        # Deleting model 'CommandParam'
        db.delete_table('domoweb_commandparam')

        # Deleting model 'Command'
        db.delete_table('domoweb_command')

        # Deleting model 'Device'
        db.delete_table('domoweb_device')

        # Deleting model 'WidgetSensorParameter'
        db.delete_table('domoweb_widgetsensorparameter')

        # Deleting model 'DeviceType'
        db.delete_table('domoweb_devicetype')

        # Deleting model 'WidgetCommandParameter'
        db.delete_table('domoweb_widgetcommandparameter')

        # Deleting model 'WidgetInstanceParam'
        db.delete_table('domoweb_widgetinstanceparam')

        # Deleting field 'Widget.version'
        db.delete_column('domoweb_widget', 'version')

        # Deleting field 'Widget.set_id'
        db.delete_column('domoweb_widget', 'set_id')

        # Deleting field 'Widget.set_name'
        db.delete_column('domoweb_widget', 'set_name')

        # Deleting field 'Widget.name'
        db.delete_column('domoweb_widget', 'name')

        # Deleting field 'Widget.height'
        db.delete_column('domoweb_widget', 'height')

        # Deleting field 'Widget.width'
        db.delete_column('domoweb_widget', 'width')

        # Deleting field 'Widget.template'
        db.delete_column('domoweb_widget', 'template')

        # Adding field 'WidgetInstance.feature_id'
        db.add_column('domoweb_widgetinstance', 'feature_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        'domoweb.command': {
            'Meta': {'object_name': 'Command'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Device']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'return_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'domoweb.commandparam': {
            'Meta': {'object_name': 'CommandParam'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Command']"}),
            'datatype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.DataType']", 'on_delete': 'models.DO_NOTHING'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.datatype': {
            'Meta': {'object_name': 'DataType'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {})
        },
        'domoweb.device': {
            'Meta': {'object_name': 'Device'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.DeviceType']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'})
        },
        'domoweb.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'plugin_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
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
        'domoweb.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'datatype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.DataType']", 'on_delete': 'models.DO_NOTHING'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Device']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_received': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'last_value': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.widget': {
            'Meta': {'object_name': 'Widget'},
            'height': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'set_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'set_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'domoweb.widgetcommandparameter': {
            'Meta': {'object_name': 'WidgetCommandParameter'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Widget']"})
        },
        'domoweb.widgetcss': {
            'Meta': {'object_name': 'WidgetCSS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Widget']"})
        },
        'domoweb.widgetinstance': {
            'Meta': {'object_name': 'WidgetInstance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Page']"}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Widget']", 'on_delete': 'models.DO_NOTHING'})
        },
        'domoweb.widgetinstancecommand': {
            'Meta': {'object_name': 'WidgetInstanceCommand'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Command']", 'on_delete': 'models.DO_NOTHING'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.WidgetInstance']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.widgetinstanceparam': {
            'Meta': {'object_name': 'WidgetInstanceParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.WidgetInstance']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.widgetinstancesensor': {
            'Meta': {'object_name': 'WidgetInstanceSensor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.WidgetInstance']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Sensor']", 'on_delete': 'models.DO_NOTHING'})
        },
        'domoweb.widgetjs': {
            'Meta': {'object_name': 'WidgetJS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Widget']"})
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
        },
        'domoweb.widgetsensorparameter': {
            'Meta': {'object_name': 'WidgetSensorParameter'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['domoweb.Widget']"})
        },
        'domoweb.xplcmd': {
            'Meta': {'object_name': 'XPLCmd'},
            'device_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'json_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'domoweb.xplstat': {
            'Meta': {'object_name': 'XPLStat'},
            'device_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'json_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['domoweb']