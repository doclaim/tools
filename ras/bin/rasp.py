import redis,yaml,sys,os,commands
sys.path.append('../plugins')
from pluginManager import DirectoryPluginManager

class raspmanager():
	def loadyaml(self):
	    retu='true'
	    try:
		y=open(self.config)
		global dict_yaml
		dict_yaml=yaml.load(y)
	    except Exception,e:
		retu='false'
		print Exception,":",e
	    return retu

	def parmfmt(self,inputstr,name):
	    arr=inputstr.split(' ')
	    x=0
	    retustr=''
	    for i in arr:
		x=x+1
		if i==name and x<len(arr):
		   retustr=arr[x]
		   break
	    return retustr

	def plugin_mgr(self,add,update,dele):
	    if dele!='' or update!='':
               print dele
	       self.plugin_manager.delPlugin(dele)
	    
	    if dele=='':
	       if add!='':
		  pluname=add
	       else:
		  pluname=update
               path='rm -rf ' + self.localpludir + '/' + pluname + '.py'
	       a,b=commands.getstatusoutput(path)
               print path,a
               path='wget -P ' + self.localpludir + ' ' + self.httpsrv + '/' + pluname + '.py'
               print path
	       a,b=commands.getstatusoutput(path)
	       print a
               if a==0:
		  self.plugin_manager.addPlugin(pluname)
	       

	def __init__(self):
            self.config='/usr/local/ras/etc/config.yaml'
	    retu=self.loadyaml()
	    if retu == 'false':
	       sys.exit(1)
	    setting=dict_yaml['root']['setting']
	    srvip=setting['srvip']
	    srvport=setting['srvport']
	    httpsrv=setting['httpsrv']
	    resid=setting['resid']
	    subch=setting['subch']
	    r = redis.Redis(srvip,srvport)
	    r.subscribe(subch)
	    
	    #init pluginmanager
	    plugin_mgr = DirectoryPluginManager()
	    plugin_mgr.loadPlugins()
            self.plugin_manager=plugin_mgr
            self.httpsrv=httpsrv
            self.localpludir='/usr/local/ras/plugins/files'
	    for msg in r.listen():
	      data=str(msg['data'])
              targetid=self.parmfmt(data,'-h')
	      addplu=self.parmfmt(data,'-a')
	      updateplu=self.parmfmt(data,'-u')
	      delplu=self.parmfmt(data,'-d')
	      if (targetid !='ALL' and targetid != resid):
		 continue
	      self.plugin_mgr(addplu.strip(),updateplu.strip(),delplu.strip())
