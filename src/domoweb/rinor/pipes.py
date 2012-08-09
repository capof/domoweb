import simplejson
import cherrypy
import datetime

from distutils2.version import *
from distutils2.version import IrrationalVersionError

from django.conf import settings
from django.core.cache import cache
from domoweb.rinor.rinorPipe import RinorPipe
from domoweb.exceptions import RinorError, RinorNotConfigured
from domoweb.models import WidgetInstance, Page

def select_sublist(list_of_dicts, **kwargs):
    return [d for d in list_of_dicts 
            if all(d.get(k)==kwargs[k] for k in kwargs)]

class EventPipe(RinorPipe):
    cache_expiry = 0
    new_path = '/events/request/new'
    get_path = '/events/request/get'
    index = 'event'
    paths = []

    def get_event(self):
        yield 'event: message\ndata: {}\n\n'
        # Get all the devices ids
        try:
            _devices_list = DevicePipe().get_dict().keys()
        except RinorNotConfigured:
            today = datetime.datetime.today()
            cherrypy.log("{0} -- EVENTS : RINOR not configured yet".format(today.strftime("%Y%m%d-%H%M%S")))
        else:
            if (len(_devices_list) > 0):
                _devices = [str(id) for id in _devices_list]
                _data = self._get_data(self.new_path, _devices)               
                _event = _data.event[0]
                _ticket = _event.ticket_id
                today = datetime.datetime.today()
                cherrypy.log("{0} -- EVENTS : NEW".format(today.strftime("%Y%m%d-%H%M%S")))
                yield 'event: message\ndata: ' + simplejson.dumps(_event) + '\n\n'
                while(True):
                    _data = self._get_data(self.get_path, [_ticket])               
                    _event = _data.event[0]
                    today = datetime.datetime.today()
                    cherrypy.log("{0} -- EVENTS : RECEIVED".format(today.strftime("%Y%m%d-%H%M%S")))
                    yield 'event: message\ndata: ' + simplejson.dumps(_event) + '\n\n'        
            else:
                today = datetime.datetime.today()
                cherrypy.log("{0} -- EVENTS : No devices yet".format(today.strftime("%Y%m%d-%H%M%S")))

class InfoPipe(RinorPipe):
    cache_expiry = 0
    list_path = ""
    index = 'rest'
    paths = []

    def get_info(self):
        _data = self._get_data(self.list_path)               
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

    def get_mode(self):
        _data = self._get_data("/package/get-mode")               
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data['mode']) > 0:
            return _data['mode'][0]
        else:
            return None
    
    def get_info_extended(self):
        _data = self.get_info()
        if (_data):
            if ("REST_API_version" in _data.info):
                _data.info['rinor_version'] = _data.info.REST_API_version
            else:    
                _data.info['rinor_version'] = '0.1'

            if ("Domogik_version" in _data.info):
                _data.info['dmg_version'] = _data.info.Domogik_version
            else:
                _data.info['dmg_version'] = '0.1'             

            try:
                _data.info['rinor_version_superior'] = (NormalizedVersion(_data.info['rinor_version']) > NormalizedVersion(settings.RINOR_MAX_API))
            except IrrationalVersionError:
                _data.info['rinor_version_superior'] = False

            try:
                _data.info['rinor_version_inferior'] = (NormalizedVersion(_data.info['rinor_version']) < NormalizedVersion(settings.RINOR_MIN_API))
            except IrrationalVersionError:
                _data.info['rinor_version_inferior'] = False
            return _data
        else:
            return None

class HelperPipe(RinorPipe):
    cache_expiry = 0
    list_path = "/helper"
    index = 'helper'
    paths = []

    def get_info(self, command):
        print command
        _data = self._get_data(self.list_path, command)               
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index]

class PagePipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/base/page/list"
    add_path = "/base/page/add"
    update_path = "/base/page/update"
    delete_path = "/base/page/del"
    path_path = "/base/page/path"
    index = 'page'
    paths = []


    def put_detail(self, id, bundle):
        params = ['id', id, 'name', bundle["name"]]
        if 'description' in bundle:
            params.extend(['description', bundle["description"]])
        if 'icon' in bundle:
            params.extend(['icon', bundle["icon"]])
        _data = self._put_data(self.update_path, params)
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        else:
            # save the django params
            try:
                page = Page.objects.get(id=id)
            except Page.DoesNotExist:
                page = Page(id=id)
            if 'theme_id' in bundle:
                page.theme_id = bundle["theme_id"]
            page.save()

        return _data[self.index][0]

    def post_list(self, bundle):
        params = ['name', bundle["name"], 'parent', bundle["parent"]]
        if 'description' in bundle:
            params.extend(['description', bundle["description"]])
        if 'icon' in bundle:
            params.extend(['icon', bundle["icon"]])
        _data = self._post_data(self.add_path, params)
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        else:
            data = _data[self.index][0]
            # save the django params
            page = Page(id=data.id)
            if 'theme_id' in bundle:
                page.theme_id = bundle["theme_id"]
            page.save()
        return data
        
    def delete_detail(self, id):
        _data = self._delete_data(self.delete_path, [id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        else:
            try:
                page = Page.objects.get(id=id)
            except Page.DoesNotExist:
                pass
            else:
                page.delete()
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

    def get_list(self):
        data = self._get_data(self.list_path)
        if data.status == "ERROR":
            raise RinorError(data.code, data.description)
        pages = data[self.index]
        for page in pages:
            try:
                model = Page.objects.get(id=page.id)
            except Page.DoesNotExist:
                page.theme_id = ''
            else:
                page.theme_id = model.theme_id
        return pages
        
    def get_tree(self):
        data = self.get_list()
        _current_path = []
        top_node = None
        
        if data:
            for obj in data:
                obj.childrens = []
                obj.leafs = 0
                # If right = left + 1 then it is a leaf
                obj.is_leaf = ((obj.left + 1) == obj.right)
                if top_node == None:
                    top_node = obj
                    obj.level = 0
                    obj.max_level = 0
                    _current_path.append(obj)
                else:
                    while (obj.left > _current_path[-1].right): # Level down
                        top = _current_path.pop()
                        _current_path[-1].leafs = _current_path[-1].leafs + top.leafs
                    obj.level = len(_current_path)
                    if obj.level > top_node.max_level:
                        # Save the number of levels in the root node
                        top_node.max_level = obj.level
                    _current_path[-1].childrens.append(obj)
                    if not obj.is_leaf:
                        _current_path.append(obj) # Level up
                    else:
                        _current_path[-1].leafs = _current_path[-1].leafs + 1
            while (len(_current_path) > 1): # Level down
                top = _current_path.pop()
                _current_path[-1].leafs = _current_path[-1].leafs + top.leafs

        return top_node

    def get_path(self, id):
        url = "%s/%s" % (self.path_path, id)
        data = self._get_data(url)
        if data.status == "ERROR":
            raise RinorError(data.code, data.description)
        return data[self.index]

class DeviceTypePipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/base/device_type/list"
    index = 'device_type'
    paths = []
    dependencies = ['package']

class DeviceUsagePipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/base/device_usage/list"
    index = 'device_usage'
    paths = []
    
class DevicePipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/base/device/list"
    add_path = "/base/device/add"
    update_path = "/base/device/update"
    delete_path = "/base/device/del"
    index = 'device'
    paths = []

    def post_list(self, name, address, type_id, usage_id, description, reference):
        _data = self._post_data(self.add_path, ['name', name, 'address', address, 'type_id', type_id, 'usage_id', usage_id, 'description', description, 'reference', reference])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]

    def put_detail(self, id, name, address, usage_id, description, reference):
        _data = self._put_data(self.update_path, ['id', id, 'name', name, 'address', address, 'usage_id', usage_id, 'description', description, 'reference', reference])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]
        
    def delete_detail(self, id):
        _data = self._delete_data(self.delete_path, [id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

class FeaturePipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/base/feature/list"
    index = 'feature'
    paths = []
    dependencies = ['device']

class WidgetInstancePipe(RinorPipe):
    cache_expiry = 3600
    paths = []
    
    def get_page_list(self, id):
        instances = WidgetInstance.objects.filter(page_id=id).order_by('order')
        for instance in instances:
            instance.feature = FeaturePipe().get_pk(instance.feature_id)
        return instances
    
class DeviceExtendedPipe(RinorPipe):
    cache_expiry = 3600
    paths = []

    def get_list(self):
        _devices = DevicePipe().get_list()
        _features = FeaturePipe().get_list()
        for device in _devices:
            device['features'] = []
            for feature in _features:
                if feature.device_id == device.id:
                    device['features'].append(feature)

        return _devices

    def post_list(self, name, address, type_id, usage_id, description, reference):
        return DevicePipe().post_list(name, address, type_id, usage_id, description, reference)

    def put_detail(self, id, name, address, usage_id, description, reference):
        return DevicePipe().put_detail(id, name, address, usage_id, description, reference)

    def delete_detail(self, id):
        _features = FeaturePipe().get_list()
        for feature in _features:
            if feature.device_id == id:
                _associations = AssociationPipe().get_list('feature', feature.id)
                for association in _associations:
                    UiConfigPipe().delete_reference('association', association.id)        
                AssociationPipe().delete_feature(feature.id)
        _device = DevicePipe().delete_detail(id)
        return _device

class StatePipe(RinorPipe):
    cache_expiry = 0
    list_path = "/stats"
    index = 'stats'
    paths = []

    def get_last(self, last, device, key):
        if (last == 1):
            _data = self._get_data(self.list_path, [device, key, 'lastest'])
        else:
            _data = self._get_data(self.list_path, [device, key, 'last', last])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)        
        if len(_data[self.index]) > 0:
            return _data[self.index]                
        else:
            return None

    def get_fromto(self, fromTime, toTime, interval, selector, device, key):
        _data = self._get_data(self.list_path, [device, key, 'from', fromTime, 'to', toTime, 'interval', interval, 'selector', selector])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)        
        if len(_data[self.index]) > 0:
#            values = []
#            for value in _data[self.index][0]['values']:
#                print value
#                time = {
#                    'minute': lambda value: datetime.datetime(int(value[0]), int(value[1]), int(value[3]), int(value[4]), int(value[5])),
#                    'hour': lambda value: datetime.datetime(int(value[0]), int(value[1]), int(value[3]), int(value[4])),
#                    'day': lambda value: datetime.datetime(int(value[0]), int(value[1]), int(value[3]))
#                }[interval](value)
#                values.append(time.strftime("%s"))
                
#            _data[self.index][0]['values'] = values
            return _data[self.index][0]
        else:
            return None
        

class UserPipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/account/user/list"
    add_path = "/account/user/add"
    update_path = "/account/user/update"
    delete_path = "/account/user/del"
    password_path = "/account/user/password"
    index = 'account'
    paths = []

    def get_auth(self, login, password):
        _data = self._get_data("/account/auth", [login, password])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)        
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

    def post_list(self, login, password, is_admin, firstname, lastname):
        _data = self._post_data(self.add_path, ['login', login, 'password', password, 'is_admin', is_admin, 'skin_used', '', 'first_name', firstname, 'last_name', lastname])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]

    def put_detail(self, id, login, is_admin, firstname, lastname):
        _data = self._put_data(self.update_path, ['id', id, 'login', login, 'is_admin', is_admin, 'skin_used', '', 'first_name', firstname, 'last_name', lastname])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]

    def put_detail_password(self, id, old, new):
        _data = self._put_data(self.password_path, ['id', id, 'old', old, 'new', new])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]

    def delete_detail(self, id):
        _data = self._delete_data(self.delete_path, [id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

class PersonPipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/account/person/list"
    add_path = "/account/person/add"
    update_path = "/account/person/update"
    delete_path = "/account/person/del"
    index = 'person'
    paths = []

    def post_list(self, firstname, lastname):
        _data = self._post_data(self.add_path, ['first_name', firstname, 'last_name', lastname])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]

    def put_detail(self, id, firstname, lastname):
        _data = self._put_data(self.update_path, ['id', id, 'first_name', firstname, 'last_name', lastname])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]

    def delete_detail(self, id):
        _data = self._delete_data(self.delete_path, [id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

class PluginPipe(RinorPipe):
    cache_expiry = 0
    list_path = "/plugin/list"
    detail_path = "/plugin/detail"
    index = 'plugin'
    paths = []

    def get_detail(self, hostname, id):
        _data = self._get_data(self.detail_path, [hostname, id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

    def command_detail(self, hostname, id, command):
        _data = self._put_data("/plugin", [command, hostname, id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return None

class PluginConfigPipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/plugin/config/list"
    delete_path = "/plugin/config/del"
    set_path = "/plugin/config/set"
    index = 'config'
    paths = []

    def get_list(self, hostname, id):
        _data = self._get_data(self.list_path, ['by-name', hostname, id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index]
        else:
            return []
    
    def get_detail(self, hostname, id, key):
        _data = None
        _configs = self.get_list(hostname, id)
        if _configs:
            for _config in _configs:
                if _config.key == key:
                    _data = _config
        return _data

    def delete_list(self, hostname, id):
        _data = self._delete_data(self.delete_path, [hostname, id])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index]
        else:
            return None

    def delete_detail(self, hostname, id, key):
        _data = self._delete_data(self.delete_path, [hostname, id, 'by-key', key])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

    def set_detail(self, hostname, id, key, value):
        _data = self._put_data(self.set_path, ['hostname', hostname, 'id', id, 'key', key, 'value', value])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None

class RepositoryPipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/package/list-repo"
    index = 'repository'
    paths = []

class PackagePipe(RinorPipe):
    cache_expiry = 0
    refresh_path = "/package/update-cache"
    installed_path = "/package/installed"
    available_path = "/package/available"
    install_path = "/package/install"
    uninstall_path = "/package/uninstall"
    index = 'package'
    paths = []

    def refresh_list(self):
        _data = self._put_data(self.refresh_path)
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return None

    def get_installed(self, host, type):
        _data = self._get_data("%s/%s/%s" % (self.installed_path, host, type))
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index]

    def get_available(self, host, type):
        _data = self._get_data("%s/%s/%s" % (self.available_path, host, type))
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index]

    def put_install(self, host, type, package, release):
        _data = self._put_data(self.install_path, [host, type, package, release])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return None

    def put_uninstall(self, host, type, package):
        _data = self._put_data(self.uninstall_path, [host, type, package])
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return None

class PackageDependencyPipe(RinorPipe):
    cache_expiry = 0
    list_path = "/package/dependency"
    index = 'dependency'
    paths = []
    
    def get_list(self, host, type, id, release):
        _data = self._get_data("%s/%s/%s/%s/%s" % (self.list_path, host, type, id, release))
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index]

class PluginDependencyPipe(RinorPipe):
    cache_expiry = 0
    list_path = "/plugin/dependency"
    index = 'dependency'
    paths = []
    
    def get_list(self, host, id):
        _data = self._get_data("%s/%s/%s" % (self.list_path, host, id))
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index]

class PluginUdevrulePipe(RinorPipe):
    cache_expiry = 0
    list_path = "/plugin/udev-rule"
    index = 'udev-rule'
    paths = []
    
    def get_list(self, host, id):
        _data = self._get_data("%s/%s/%s" % (self.list_path, host, id))
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index]
        
class CommandPipe(RinorPipe):
    cache_expiry = 0
    update_path = "/command"
    index = 'response'
    paths = []

    def put_detail(self, member, address, command, value=None):
        if (command and len(command) > 0):
            if (value): 
                _data = self._put_data(self.update_path, [member, address, command, value])
            else:
                _data = self._put_data(self.update_path, [member, address, command])
        else: # Ignore value if empty
            if (value): 
                _data = self._put_data(self.update_path, [member, address, value])
            else:
                raise RinorError('999', 'No command or value provided')
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)
        return _data[self.index][0]

class HostPipe(RinorPipe):
    cache_expiry = 3600
    list_path = "/host"
    index = 'host'
    paths = []
    
    def get_detail(self, id):
        _data = self._get_data("%s/%s" % (self.list_path, id))
        if _data.status == "ERROR":
            raise RinorError(_data.code, _data.description)        
        if len(_data[self.index]) > 0:
            return _data[self.index][0]
        else:
            return None