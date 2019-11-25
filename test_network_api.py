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

@pytest.mark.skip(reason="there is a framing problem currently that prevents this test to succeed as it expects a clean close (FIN packet, from the connected peer) that does not get catched 100% of times")
def test_network_api_client(boot_with_proxy):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    success = 'Client app read completed'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    print(text)
    assert match == success

def test_network_api_echo_server(boot_with_proxy):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    run_echo_client()
    success = 'Closing server socket communication'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    print(text)
    assert match == success

def run_echo_client():
    print("Running tap app to connect to Server")

    server_address = ('192.168.82.92', 5555)
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        print ('Trying to connect to Server...')

        try:
            # Connect the socket to the port where the server is listening
            print('connecting to %s port %s' %server_address, file=sys.stderr)
            sock.connect(server_address)
        except:
            print('connection failed, retrying in 2 secs')
            time.sleep(2)
        break

    try:
        received_string = ""
        # Send data
        message = 'This is the message.  It will be repeated. Hello from client...!'
        print('sending "%s"' %message, file=sys.stderr)
        sock.sendall(message.encode())

        # Look for the response
        while len(received_string) < len(message):
            received_string += sock.recv(1).decode()

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()
        print('received "%s"' %received_string, file=sys.stderr)
        assert received_string == message
