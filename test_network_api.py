import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time
import socket

test_system = "test_network_api"
timeout = 180


def test_network_api_client(boot_with_proxy):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    success = 'Client app read completed'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    print(text)
    assert match == success

def test_network_api_server(boot_with_proxy,run_tap_server_test):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    success = 'Closing server socket communication'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    print(text)
    assert match == success

@pytest.fixture(scope="module")
def run_tap_server_test():
    print("Running tap app to connect to Server")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Trying to connect to Server...')

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.82.92', 5555)
    print('connecting to %s port %s' %server_address, file=sys.stderr)
    sock.connect(server_address)

    try:
        # Send data
        message = 'This is the message.  It will be repeated. Hello from client...!'
        print('sending "%s"' %message, file=sys.stderr)
        sock.sendall(message.encode())

        # Look for the response
        received_string = ""

        while len(received_string) < len(message):
            received_string += sock.recv(1).decode()

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()
        print('received "%s"' %received_string, file=sys.stderr)
        assert received_string == message
    yield
