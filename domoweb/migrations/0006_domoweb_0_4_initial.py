# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WidgetInstanceSensor'
        db.create_table(u'domoweb_widgetinstancesensor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetSensor'], on_delete=models.DO_NOTHING)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Sensor'], on_delete=models.DO_NOTHING)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetInstanceSensor'])

        # Adding model 'WidgetInstanceCommand'
        db.create_table(u'domoweb_widgetinstancecommand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetCommand'], on_delete=models.DO_NOTHING)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Command'], on_delete=models.DO_NOTHING)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetInstanceCommand'])

        # Adding model 'WidgetCSS'
        db.create_table(u'domoweb_widgetcss', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
        ))
        db.send_create_signal(u'domoweb', ['WidgetCSS'])

        # Adding model 'WidgetDevice'
        db.create_table(u'domoweb_widgetdevice', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('types', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetDevice'])

        # Adding model 'Sensor'
        db.create_table(u'domoweb_sensor', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Device'])),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datatype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.DataType'], on_delete=models.DO_NOTHING)),
            ('last_value', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_received', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'domoweb', ['Sensor'])

        # Adding model 'DataType'
        db.create_table(u'domoweb_datatype', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('parameters', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'domoweb', ['DataType'])

        # Adding model 'XPLCmd'
        db.create_table(u'domoweb_xplcmd', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('device_id', self.gf('django.db.models.fields.IntegerField')()),
            ('json_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'domoweb', ['XPLCmd'])

        # Adding model 'XPLStat'
        db.create_table(u'domoweb_xplstat', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('device_id', self.gf('django.db.models.fields.IntegerField')()),
            ('json_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'domoweb', ['XPLStat'])

        # Adding model 'WidgetInstanceOption'
        db.create_table(u'domoweb_widgetinstanceoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetOption'], on_delete=models.DO_NOTHING)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetInstanceOption'])

        # Adding model 'WidgetSensor'
        db.create_table(u'domoweb_widgetsensor', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('types', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filters', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetSensor'])

        # Adding model 'WidgetJS'
        db.create_table(u'domoweb_widgetjs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
        ))
        db.send_create_signal(u'domoweb', ['WidgetJS'])

        # Adding model 'CommandParam'
        db.create_table(u'domoweb_commandparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Command'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datatype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.DataType'], on_delete=models.DO_NOTHING)),
        ))
        db.send_create_signal(u'domoweb', ['CommandParam'])

        # Adding model 'Command'
        db.create_table(u'domoweb_command', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Device'])),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('return_confirmation', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('datatypes', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'domoweb', ['Command'])

        # Adding model 'Device'
        db.create_table(u'domoweb_device', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.DeviceType'], null=True, on_delete=models.DO_NOTHING, blank=True)),
        ))
        db.send_create_signal(u'domoweb', ['Device'])

        # Adding model 'WidgetOption'
        db.create_table(u'domoweb_widgetoption', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('options', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetOption'])

        # Adding model 'DeviceType'
        db.create_table(u'domoweb_devicetype', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('plugin_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'domoweb', ['DeviceType'])

        # Adding model 'WidgetInstanceDevice'
        db.create_table(u'domoweb_widgetinstancedevice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetInstance'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.WidgetDevice'], on_delete=models.DO_NOTHING)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Device'], on_delete=models.DO_NOTHING)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetInstanceDevice'])

        # Adding model 'WidgetCommand'
        db.create_table(u'domoweb_widgetcommand', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domoweb.Widget'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('types', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filters', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'domoweb', ['WidgetCommand'])

        # Adding field 'Widget.version'
        db.add_column(u'domoweb_widget', 'version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.set_id'
        db.add_column(u'domoweb_widget', 'set_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.set_name'
        db.add_column(u'domoweb_widget', 'set_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.name'
        db.add_column(u'domoweb_widget', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Widget.height'
        db.add_column(u'domoweb_widget', 'height',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Widget.width'
        db.add_column(u'domoweb_widget', 'width',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Widget.template'
        db.add_column(u'domoweb_widget', 'template',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'WidgetInstance.feature_id'
        db.delete_column(u'domoweb_widgetinstance', 'feature_id')

        # Deleting field 'WidgetInstance.order'
        db.delete_column(u'domoweb_widgetinstance', 'order')

        # Adding field 'WidgetInstance.row'
        db.add_column(u'domoweb_widgetinstance', 'row',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'WidgetInstance.col'
        db.add_column(u'domoweb_widgetinstance', 'col',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'WidgetInstance.configured'
        db.add_column(u'domoweb_widgetinstance', 'configured',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'WidgetInstanceSensor'
        db.delete_table(u'domoweb_widgetinstancesensor')

        # Deleting model 'WidgetInstanceCommand'
        db.delete_table(u'domoweb_widgetinstancecommand')

        # Deleting model 'WidgetCSS'
        db.delete_table(u'domoweb_widgetcss')

        # Deleting model 'WidgetDevice'
        db.delete_table(u'domoweb_widgetdevice')

        # Deleting model 'Sensor'
        db.delete_table(u'domoweb_sensor')

        # Deleting model 'DataType'
        db.delete_table(u'domoweb_datatype')

        # Deleting model 'XPLCmd'
        db.delete_table(u'domoweb_xplcmd')

        # Deleting model 'XPLStat'
        db.delete_table(u'domoweb_xplstat')

        # Deleting model 'WidgetInstanceOption'
        db.delete_table(u'domoweb_widgetinstanceoption')

        # Deleting model 'WidgetSensor'
        db.delete_table(u'domoweb_widgetsensor')

        # Deleting model 'WidgetJS'
        db.delete_table(u'domoweb_widgetjs')

        # Deleting model 'CommandParam'
        db.delete_table(u'domoweb_commandparam')

        # Deleting model 'Command'
        db.delete_table(u'domoweb_command')

        # Deleting model 'Device'
        db.delete_table(u'domoweb_device')

        # Deleting model 'WidgetOption'
        db.delete_table(u'domoweb_widgetoption')

        # Deleting model 'DeviceType'
        db.delete_table(u'domoweb_devicetype')

        # Deleting model 'WidgetInstanceDevice'
        db.delete_table(u'domoweb_widgetinstancedevice')

        # Deleting model 'WidgetCommand'
        db.delete_table(u'domoweb_widgetcommand')

        # Deleting field 'Widget.version'
        db.delete_column(u'domoweb_widget', 'version')

        # Deleting field 'Widget.set_id'
        db.delete_column(u'domoweb_widget', 'set_id')

        # Deleting field 'Widget.set_name'
        db.delete_column(u'domoweb_widget', 'set_name')

        # Deleting field 'Widget.name'
        db.delete_column(u'domoweb_widget', 'name')

        # Deleting field 'Widget.height'
        db.delete_column(u'domoweb_widget', 'height')

        # Deleting field 'Widget.width'
        db.delete_column(u'domoweb_widget', 'width')

        # Deleting field 'Widget.template'
        db.delete_column(u'domoweb_widget', 'template')

        # Adding field 'WidgetInstance.feature_id'
        db.add_column(u'domoweb_widgetinstance', 'feature_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'WidgetInstance.order'
        db.add_column(u'domoweb_widgetinstance', 'order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'WidgetInstance.row'
        db.delete_column(u'domoweb_widgetinstance', 'row')

        # Deleting field 'WidgetInstance.col'
        db.delete_column(u'domoweb_widgetinstance', 'col')

        # Deleting field 'WidgetInstance.configured'
        db.delete_column(u'domoweb_widgetinstance', 'configured')


    models = {
        u'domoweb.command': {
            'Meta': {'object_name': 'Command'},
            'datatypes': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Device']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'return_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'domoweb.commandparam': {
            'Meta': {'object_name': 'CommandParam'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Command']"}),
            'datatype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.DataType']", 'on_delete': 'models.DO_NOTHING'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'domoweb.datatype': {
            'Meta': {'object_name': 'DataType'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {})
        },
        u'domoweb.device': {
            'Meta': {'object_name': 'Device'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.DeviceType']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'})
        },
        u'domoweb.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'plugin_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'domoweb.page': {
            'Meta': {'object_name': 'Page'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.PageIcon']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'right': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.PageTheme']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'})
        },
        u'domoweb.pageicon': {
            'Meta': {'object_name': 'PageIcon'},
            'icon_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'iconset_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'iconset_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'domoweb.pagetheme': {
            'Meta': {'object_name': 'PageTheme'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'domoweb.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'domoweb.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'datatype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.DataType']", 'on_delete': 'models.DO_NOTHING'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Device']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_received': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'last_value': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'domoweb.widget': {
            'Meta': {'object_name': 'Widget'},
            'height': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'set_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'set_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'domoweb.widgetcommand': {
            'Meta': {'object_name': 'WidgetCommand'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Widget']"})
        },
        u'domoweb.widgetcss': {
            'Meta': {'object_name': 'WidgetCSS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Widget']"})
        },
        u'domoweb.widgetdevice': {
            'Meta': {'object_name': 'WidgetDevice'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Widget']"})
        },
        u'domoweb.widgetinstance': {
            'Meta': {'object_name': 'WidgetInstance'},
            'col': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'configured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Page']"}),
            'row': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Widget']", 'on_delete': 'models.DO_NOTHING'})
        },
        u'domoweb.widgetinstancecommand': {
            'Meta': {'object_name': 'WidgetInstanceCommand'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Command']", 'on_delete': 'models.DO_NOTHING'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetInstance']"}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetCommand']", 'on_delete': 'models.DO_NOTHING'})
        },
        u'domoweb.widgetinstancedevice': {
            'Meta': {'object_name': 'WidgetInstanceDevice'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Device']", 'on_delete': 'models.DO_NOTHING'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetInstance']"}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetDevice']", 'on_delete': 'models.DO_NOTHING'})
        },
        u'domoweb.widgetinstanceoption': {
            'Meta': {'object_name': 'WidgetInstanceOption'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetInstance']"}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetOption']", 'on_delete': 'models.DO_NOTHING'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domoweb.widgetinstancesensor': {
            'Meta': {'object_name': 'WidgetInstanceSensor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetInstance']"}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.WidgetSensor']", 'on_delete': 'models.DO_NOTHING'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Sensor']", 'on_delete': 'models.DO_NOTHING'})
        },
        u'domoweb.widgetjs': {
            'Meta': {'object_name': 'WidgetJS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Widget']"})
        },
        u'domoweb.widgetoption': {
            'Meta': {'object_name': 'WidgetOption'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Widget']"})
        },
        u'domoweb.widgetsensor': {
            'Meta': {'object_name': 'WidgetSensor'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domoweb.Widget']"})
        },
        u'domoweb.xplcmd': {
            'Meta': {'object_name': 'XPLCmd'},
            'device_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'json_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'domoweb.xplstat': {
            'Meta': {'object_name': 'XPLStat'},
            'device_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'json_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['domoweb']