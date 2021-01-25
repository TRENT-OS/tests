from scapy.all import *
import socket
import logs # logs module from the common directory in TA
import pytest
from http.server import BaseHTTPRequestHandler, HTTPServer
import shutil
import pathlib
import sys
import socketserver
import threading
import os
import tests

# This python file is imported by pydoc which sometimes throws an error about a
# missing IPv6 default route (if the machine building the documentation doesn't
# have it set). To remove this warning we disable IPv6 support in scapy, since
# we don't use it at this time.
from scapy.config import conf
conf.ipv6_enabled = False

test_system = None
TEST_TIMEOUT = 10


def get_requested_filepath(path):
    foldername = pathlib.PurePath(__file__)

    # PurePath(path).name is used as path is of the format
    # "/<requested_file>.bin"
    filename = pathlib.PurePath(
                    foldername.parent,
                    (pathlib.Path(__file__)).stem,
                    pathlib.PurePath(path).name)

    return filename


class HandlerClass(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'bin')
        self.end_headers()

    def do_GET(self):
        self._set_response()

        try:
            file = open(get_requested_filepath(self.path),'rb')
            self.wfile.write(file.read())
        except:
            self.wfile.write('File missing :'.encode('utf-8'))
            self.wfile.write(self.path.encode('utf-8'))



def startServer(server_class=HTTPServer, handler_class=HandlerClass, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except:
        print("Exception occurred!!!")
    httpd.server_close()



@pytest.fixture(scope="module")
def startDaemon(request):
    #start the server in a seperate thread
    daemon = threading.Thread(name='daemon',target=startServer,daemon=True)
    daemon.start()
    def fin():
        print("teardown httpd")
        daemon.killed = True
    request.addfinalizer(fin)

