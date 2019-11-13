
from port_table import PortTable
import os
import logging


class Call:
    def __init__(self,callid):
        self.callid = callid
        self.state = 'init'
        self.logger = logging.getLogger(__name__)
        
    def getCallId(self):
        return self.callid
    
    def addLocalOfferPort(self,audio,video,content,fecc,bfcp):
        instant = PortTable.instance()
        instant.addLocalPort(self.callid,audio,video,content,fecc,bfcp)
        log_str = "callid {}, audio {} video {} content {} fecc {} bfcp {}".format(self.callid,audio, video, content, fecc, bfcp)
        self.logger.info(log_str)
        if self.state == 'answer':
            self.write('add') 
            self.state = 'connected'
            return
        self.state = 'offer'
    
    def addRemoteOfferPort(self,audio,video,content,fecc,bfcp):
        instant = PortTable.instance()
        instant.addRemotePort(self.callid,audio,video,content,fecc,bfcp)
        log_str = "callid {}, audio {} video {} content {} fecc {} bfcp {}".format(self.callid,audio, video, content, fecc, bfcp)
        self.logger.info(log_str)
        if self.state == 'answer':
            self.write('add')
            self.state = 'connected'
            return
        self.state = 'offer'
        
    def addLocalAnswerPort(self,audio,video,content,fecc,bfcp):
        instant = PortTable.instance()
        instant.addLocalPort(self.callid,audio,video,content,fecc,bfcp)
        log_str = "callid {}, audio {} video {} content {} fecc {} bfcp {}".format(self.callid,audio, video, content, fecc, bfcp)
        self.logger.info(log_str)
        if self.state == 'offer':
            self.write('add')
            self.state = 'connected'
            return
        self.state = 'answer'
        
    def addRemoteAnswerPort(self,audio,video,content,fecc,bfcp):
        instant = PortTable.instance()
        instant.addRemotePort(self.callid,audio,video,content,fecc,bfcp)
        log_str = "callid {}, audio {} video {} content {} fecc {} bfcp {}".format(self.callid,audio, video, content, fecc, bfcp)
        self.logger.info(log_str)
        if self.state == 'offer':
            self.write('add')
            self.state = 'connected'
            return
        self.state = 'answer'
        
    def getState(self):
        return self.state
    
    def write(self,cmd):
        instant = PortTable.instance()
        tunnelPort=os.environ.get('TUNNEL_PORT')
        if tunnelPort == None:
            tunnelPort = 50000
        myCmd = '/usr/bin/distr.sh ' + cmd + ' ' + str(tunnelPort) + ' '
        dst_ports = instant.getLocalPorts(self.callid)
        src_ports = instant.getRemotePorts(self.callid)
        param = ""
        for (s, d) in zip(src_ports, dst_ports):
            if s == 0 or d == 0:
                continue
            param = param + str(s) + ':' + str(d) + ' '
            param = param + str(s+1) + ':' + str(d+1) + ' '
    
        myCmd = myCmd + param
        self.logger.info(myCmd)
        os.system(myCmd)
    
    

