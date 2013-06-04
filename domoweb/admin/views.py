#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Module purpose
==============

Django web UI views

Implements
==========


@author: Domogik project
@copyright: (C) 2007-2010 Domogik project
@license: GPL(v3)
@organization: Domogik
"""
import urllib
import urllib2
import pyinfo
import mimetypes
import django_tables2 as tables
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.contrib import messages
from django.conf import settings
from django import forms
from django.forms.widgets import Select
from domoweb.utils import *
from domoweb.rinor.pipes import *
from domoweb.exceptions import RinorError, RinorNotConfigured
from domoweb.models import Parameter, Widget, PageIcon, WidgetInstance, WidgetInstanceParam, WidgetInstanceSensor, WidgetInstanceCommand, PageTheme, Page, DataType, DeviceType, Device, Command, CommandParam, Sensor
from domoweb.models import Parameter, Widget, WidgetParameter, WidgetSensorParameter, WidgetCommandParameter, PageIcon, WidgetInstance, WidgetInstanceParam, WidgetInstanceSensor, WidgetInstanceCommand, PageTheme, Page, DeviceType, DeviceUsage, Device, Command, CommandParam, Sensor

def login(request):
    """
    Login process
    @param request : HTTP request
    @return an HttpResponse object
    """
    next = request.GET.get('next', '')

    page_title = _("Login page")
    if request.method == 'POST':
        return _auth(request, next)
    else:
        users = UserPipe().get_list()
        return go_to_page(
            request, 'login.html',
            page_title,
            next=next,
            account_list=users
        )

def logout(request):
    """
    Logout process
    @param request: HTTP request
    @return an HttpResponse object
    """
    next = request.GET.get('next', '')

    request.session.clear()
    if next != '':
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/')


def _auth(request, next):
    # An action was submitted => login action
    user_login = request.POST.get("login",'')
    user_password = request.POST.get("password",'')
    try:
        account = UserPipe().get_auth(user_login, user_password)
        request.session['user'] = {
            'login': account.login,
            'is_admin': (account.is_admin == "True"),
            'first_name': account.person.first_name,
            'last_name': account.person.last_name,
            'skin_used': account.skin_used
        }
        if next != '':
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/')

    except RinorError:
        # User not found, ask again to log in
        error_msg = ugettext(u"Sorry unable to log in. Please check login name / password and try again.")
        return HttpResponseRedirect('%s/?status=error&msg=%s' % (settings.LOGIN_URL, error_msg))


@admin_required
def admin_management_accounts(request):
    """
    Method called when the admin accounts page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """
    
    page_title = _("Accounts management")
    users = UserPipe().get_list()
    people = PersonPipe().get_list()
    return go_to_page(
        request, 'management/accounts.html',
        page_title,
        nav1_admin = "selected",
        nav2_management_accounts = "selected",
        accounts_list=users,
        people_list=people
    )

@admin_required
def admin_organization_pages(request):
    """
    Method called when the admin pages organization page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Pages organization")

    id = request.GET.get('id', 0)
    pages = Page.objects.get_tree()

    return go_to_page(
        request, 'organization/pages.html',
        page_title,
        nav1_admin = "selected",
        nav2_organization_pages = "selected",
        id=id,
        pages_list=pages
    )

@admin_required
def admin_plugins_plugin(request, plugin_host, plugin_id, plugin_type):
    """
    Method called when the admin plugin command page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    plugin = PluginPipe().get_detail(plugin_host, plugin_id)
    devices = Device.objects.filter(type__plugin_id=plugin.id)
    types = DeviceType.objects.filter(plugin_id=plugin.id)

    if plugin_id == "rfxcom-lan":
        products = ProductsPipe().get_list("rfxcom")
    else:
        products = ProductsPipe().get_list(plugin_id)

    if plugin_type == "plugin":
        page_title = _("Plugin")
        dependencies = PluginDependencyPipe().get_list(plugin_host, plugin_id)
        udevrules = PluginUdevrulePipe().get_list(plugin_host, plugin_id)
        return go_to_page(
            request, 'plugins/plugin.html',
            page_title,
            nav1_admin = "selected",
            nav2_plugins_plugin = "selected",
            plugin=plugin,
            plugin_type=plugin_type,
            dependencies=dependencies,
            udevrules=udevrules,
            devices_list=devices,
            types_list=types,
	    product_list=products,
        )
    if plugin_type == "external":
        page_title = _("External Member")
        return go_to_page(
            request, 'plugins/external.html',
            page_title,
            nav1_admin = "selected",
            nav2_plugins_plugin = "selected",
            plugin=plugin,
            plugin_type=plugin_type,
            devices_list=devices,
            types_list=types,
	    product_list=products,
        )

class SelectIcon(Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        class_html = ' class="icon16-usage-%s"' % option_value
        if option_value in selected_choices:
            selected_html = ' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return '<option value="%s"%s%s>%s</option>' % (
            escape(option_value), selected_html, class_html,
            conditional_escape(force_unicode(option_label)))

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
    
class DeviceForm(forms.Form):
    name = forms.CharField(max_length=50, label=_("Name"), required=True)
    reference = forms.CharField(max_length=50, label=_("Hardware/Software Reference"), required=False)
    type_id = forms.CharField(widget=forms.HiddenInput, required=True)

    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(DeviceForm, self).__init__(*args, **kwargs)

   
class ParametersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', None)
        self.id = kwargs.pop('id', None)
        self.params = kwargs.pop('params', None)
        self.prefix = kwargs.pop('prefix', None)
        kwargs['auto_id'] = '%s'
        # This should be done before any references to self.fields
        super(ParametersForm, self).__init__(*args, **kwargs)
        if self.params:
            for parameter in self.params:
                self.addCharField(('%s-%s-%s')%(self.prefix, self.id, parameter.key), parameter.description, required=True)

    def addCharField(self, key, label, required=False, max_length=50):
        self.fields[key] = forms.CharField(label=label, required=required, max_length=max_length)

    def setData(self, kwds):
        """Set the data to include in the form"""
        for name,field in self.fields.items():
            self.data[name] = field.widget.value_from_datadict(
                                kwds, self.files, self.add_prefix(name))
        self.is_bound = True

    def validate(self): self.full_clean()

    def getData(self):
        data = {}
        for key, cd in self.cleaned_data.items():
            key = key.replace(('%s-%s-')%(self.prefix, self.id), "")
            data[key] = cd
        return data
    
@admin_required
def admin_add_device(request, plugin_host, plugin_id, plugin_type, type_id):
    page_title = _("Add device")
    parameters = DeviceParametersPipe().get_detail(type_id)

    globalparametersform = None
    if parameters["global"] :
        globalparametersform = ParametersForm(auto_id='global_%s')
        for parameter in parameters["global"]:
            globalparametersform.addCharField(parameter.key, parameter.description, required=True)

    commands = []
    hasscommandsparamters = 0
    for command in parameters["xpl_cmd"]:
        form = ParametersForm(id=command.id, name=command.name, params=command.params, prefix='cmd')
        commands.append(form)
        if command.params:
            hasscommandsparamters = 1

    stats = []
    hasstatsparamters = 0
    for stat in parameters["xpl_stat"]:
        form = ParametersForm(id=stat.id, name=stat.name, params=stat.params, prefix='stat')
        stats.append(form)
        if stat.params:
            hasstatsparamters = 1

    if request.method == 'POST':
        valid = True
        deviceform = DeviceForm(request.POST) # A form bound to the POST data
        valid = valid and deviceform.is_valid()
        if globalparametersform:
            globalparametersform.setData(request.POST)
            globalparametersform.validate()
            valid = valid and globalparametersform.is_valid()
        for command in commands:
            command.setData(request.POST)
            command.validate()
            valid = valid and command.is_valid()
        for stat in stats:
            stat.setData(request.POST)
            stat.validate()
            valid = valid and stat.is_valid()
        if valid:
            cd = deviceform.cleaned_data
            device = Device.create(cd["name"], cd["type_id"], cd["reference"])
            if globalparametersform:
                device.add_global_params(parameters=globalparametersform.cleaned_data)
            for command in commands:
                if command.params:
                    device.add_xplcmd_params(id=command.id, parameters=command.getData())
            for stat in stats:
                if stat.params:
                    device.add_xplstat_params(id=stat.id, parameters=stat.getData())
            return redirect('admin_plugins_plugin_view', plugin_host=plugin_host, plugin_id=plugin_id, plugin_type=plugin_type) # Redirect after POST
    else:
        deviceform = DeviceForm(auto_id='main_%s', initial={'type_id': type_id})

    return go_to_page(
        request, 'plugins/device.html',
        page_title,
        plugin_host=plugin_host,
        plugin_id=plugin_id,
        plugin_type=plugin_type,
        deviceform=deviceform,
        globalparametersform=globalparametersform,
        hasscommansparamters=hasscommandsparamters,
        hasstatsparamters=hasstatsparamters,
        commands=commands,
        stats=stats,
    )

@admin_required
def admin_del_device(request, device_id, plugin_host, plugin_id, plugin_type):
    Device.objects.get(id=device_id).delete()
    return redirect('admin_plugins_plugin_view', plugin_host=plugin_host, plugin_id=plugin_id, plugin_type=plugin_type) # Redirect after POST

@admin_required
def admin_core_helpers(request):
    """
    Method called when the admin helpers tool page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Helpers tools")

    return go_to_page(
        request, 'core/helpers.html',
        page_title,
        nav1_admin = "selected",
        nav2_core_helpers = "selected",
    )


@admin_required
def admin_core_rinor(request):
    """
    Method called when the admin Python Info page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("RINOR informations")

    info = InfoPipe().get_info()
    hosts = HostPipe().get_list()
    host = ''
    for h in hosts:
        if h.primary == 'True':
            host = h.id
    return go_to_page(
        request, 'core/rinor.html',
        page_title,
        nav1_admin = "selected",
        nav2_core_rinor = "selected",
        rinor=info,
        host=host
    )


@admin_required
def admin_core_pyinfo(request):
    """
    Method called when the admin Python info page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Python informations")
    
    return go_to_page(
        request, 'core/pyinfo.html',
        page_title,
        nav1_admin = "selected",
        nav2_core_pyinfo = "selected",
        pyinfo=pyinfo.foo.fullText()
    )
    
HIDDEN_SETTINGS = re.compile('SECRET|PASSWORD|PROFANITIES_LIST|SIGNATURE')
CLEANSED_SUBSTITUTE = u'********************'

def cleanse_setting(key, value):
    """Cleanse an individual setting key/value of sensitive content.

    If the value is a dictionary, recursively cleanse the keys in
    that dictionary.
    """
    try:
        if HIDDEN_SETTINGS.search(key):
            cleansed = CLEANSED_SUBSTITUTE
        else:
            if isinstance(value, dict):
                cleansed = dict((k, cleanse_setting(k, v)) for k,v in value.items())
            else:
                cleansed = value
    except TypeError:
        # If the key isn't regex-able, just return as-is.
        cleansed = value
    return cleansed

def get_safe_settings():
    "Returns a dictionary of the settings module, with sensitive settings blurred out."
    settings_dict = {}
    for k in dir(settings):
        if k.isupper():
            settings_dict[k] = cleanse_setting(k, getattr(settings, k))
    return settings_dict


@admin_required
def admin_core_djangoinfo(request):
    """
    Method called when the admin Django Info page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """
    from django import get_version
    import sys
    
    page_title = _("Django informations")
    
    return go_to_page(
        request, 'core/djangoinfo.html',
        page_title,
        nav1_admin = "selected",
        nav2_core_djangoinfo = "selected",
        settings=get_safe_settings(),
        sys_executable=sys.executable,
        sys_version_info='%d.%d.%d' % sys.version_info[0:3],
        django_version_info=get_version(),
        sys_path=sys.path,
    )

class WidgetTable(tables.Table):
    class Meta:
        model = Widget

class WidgetParameterTable(tables.Table):
    class Meta:
        model = WidgetParameter

class WidgetSensorParameterTable(tables.Table):
    class Meta:
        model = WidgetSensorParameter

class WidgetCommandParameterTable(tables.Table):
    class Meta:
        model = WidgetCommandParameter

class ParameterTable(tables.Table):
    class Meta:
        model = Parameter

class PageIconTable(tables.Table):
    class Meta:
        model = PageIcon

class WidgetInstanceTable(tables.Table):
    class Meta:
        model = WidgetInstance

class WidgetInstanceParamTable(tables.Table):
    class Meta:
        model = WidgetInstanceParam

class WidgetInstanceSensorTable(tables.Table):
    class Meta:
        model = WidgetInstanceSensor

class WidgetInstanceCommandTable(tables.Table):
    class Meta:
        model = WidgetInstanceCommand

class PageThemeTable(tables.Table):
    class Meta:
        model = PageTheme

class PageTable(tables.Table):
    class Meta:
        model = Page

class DeviceTable(tables.Table):
    class Meta:
        model = Device

class DeviceTypeTable(tables.Table):
    class Meta:
        model = DeviceType

class DataTypeTable(tables.Table):
    class Meta:
        model = DataType

class CommandTable(tables.Table):
    class Meta:
        model = Command

class CommandParamTable(tables.Table):
    class Meta:
        model = CommandParam

class SensorTable(tables.Table):
    class Meta:
        model = Sensor
 
@admin_required
def admin_core_domowebdata(request):
    """
    Method called when the admin Domoweb Data page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """
    
    page_title = _("Domoweb Data")
    
    widget_table = WidgetTable(Widget.objects.all())
    widgetparameter_table = WidgetParameterTable(WidgetParameter.objects.all())
    widgetsensorparameter_table = WidgetSensorParameterTable(WidgetSensorParameter.objects.all())
    widgetcommandparameter_table = WidgetCommandParameterTable(WidgetCommandParameter.objects.all())
    parameter_table = ParameterTable(Parameter.objects.all())
    pageicon_table = PageIconTable(PageIcon.objects.all())
    widgetinstance_table = WidgetInstanceTable(WidgetInstance.objects.all())
    widgetinstanceparam_table = WidgetInstanceParamTable(WidgetInstanceParam.objects.all())
    widgetinstancesensor_table = WidgetInstanceSensorTable(WidgetInstanceSensor.objects.all())
    widgetinstancecommand_table = WidgetInstanceCommandTable(WidgetInstanceCommand.objects.all())
    pagetheme_table = PageThemeTable(PageTheme.objects.all())
    page_table = PageTable(Page.objects.all())
    device_table = DeviceTable(Device.objects.all())
    devicetype_table = DeviceTypeTable(DeviceType.objects.all())
    datatype_table = DataTypeTable(DataType.objects.all())
    command_table = CommandTable(Command.objects.all())
    commandparam_table = CommandParamTable(CommandParam.objects.all())
    sensor_table = SensorTable(Sensor.objects.all())
    
    return go_to_page(
        request, 'core/domowebdata.html',
        page_title,
        nav1_admin = "selected",
        nav2_core_domowebdata = "selected",
        parameter_table = parameter_table,
        widget_table = widget_table,
        widgetparameter_table = widgetparameter_table,
        widgetsensorparameter_table = widgetsensorparameter_table,
        widgetcommandparameter_table = widgetcommandparameter_table,
        pageicon_table = pageicon_table,
        widgetinstance_table = widgetinstance_table,
        widgetinstanceparam_table = widgetinstanceparam_table,
        widgetinstancesensor_table = widgetinstancesensor_table,
        widgetinstancecommand_table = widgetinstancecommand_table,
        pagetheme_table = pagetheme_table,
        page_table = page_table,
        device_table = device_table,
        devicetype_table = devicetype_table,
        datatype_table = datatype_table,
        command_table = command_table,
        commandparam_table = commandparam_table,
        sensor_table = sensor_table,
    )
    
@admin_required
def admin_host(request, id):
    """
    Method called when the admin plugins page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    host = HostPipe().get_detail(id)
    repositories = RepositoryPipe().get_list()
        
    page_title = _("Host %s" % id)
    
    return go_to_page(
        request, 'hosts/host.html',
        page_title,
        nav1_admin = "selected",
        nav2_hosts_host = "selected",
        repositories=repositories,
        id=id,
        host=host
    )

@admin_required
def admin_resource_icon_package_installed(request, type, id):
    try:
        ip = Parameter.objects.get(key='rinor_ip')
        port = Parameter.objects.get(key='rinor_port')
    except Parameter.DoesNotExist:
        raise RinorNotConfigured
    else:
        try:
            prefix = Parameter.objects.get(key='rinor_prefix')
        except Parameter.DoesNotExist:
            uri = "http://%s:%s/package/icon/installed/%s/%s" % (ip.value, port.value, type, id)
        else:
            uri = "http://%s:%s/%s/package/icon/installed/%s/%s" % (ip.value, port.value, prefix.value, type, id)

    contents = urllib2.urlopen(uri).read()
    mimetype = mimetypes.guess_type(uri)
    response = HttpResponse(contents, mimetype=mimetype)
    return response

@admin_required
def admin_resource_icon_package_available(request, type, id, version):
    try:
        ip = Parameter.objects.get(key='rinor_ip')
        port = Parameter.objects.get(key='rinor_port')
    except Parameter.DoesNotExist:
        raise RinorNotConfigured
    else:
        try:
            prefix = Parameter.objects.get(key='rinor_prefix')
        except Parameter.DoesNotExist:
            uri = "http://%s:%s/package/icon/available/%s/%s/%s" % (ip.value, port.value, type, id, version)
        else:
            uri = "http://%s:%s/%s/package/icon/available/%s/%s/%s" % (ip.value, port.value, prefix.value, type, id, version)

    contents = urllib2.urlopen(uri).read()
    mimetype = mimetypes.guess_type(uri)
    response = HttpResponse(contents, mimetype=mimetype)
    return response

@admin_required
def admin_core_devicesstats(request):
    """
    Method called when the admin Domoweb Data page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """
    
    page_title = _("Devices Stats Logs")
    
    devicesevents = StatePipe().get_last(100, '*', '*')
    devicesevents.reverse()
    
    return go_to_page(
        request, 'core/devicesstats.html',
        page_title,
        devicesevents_list = devicesevents,
        nav1_admin = "selected",
        nav2_core_domowebdata = "selected",
        parameter_data = Parameter.objects.all()
    )

class DeviceUpgradeForm(forms.Form):
    old = forms.ChoiceField(label=_("Old device"), required=True)
    new = forms.ChoiceField(label=_("New device"), required=True)

    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(DeviceUpgradeForm, self).__init__(*args, **kwargs)

    def clean(self):
        return super(DeviceUpgradeForm, self).clean()
 
@admin_required
def admin_core_deviceupgrade(request):
    """
    Method called when the admin Domoweb Data page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    msg = ''
    # handle the post form
    if request.method == 'POST':
        dev = Device.list_upgrade()   
        frm = DeviceUpgradeForm(request.POST)
        frm.fields['old'].choices = dev[0]['old']
        frm.fields['new'].choices = dev[0]['new']
        if frm.is_valid():
            cleaned_data = frm.clean()
            old = cleaned_data['old']
            new = cleaned_data['new']
            msg = 'post done ' + old + '  ' + new
            old = old.split('-')
            new = new.split('-')
            Device.do_upgrade(old[0], old[1], new[0], new[1])       
        else:
            msg = frm._errors
    
    # do the real output
    page_title = _("Devices Upgrade")
    dev = Device.list_upgrade()   
    frm = DeviceUpgradeForm(auto_id='main_%s')
    frm.fields['old'].choices = dev[0]['old']
    frm.fields['new'].choices = dev[0]['new']
 
    return go_to_page(
        request, 'core/deviceupgrade.html',
        page_title,
        frm = frm,
        msg = msg,
        nav1_admin = "selected",
        nav2_core_deviceupgrade = "selected",
        parameter_data = Parameter.objects.all()
    )
