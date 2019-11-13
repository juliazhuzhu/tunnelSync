
import threading
from call import Call
from port_table import PortTable

class CallMgr:
    
    _instance_lock = threading.Lock()
    
    def __init__(self):
        self.call_table={}
        
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(CallMgr, "_instance"):
            with CallMgr._instance_lock:
                if not hasattr(CallMgr, "_instance"):
                    CallMgr._instance = object.__new__(cls)  
        return CallMgr._instance
        
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(CallMgr, "_instance"):
            with CallMgr._instance_lock:
                if not hasattr(PortTable, "_instance"):
                    CallMgr._instance = CallMgr(*args, **kwargs)
        return CallMgr._instance    
       
    def start(self):
        pass
        
    def addCall(self,callid):
        call = Call(callid)
        self.call_table[callid] = call
        return call
    
    
    def getCall(self,callid):
        if callid in self.call_table:
            return self.call_table[callid]
        return ""
    
    def rmCall(self,callid):
        if callid in self.call_table:
            call = self.call_table[callid]
            call.write('del')
            ins = PortTable.instance()
            ins.rmCallPorts(callid)
            del self.call_table[callid]
            