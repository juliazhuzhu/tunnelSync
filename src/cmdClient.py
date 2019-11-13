
import socket
import sys
import json

server_address = './uds_socket'
 
def send_data_unix_socket(data):
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    print (sys.stderr, 'connecting to %s' % server_address)
    try:
        sock.connect(server_address)
    except socket.error:
        print (sys.stderr)
        sys.exit(1)
    try:
        # Send data
        print (sys.stderr, 'sending "%s"' % data)
        sock.sendall(data)
     
        
    finally:
        print (sys.stderr, 'closing socket')
        sock.close()

class AddPortCommand:
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
            
    def sendLocalOffer(self):
        self.data['sub_type']='localOffer'
        self.__send()
    
    def sendRemoteAnswer(self):
        self.data['sub_type']='remoteAnswer'
        self.__send()
    
    def sendRemoteOffer(self):
        self.data['sub_type']='remoteOffer'
        self.__send()
            
    def sendLocalAnswer(self):
        self.data['sub_type']='localAnswer'
        self.__send() 
     
    
               
    def __send(self):
       
        encoded_data = json.dumps(self.data).encode('utf-8')
        send_data_unix_socket(encoded_data)
        print(encoded_data.decode('utf-8'))

class DelPortCommand:
    def __init__(self,callid):
       self.callid = callid
    
    def send(self):
        self.data = {
                    'callid': self.callid,
                    'type': 'delPort',
                    }
       
        encoded_data = json.dumps(self.data).encode('utf-8')
        send_data_unix_socket(encoded_data)
        print(encoded_data.decode('utf-8'))


if __name__ == "__main__":
   request = AddPortCommand("1234",1234,455,22,22,11)
   request.sendLocalOffer()
   
   request = AddPortCommand("1234",1234,455,22,22,11)
   request.sendRemoteAnswer()
   
   request = AddPortCommand("1235",1235,455,22,22,11)
   request.sendRemoteOffer()
   
   request = AddPortCommand("1235",1235,455,22,22,11)
   request.sendLocalAnswer()
   
   request = DelPortCommand("1234")
   request.send()
   
   request = DelPortCommand("1235")
   request.send()

