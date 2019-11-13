
import threading
class PortTable:
    _instance_lock = threading.Lock()
    def __init__(self):
        self.local_port_table = {}
        self.remote_port_table = {}
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(PortTable, "_instance"):
            with PortTable._instance_lock:
                if not hasattr(PortTable, "_instance"):
                    PortTable._instance = object.__new__(cls)  
        return PortTable._instance
        
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(PortTable, "_instance"):
            with PortTable._instance_lock:
                if not hasattr(PortTable, "_instance"):
                    PortTable._instance = PortTable(*args, **kwargs)
        return PortTable._instance
        
    def addLocalPort(self,callid,audio_port,video_port,content_port, fecc_port, bfcp_port):
        self.local_port_table[callid]= (audio_port,video_port,content_port,fecc_port,bfcp_port)
    
    def addRemotePort(self,callid,audio_port,video_port,content_port, fecc_port, bfcp_port):
        self.remote_port_table[callid]= (audio_port,video_port,content_port,fecc_port,bfcp_port)
       
    def getLocalPorts(self,callid):
        if callid in self.local_port_table:
            return self.local_port_table[callid]
        return ""
    
    def getRemotePorts(self,callid):
        if callid in self.remote_port_table:
            return self.remote_port_table[callid]
        return ""
    
    def rmCallPorts(self,callid):
        if callid in self.remote_port_table:
            del self.remote_port_table[callid]
            
        if callid in self.local_port_table:
            del self.local_port_table[callid]
            
    def start(self):
        pass

if __name__ == "__main__":
    
    portTable = PortTable()
    
    portTable.addLocalPort("1234", 3222, 3224, 4226, 3228, 3230)
    
    portTable1 = PortTable.instance()
    
    item_val = portTable1.getLocalPorts("1234")
    if item_val != "":
        print(item_val)
    portTable1.rmCallPorts("1234")
    portTable2 = PortTable.instance()
    item_val = portTable2.getLocalPorts("1234")
    if item_val != "":
        print(item_val)
    else:
        print("call not exist")