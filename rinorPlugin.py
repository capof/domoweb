import cherrypy
from cherrypy.process import plugins
from rinorPipe import UsagePipe

class RinorPlugin(plugins.SimplePlugin):
    def __init__(self, bus, project):
        self.project = project
        plugins.SimplePlugin.__init__(self, bus)

    def start(self):
        self.bus.log("Starting the Rinor Plugin")
#        UsagePipe.load()

