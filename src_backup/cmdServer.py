import socket
import sys
import os
from urllib3 import *

def send(encoded_data,url):
        http = PoolManager()
        #encoded_data = json.dumps(self.data).encode('utf-8')
        r = http.request(
             'POST',
             url,
             body=encoded_data,
             headers={'Content-Type': 'application/json'})
        print(r.data.decode('utf-8'))
        
server_address = './uds_socket'
 
# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise
# Create a UDS socket
sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
# Bind the socket to the port
print (sys.stderr, 'starting up on %s' % server_address)
sock.bind(server_address)
 
# Listen for incoming connections
sock.listen(1)
 
while True:
    # Wait for a connection
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stderr, 'connection from', client_address)
 
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(300)
            print (sys.stderr, 'received "%s"' % data)
            if data:
                print (sys.stderr, 'sending data back to the client')
                send(data,'http://localhost:8001')
                #connection.sendall(data)
            else:
                print (sys.stderr, 'no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
