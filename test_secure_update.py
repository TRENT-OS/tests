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
        self.wfile.write(
            "GET1 request for {}-".format(self.path).encode('utf-8'))

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


def test_timestamp_rcv(boot_with_proxy,startDaemon):
    """
    Checks reception of timestamp file from the server.
    """
    tests.run_test_log_match_sequence(
        boot_with_proxy,test_system,
        ['!!! test_requestTimestampFile_pos: OK',
         '!!! test_readTimestampFile_pos: OK'],
        TEST_TIMEOUT)



def test_snapshot_rcv(boot_with_proxy):
    """
    Checks reception of snapshot file from the server.
    """
    tests.run_test_log_match_sequence(
        boot_with_proxy,test_system,
        ['!!! test_requestSnapshotFile_pos: OK',
         '!!! test_readSnapshotFile_pos: OK'],
        TEST_TIMEOUT)



def test_target_rcv(boot_with_proxy):
    """
    Checks reception of target file from the server.
    """
    tests.run_test_log_match_sequence(
        boot_with_proxy,test_system,
        ['!!! test_requestTargetFile_pos: OK',
         '!!! test_readTargetFile_pos: OK'],
        TEST_TIMEOUT)



def test_root_rcv(boot_with_proxy):
    """
    Checks reception of root file from the server.
    """
    tests.run_test_log_match_sequence(
        boot_with_proxy,test_system,
        ['!!! test_requestRootFile_pos: OK',
         '!!! test_readRootFile_pos'],
        TEST_TIMEOUT)

def test_non_existing_file(boot_with_proxy):
    """
    Checks reception of a non existing file from the server.
    """
    tests.run_test_log_match_sequence(
        boot_with_proxy,test_system,
        ['!!! test_requestNonExistingFile_neg: OK',
         '!!! test_readNonExistingFile_neg: OK'],
        TEST_TIMEOUT)

def test_complete(boot_with_proxy):
    """
    Checking if all tests has been completed and that there was no
    failure/exception during the tear down phase.
    """
    tests.run_test_log_match_sequence(
        boot_with_proxy,test_system,
        ['!!! All tests successfully completed.'],
        TEST_TIMEOUT)
