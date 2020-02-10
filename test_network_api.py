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

#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="there is a framing problem currently that prevents this test to succeed as it expects a clean close (FIN packet, from the connected peer) that does not get catched 100% of times")
def test_network_api_client(boot_with_proxy):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    success = 'Client app read completed'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    print(text)
    assert match == success

#-------------------------------------------------------------------------------
# at the moment the stack can handle these sizes without issues. We will increase this sizes and fix the issues in a second moment.
lst = [ 2, 4, 8, 16, 32, 64, 128, 256, 512 ]
@pytest.mark.parametrize('n', lst)
def test_network_api_echo_server(boot_with_proxy, n):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    with open('./test_network_api/dante.txt', 'rb') as file:
        blob = file.read(n)

    run_echo_client(blob)

    success = 'connection closed by server'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    assert match == success


#-------------------------------------------------------------------------------
def run_echo_client(blob):

    print("Running tap app to connect to Server")

    server_address = ('192.168.82.92', 5555)
    received_blob = b""

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (sock is None):
        pytest.skip("could not get a socket")

    sock.settimeout(timeout)

    for attempt in range(3):
        print ('Trying to connect to Server, attempt # ' + str(attempt) + '...')

        try:
            # Connect the socket to the port where the server is listening
            print('connecting to %s port %s' %server_address, file=sys.stderr)
            sock.connect(server_address)
        except:
            print('connection failed, retrying in 2 secs')
            time.sleep(2)
            continue
        break

    try:
        # Send data
        print('sending blob of ' + str(len(blob)) + ' bytes', file=sys.stderr)
        test_time_base = time.time()
        sock.sendall(blob)

        # Look for the response
        while len(received_blob) < len(blob):
            received_blob += sock.recv(1)

            if (len(received_blob) == 1):
                time_leapsed_ms = (time.time() - test_time_base) * 1000
                print('first byte received in ' + str(time_leapsed_ms) + ' ms, troughtput (partial) is ' + str((len(blob) + 1) / time_leapsed_ms) + ' kB/s')

        time_leapsed_ms = (time.time() - test_time_base) * 1000
        print('echo completed in ' + str(time_leapsed_ms) + ' ms, troughtput (full echo) is ' + str((len(blob) * 2) / time_leapsed_ms) + ' kB/s')

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()
        assert received_blob == blob
