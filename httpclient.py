#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):


    def formRequest(self, command, path, hostname):


        if (command == "GET"):
            req_type = "GET " + path


        if (command == "POST"):
            req_type = "POST " + path




        request = req_type + " HTTP/1.1" + "\r\n" + \
        "Host:" + hostname + "\r\n" + \
        "Accept: */*\r\n"




        #"Date: " + datetime.datetime.today().strftime("%a, %d %B %Y %X %Z") + "\r\n" \
        #"Content-type: text/" + mime_type + "\r\n" + \
        #"Content-length: " + str(len(contents)) + "\r\n\r\n" + \
        #contents + "\r\n"


        return request




    def connect(self, host, port):




        if port is None:
            port = 80

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect((host, port))

        except socket.error as msg:
            self.socket.close()
            self.socket = None


        if self.socket == None:
            sys.exit(1)




        return None

    def get_code(self, data):

        code = (int)((data.split(" "))[1])


        return code

    def get_headers(self,data):

        headers = data.split("\r\n\r\n")[0]

        return headers

    def get_body(self, data):


        body = data.split("\r\n\r\n")[1]

        #print(body)

        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #code = 500
        #body = ""


  

        hostname, port, path = self.parse(url)




        self.connect(hostname, port)

        request = self.formRequest("GET", path, hostname )
        request += "Connection: close\r\n\r\n"


    

        self.sendall(request)



        recieved_data = self.recvall(self.socket)
        self.socket.close()

      


        print(recieved_data)

        code = self.get_code(recieved_data)
        body = self.get_body(recieved_data)

   


        return HTTPResponse(code, body)

    def POST(self, url, args=None):

        #code = 500
        #body = ""

        hostname, port, path = self.parse(url)

        self.connect(hostname, port)


        if  (args is None):
            encoded_args = ""
            length = 0

        else:
            encoded_args = urlencode(args)
            length = len(encoded_args)




        #https://stackoverflow.com/questions/14551194/how-are-parameters-sent-in-an-http-post-request
        content_type = "application/x-www-form-urlencoded"

        request = self.formRequest("POST", path, hostname)

        request += "Connection: close\r\n"
        request += "Content-type: " + content_type + "\r\n"
        request += "Content-length: {}\r\n\r\n".format(length)
        request += encoded_args


        #print(request)

        self.sendall(request)

        recieved_data = self.recvall(self.socket)

        print(recieved_data)

        code = self.get_code(recieved_data)
        body = self.get_body(recieved_data)


        self.socket.close()

        return HTTPResponse(code, body)

    def parse(self, url):



 

        parsed_url = urlparse(url)

	

        hostname = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path

        

        # add trailing for paths not including .something
        if path == "":
            path = "/"


        return hostname, port, path




    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"

    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
