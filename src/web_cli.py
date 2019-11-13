from urllib3 import *
import json



class AddPortRequest:
    def __init__(self,callid,audio,video,content,fecc,bfcp):
        self.callid = callid
        self.audio_port=audio
        self.video_port=video
        self.content_port=content
        self.fecc_port=fecc
        self.bfcp_port=bfcp
    
        self.data = {
                    'callid': self.callid,
                    'type': 'addPort',
                    'audio': self.audio_port,
                    'video': self.video_port,
                    'content': self.content_port,
                    'fecc': self.fecc_port,
                    'bfcp': self.bfcp_port}
            
    def sendLocalOffer(self,url):
        self.data['sub_type']='localOffer'
        self.__send(url)
    
    def sendRemoteAnswer(self,url):
        self.data['sub_type']='remoteAnswer'
        self.__send(url)
    
    def sendRemoteOffer(self,url):
        self.data['sub_type']='remoteOffer'
        self.__send(url)
            
    def sendLocalAnswer(self,url):
        self.data['sub_type']='localAnswer'
        self.__send(url) 
     
    
               
    def __send(self,url):
        http = PoolManager()
        encoded_data = json.dumps(self.data).encode('utf-8')
        r = http.request(
             'POST',
             url,
             body=encoded_data,
             headers={'Content-Type': 'application/json'},
             timeout=Timeout(connect=2.0,read=4.0))
        print(r.data.decode('utf-8'))

class DelPortRequest:
    def __init__(self,callid):
       self.callid = callid
    
    def send(self,url):
        self.data = {
                    'callid': self.callid,
                    'type': 'delPort',
                    }
        http = PoolManager()
        encoded_data = json.dumps(self.data).encode('utf-8')
        r = http.request(
             'POST',
             url,
             body=encoded_data,
             headers={'Content-Type': 'application/json'},
             timeout=Timeout(connect=2.0,read=4.0))
        print(r.data.decode('utf-8'))

if __name__ == "__main__":
   
   request = AddPortRequest("1234",1112,2222,3332,4444,5556)
   request.sendLocalOffer('http://localhost:8001')
   
   request = AddPortRequest("1234",1112,2222,3332,4444,5556)
   request.sendRemoteAnswer('http://localhost:8001')
   
   request = AddPortRequest("1235",1114,2224,3334,4448,5558)
   request.sendRemoteOffer('http://localhost:8001')
   
   request = AddPortRequest("1235",1114,2224,3334,4446,5554)
   request.sendLocalAnswer('http://localhost:8001')
   
   
   
   request = AddPortRequest("1236",1116,2228,3336,4442,5552)
   request.sendRemoteAnswer('http://localhost:8001')
   
   request = AddPortRequest("1236",1118,2226,3338,4446,0)
   request.sendLocalOffer('http://localhost:8001')
   
   
   request = DelPortRequest("1234")
   request.send('http://localhost:8001')
   
   request = DelPortRequest("1235")
   request.send('http://localhost:8001')
   
  


  
   
    
 