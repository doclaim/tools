import sys,os,time,threading
from iPlugin import Plugin
from imp import find_module,load_module,acquire_lock,release_lock

class mythread(threading.Thread):  
    def __init__(self,plug):  
        threading.Thread.__init__(self)  
        self.plugin=plug
        #self.doRecv=True
    def run(self):
        self.doRecv=True
        pm=DirectoryPluginManager()
        while 1==1:
              if self.doRecv==False:
                 continue
              plugin=pm.getPlugins(self.plugin.name)
              if len(plugin) <1:
                 continue
              plu=plugin[0]
              time.sleep(int(plu.interval))
              try:
                 plu.execute()
              except:
                 print 'error'

    def stop(self):
        self.doRecv = False
  
    def restart(self):
	self.doRecv=True
        print 'true'
        print self.getName()

class DirectoryPluginManager():
    """Plugin manager that loads plugins from plugin directories.
    """
    name = "directory"
    plugins=[]
    thread=[]

    def __init__(self):
        self.plugdir = '/usr/local/ras/plugins/files'
    
    def addPlugin(self,name):
	self.loadPlugin(name)
        self.showPlugin()

    def delPlugin(self,name):
	plugs=self.getPlugins(name)
        if len(plugs)==0:
           print "%s not found" %name
           return
        plug=plugs[0]
        mod = sys.modules.get(plug.name)
        #mod = sys.modules.get(plug.name)
        print mod
        print plug.name        
        if mod is not None:
            self.stopThread(plug.name)
            DirectoryPluginManager.plugins.remove(plug)
            del sys.modules[plug.name]
        self.showPlugin()         

    def getPlugins(self,name=None):
        plugins = []
        for plugin in DirectoryPluginManager.plugins:
            if (name is None or plugin.name == name):
                plugins.append(plugin)
        return plugins

    def reloadPlugin(self,name):
	self.delPlugin(name)
	self.addPlugin(name)

    def showPlugin(self):
        print len(DirectoryPluginManager.plugins)
	for a in DirectoryPluginManager.plugins:
            print sys.modules.get(a.name)
    
    def execPlugin(self,plugin):
	while 1==1:
          time.sleep(int(plugin.interval))
          try:
             plugin.execute()
          except:
             print 'execute failed'
	        
    def startThread(self,plugin):
        new=True
        for item in DirectoryPluginManager.thread:
           if plugin.name != item.getName():
              continue
           item.restart()
           print 'fff' 
           new=False
        if new==False:
           return        
        t=mythread(plugin)
	DirectoryPluginManager.thread.append(t)
        t.setName(plugin.name)
        t.setDaemon(True)
        t.start()
    
    def showThread(self):
	print "activeThread count is %s" %(threading.activeCount() - 1)
	for item in threading.enumerate():
	    print item	
 
    def stopThread(self,name):
        #for item in threading.enumerate():
        for item in DirectoryPluginManager.thread:
	    if name != item.getName():
	       continue
            if item.isAlive():
        	try:
                   #item._Thread__stop()
                   #item._Thread__delete()
                   print item.doRecv
                   item.stop()
                   print item.doRecv
                except:
                   print "could not be terminated %s" %name

    def loadPlugin(self,name):
	loaded=False
	for plug in DirectoryPluginManager.plugins:
	    if plug.name == name:
		loaded=True
		break
        if loaded == True:
	   return
	
	fh=None
	mod=None
	try:
            acquire_lock()
            fh, filename, desc = find_module(name, [self.plugdir])
            old = sys.modules.get(name)
            if old is not None:
               # make sure we get a fresh copy of anything we are trying
               # to load from a new path
               del sys.modules[name]
            mod = load_module(name, fh, filename, desc)
        finally:
            if fh:
                fh.close()
                release_lock()
            if hasattr(mod, "__all__"):
                plug=getattr(mod,mod.__all__[0])
                if issubclass(plug, Plugin):
                   DirectoryPluginManager.plugins.append(plug())
                   #sys.modules.get(a.name)
		   self.startThread(plug())

    def loadPlugins(self):
        """Load plugins by iterating files in plugin directories.
        """
        plugins = []
        
        for f in os.listdir(self.plugdir):
            if f.endswith(".py") and f != "__init__.py":
            	plugins.append(f[:-3])

        for name in plugins:
	    self.loadPlugin(name)
        self.showPlugin()
