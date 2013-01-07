import urllib
import urllib2
import cherrypy
from django.utils import simplejson
from httplib import BadStatusLine
from domowebExceptions import RinorNotAvailable, RinorError, RinorNotConfigured

class RinorPipe():
    ip = None
    port = None
    prefix = None

    @staticmethod
    def init():
        from domoweb.models import Parameter
        try:
            RinorPipe.ip = Parameter.objects.get(key='rinor_ip').value
            RinorPipe.port = Parameter.objects.get(key='rinor_port').value
        except Parameter.DoesNotExist:
            raise RinorNotConfigured
        else:
            try:
                RinorPipe.prefix = Parameter.objects.get(key='rinor_prefix').value
            except Parameter.DoesNotExist:
                cherrypy.engine.log("Rinor configured on http://%s:%s" % (RinorPipe.ip, RinorPipe.port))
            else:
                cherrypy.engine.log("Rinor configured on http://%s:%s/%s" % (RinorPipe.ip, RinorPipe.port, RinorPipe.prefix))

    @staticmethod
    def _clean_url(path, data=None):
        if (data):
            _tmp = []
            for d in data:
                if type(d) == str or type(d) == unicode:
                    d=urllib.quote(d.encode('utf8'), '')
                else:
                    d=str(d)
                _tmp.append(d)
            _data = '/'.join(_tmp)
            _path = "%s/%s/" % (path, _data)
        else:
            _path = "%s/" % path
        return _path
    
    @staticmethod
    def _get_data(path, data=None):
        _path = RinorPipe._clean_url(path, data)
        cherrypy.engine.log("RINOR GET %s" % _path)
        if not RinorPipe.ip:
            RinorPipe.init()
        _data = _get_json(path=_path, ip=RinorPipe.ip, port=RinorPipe.port, prefix=RinorPipe.prefix)
        return _data

    @staticmethod
    def get_list(path, index):
        data = RinorPipe._get_data(path)
        if data.status == "ERROR":
            raise RinorError(data.code, data.description)
        return data[index]
    
def _get_json(path, ip, port, prefix=None):
    if prefix:
        uri = "http://%s:%s/%s%s" % (ip, port, prefix, path)
    else:
        uri = "http://%s:%s%s" % (ip, port, path)
    
    retries = 0
    attempts = 0
    while True:
        try:
            attempts += 1
            respObj = urllib2.urlopen(uri)
            break
        except urllib2.HTTPError, e:
            raise RinorNotAvailable(code=e.code, resp=e.read())
        except urllib2.URLError, e:
            if attempts <= retries:
                continue
            else:
                raise RinorNotAvailable(reason=e.reason)
        except BadStatusLine:
            raise RinorError(reason="No response for '%s'" % uri)
    resp = respObj.read()
    resp_obj = simplejson.loads(resp)
    return _objectify_json(resp_obj)
    
def _objectify_json(i):
    if isinstance(i, dict):
        transformed_dict = JSONDict()
        for key, val in i.iteritems():
            transformed_dict[key] = _objectify_json(val)
        return transformed_dict
    elif isinstance(i, list):
        for idx in range(len(i)):
            i[idx] = _objectify_json(i[idx])
    return i
    
class JSONDict(dict):
    def __getattr__(self, attrname):
        if self.has_key(attrname):
            return self[attrname]
        else:
            raise AttributeError

class UsagePipe(RinorPipe):
    index = 'device_usage'
    paths={
        "list": "/base/device_usage/list"
    }
    
    @staticmethod
    def load():
        from domoweb.models import Usage
        _data = UsagePipe.get_list(UsagePipe.paths['list'], UsagePipe.index)
        Usage.objects.all().delete()
        for usage in _data:
            u = Usage(id=usage.id, name=usage.name, options=usage.default_options)
            u.save()