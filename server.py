#  coding: utf-8 
import socketserver
import os
from pathlib import Path
from mimetypes import MimeTypes

# Copyright 2023 Abram Hindle, Eddie Antonio Santos, Gurkirat Singh
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()

        route_handling(self)

        print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

def route_handling(self):
    file_name = 'www' + str(self.data).split()[1]
    path = Path(file_name)
    absPath = os.path.abspath(path)
    
    have_reponse = False

    if (str(self.data).split()[0][2:] == 'GET'):
        pass
    else:
        print_405_error(self)
        return
    print(str(self.data).split()[0][2:])

    if ('www' in absPath):
        header = 'HTTP/1.1 200 OK\n'
        pass
    else:
        print_404_error(self)
        return

    #handling dir
    if (os.path.isdir(path)):
        # check if dir ends with '/'
        if file_name[len(file_name)-1] == '/':
            file_name += 'index.html'
            path = Path(file_name)
            #check if index.html exits in dir
            if (os.path.isfile(path)):
                file = open(path, 'rb')
                response = file.read()
                have_reponse = True
                file.close()
            #index.html not in dir
            else:
                print_404_error(self)
        
        # if dir not ends with '/' (301 moved)
        else:
            handle_301(self)
            
    #handling files
    elif (os.path.isfile(path)):
        file = open(path, 'rb')
        response = file.read()
        have_reponse = True
        file.close()
        
    else :
        print_404_error(self)
    
    if (have_reponse):  
        mime = MimeTypes()
        mimetype, x = mime.guess_type(path)
        header += 'Content-Type: '+ str(mimetype) +'\r\n'

        final_response = header.encode('utf-8')
        final_response += response

        self.request.send(final_response)
    
def handle_301(self):
    header = 'HTTP/1.1 301 Permanently Moved\n\n'
    loc = 'Location: '
    response = header + loc + str(self.data).split()[1] + '/'

    final_response = response.encode('utf-8')

    self.request.send(final_response)

def print_405_error(self):
    header = 'HTTP/1.1 405 Method Not Allowed\n\n'

    final_response = header.encode('utf-8')

    self.request.send(final_response)

def print_404_error(self):
    header = 'HTTP/1.1 404 Not Found\n\n'
    response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response

    self.request.send(final_response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
