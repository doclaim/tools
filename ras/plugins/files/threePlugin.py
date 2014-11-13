#coding:utf-8
import sys,time
sys.path.append('../')

from iPlugin import Plugin
import commands
__all__ = ["ThreePlugin"]

class ThreePlugin(Plugin):
   
    name = "threePlugin"
    version = '0.0.1'
    interval = 10

    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):
        return "first plugin"

    def execd(self):
        while 1==1:
              print 'test_first'
              print 'edit'
              time.sleep(1)
    
    def newfunc(self):
	print 'ii'

    def newfunc2(self):
	print '22'
 
    def newfun3(self):
	pass

    def execute(self):
  	commands.getstatusoutput(" echo three >> /tmp/test")		

	

    def execFun(self):
        print 'update command'
        #return "exec first function"
