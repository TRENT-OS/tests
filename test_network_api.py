import socket
import time
import re
import os
import logs
import pytest

import sys

from scapy.all import *

sys.path.append('../common')


test_system = "test_network_api"
timeout = 180

NET_GATEWAY = "192.168.82.1"
# Defines taken from the seos_system_config.h
# Client
ETH_1_ADDR = "192.168.82.91"

CFG_TEST_HTTP_SERVER = "192.168.82.12"
#Server
ETH_2_ADDR = "192.168.82.92"

def test_network_basic(boot_with_proxy):
    """Check to see if scapy is running correctly """
    for i in range(5):
        randNum = random.randint(0, 255)
        ans = sr1(IP(dst=NET_GATEWAY)/ICMP(id=randNum),timeout=1)
        if ans is None:
            pytest.fail("Timeout waiting for ping reply")
        if not ans.payload.id == randNum:
            pytest.fail("Failed we got a reply for a ping we didn't send.")
        

@pytest.mark.skip(reason="Not implemented yet")
def test_network_picotcp_unit_tests(boot_with_proxy):
    """Execute all picotcp unit tests"""

@pytest.mark.skip(reason="Not implemented yet")
def test_network_picotcp_smoke_tests(boot_with_proxy):
    """Execute all picotcp smoke tests"""

# -------------------------------------------------------------------------------
@pytest.mark.skip(reason="Failing due to synchronization issue")
def test_network_api_client(boot_with_proxy):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Test ended"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s"%(expr_fail))

# -------------------------------------------------------------------------------
# at the moment the stack can handle these sizes without issues. We will increase this sizes and fix the issues in a second moment.
lst = [2, 4, 8, 16, 32, 64, 128, 256, 512]
@pytest.mark.parametrize('n', lst)
#@pytest.mark.skip(reason="Takes too long")
def test_network_api_echo_server(boot_with_proxy, n):
    """Test TCP/IP stack with a server that echoes the data sent to him in blocks. The test is repeated using blocks of different sizes."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    with open('test_network_api/dante.txt', 'rb') as file:
        blob = file.read(n)

    run_echo_client(blob)

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["connection closed by server"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s"%(expr_fail))


# -------------------------------------------------------------------------------
def run_echo_client(blob):

    print("Running tap app to connect to Server")

    server_address = (ETH_2_ADDR, 5555)
    received_blob = b""

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (sock is None):
        pytest.skip("could not get a socket")

    sock.settimeout(timeout)

    for attempt in range(3):
        print('Trying to connect to Server, attempt # ' + str(attempt) + '...')

        try:
            # Connect the socket to the port where the server is listening
            print('connecting to %s port %s' % server_address, file=sys.stderr)
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
                print('first byte received in ' + str(time_leapsed_ms) +
                      ' ms, troughtput (partial) is ' + str((len(blob) + 1) / time_leapsed_ms) + ' kB/s')

        time_leapsed_ms = (time.time() - test_time_base) * 1000
        print('echo completed in ' + str(time_leapsed_ms) +
              ' ms, troughtput (full echo) is ' + str((len(blob) * 2) / time_leapsed_ms) + ' kB/s')

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()
        if not received_blob == blob:
             pytest.fail("Blobs mismatch")


# --- TCP TESTS ---
@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
def test_network_tcp_connection_establishment(boot_with_proxy):
    """Test the SYN/ACK-SYN/ACK sequence with various sequence numbers, delays and lost packets."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    for i in range(10):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,flags='S')
        sa = sr1(s,timeout=2)
        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=s.seq+1,ack=sa.seq+1,flags='A')
        send(a)
        if not (sa.ack == s.ack +1):
            pytest.fail("ACK mismatch")
        if not (a.ack == sa.seq+1):
            pytest.fail("ACK mismatch")

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80
@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
def test_network_tcp_connection_closure(boot_with_proxy):
    """Test the FIN sequence with various sequence numbers, delays and lost packets."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,flags='S')
        sa = sr1(s,timeout=2)
        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=s.seq+1,ack=sa.seq+1,flags='A')
        send(a)
        r = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=a.seq,ack=sa.seq+1,flags='F')
        p = sr1(r,timeout=2)
        if p is None:
            pytest.fail("Didn't receive FIN ack")
        if not ( p.haslayer(TCP) and ((p['TCP'].flags & FIN) or (p['TCP'].flags & ACK))): 
             pytest.fail("Didn't receive FIN")

@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
def test_network_tcp_connection_reset(boot_with_proxy):
    """Test the RST sequence with various sequence numbers, delays and lost packets."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,flags='S')
        sa = sr1(s,timeout=2)
        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=s.seq+1,ack=sa.seq+1,flags='A')
        send(a)
        #r = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=a.seq,ack=sa.seq+1,flags='RA')
        r = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=a.seq,ack=sa.seq+1,flags='R')
        p = sr1(r,timeout=2)
        if p is None: 
            pytest.fail("Didn't receive RST ack")

@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
def test_network_tcp_connection_invalid(boot_with_proxy):
    """Test connecting to a port nobody is listening on."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    for i in range(10):
        source_port = random.randint(1025, 65536)
        r = IP(dst=ETH_2_ADDR)/TCP(dport=source_port,sport=source_port,seq=0,ack=0,flags='S')
        p = sr1(r,timeout=2)
        if p is not None:
            pytest.fail("No reply")
        if not (p.haslayer(ICMP) and p.payload.type == 3):
            pytest.fail("Received wrong message. Expected Port unreachable")

@pytest.mark.skip(reason="Not implemented yet")
def test_network_tcp_window_size_scaling(boot_with_proxy):
    """Test the TCP window size scaling with various sequence numbers, delays and lost packets."""

@pytest.mark.skip(reason="Not implemented yet")
def test_network_tcp_out_of_band_signaling(boot_with_proxy):
    """Test TCP Out of Band signaling various sequence numbers, delays and lost packets."""

@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
def test_network_tcp_out_of_order_receive(boot_with_proxy):
    """Test receiving TCP pakets out of order with various sequence numbers, delays and lost packets."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,flags='S')
        sa = sr1(s,timeout=2)
        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=s.seq+1,ack=sa.seq+1,flags='A')
        send(a)
        r = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=a.seq,ack=0,flags='')/"TTTTTTTT"
        p = sr1(r,timeout=2)

        r1 = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=p.ack,ack=p.seq+len(p),flags='')/"XXXXXXXX"
        p1 = sr1(r1,timeout=2)
        time.sleep(10)



def test_network_tcp_data_send(boot_with_proxy):
    """Test sending data in TCP pakets with various sequence numbers, delays and lost packets."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)

    for i in range(5):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555)/Raw(RandString(size=72))
        r = sr1(s,timeout=2)
        s.show()
        r.show()
#        assert s.payload == r.payload

# # --- UDP TESTS ---

# @pytest.mark.skip(reason="Not implemented in SEOS")
# def test_network_udp_send(boot_with_proxy):
#     """Test sending UDP datagrams with various sizes."""

# @pytest.mark.skip(reason="Not implemented in SEOS")
# def test_network_udp_receive(boot_with_proxy):
#     """Test receiving UDP datagrams with various sizes."""


# --- DHCP TESTS ---

@pytest.mark.skip(reason="Not implemented in SEOS")
def test_network_dhcp_get_address(boot_with_proxy):
    """Test getting a valid IP configuration from a DHCP server."""

@pytest.mark.skip(reason="Not implemented in SEOS")
def test_network_dhcp_renew_address(boot_with_proxy):
    """Test renewing the IP address from a DHCP server."""

@pytest.mark.skip(reason="Not implemented in SEOS")
def test_network_dhcp_expire_address(boot_with_proxy):
    """Test having the existing lease expiring while having active TCP connections."""


### --- ARP TESTS ---
@pytest.mark.skip(reason="Fails due synchronization issue")
def test_network_arp_request(boot_with_proxy):
    """Test asking for the MAC address of a known host."""

    test_run = boot_with_proxy(test_system)
    filter = "arp and src host "+ETH_1_ADDR+" and dst host "+CFG_TEST_HTTP_SERVER
    p = sniff(iface='br0',filter=filter,timeout=30)
    f_out = test_run[1]
    time.sleep(10)
    if len(p) == 0:
         pytest.fail("Timeout waiting for arp request")
    p.show()

@pytest.mark.skip(reason="Filtered by proxy")
def test_network_arp_reply_client(boot_with_proxy):
    """Test if the client implementation component replies to arp request.
        Success: We get a valid arp reply
        Failure: Timeout
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    ans, uns = arping(ETH_1_ADDR)
    if len(uns) != 0:
         pytest.fail("Timeout waiting for arp reply")

@pytest.mark.skip(reason="Timeout due to server load")
def test_network_arp_reply_server(boot_with_proxy):
    """Test if the server implementation component replies to arp request.
        Success: We get a valid arp reply
        Failure: Timeout
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    ans, uns = arping(ETH_2_ADDR)
    if len(uns) != 0:
        pytest.fail("Timeout waiting for arp reply")

### --- ICMP TESTS ---

@pytest.mark.skip(reason="Not implemented in SEOS")
def test_network_ping_request(boot_with_proxy):
    """Test pinging a known host."""
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)
    filter = "icmp and src host "+ETH_1_ADDR+" and dst host "+CFG_TEST_HTTP_SERVER
    p = sniff(iface='br0',filter=filter,timeout=30)
    if len(p) == 0:
         pytest.fail("Timeout waiting for ping request")
    p.show()

@pytest.mark.skip(reason="Filtered by proxy")
def test_network_ping_reply_client(boot_with_proxy):
    """Test if the client implementation component replies to ping.
        Success: We get a valid ping reply
        Failure: Timeout
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)

    lost = 0
    for i in range(5):
        randNum = random.randint(0, 255)
        ans = sr1(IP(dst=ETH_1_ADDR)/ICMP(id=randNum),timeout=2)
        if ans == None:
            pytest.fail("Timeout waiting for ping reply")
        if not ans.payload.id == randNum:
            pytest.fail("Failed. We got a reply for a ping we didn't send.")



def test_network_ping_reply_server(boot_with_proxy):
    """Test if the server implementation component replies to ping.
        Success: We get a valid ping reply
        Failure: Timeout
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    time.sleep(10)

    lost = 0
    for i in range(5):
        randNum = random.randint(0, 255)
        ans = sr1(IP(dst=ETH_2_ADDR)/ICMP(id=randNum),timeout=1)
        if ans == None:
            pytest.fail("Timeout waiting for ping reply")
        if not ans.payload.id == randNum:
            pytest.fail("Failed. We got a reply for a ping we didn't send.")
