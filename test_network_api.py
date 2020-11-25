from scapy.all import *
import socket
import time
import re
import os
import logs # logs module from the common directory in TA
import pytest
import http.server
import socketserver
import shutil
import pathlib
import random
import string
import threading

import sys

server_dos_tests = ['test_tcp_options_poison']

# This python file is imported by pydoc which sometimes throws an error about a
# missing IPv6 default route (if the machine building the documentation doesn't
# have it set). To remove this warning we disable IPv6 support in scapy, since
# we don't use it at this time.
from scapy.config import conf
conf.ipv6_enabled = False


# configure in which interface to send out the packets.
conf.iface = "br0"
test_system = "test_network_api"
timeout = 180

CONTAINER_GATEWAY = "172.17.0.1"
NET_GATEWAY = "10.0.0.1"
# Defines taken from the system_config.h
# Client
ETH_1_ADDR = "10.0.0.10"

CFG_TEST_HTTP_SERVER = "192.168.82.12"
# Server
ETH_2_ADDR = "10.0.0.11"


#-------------------------------------------------------------------------------
def test_network_basic(boot_with_proxy):
    """Check to see if scapy is running correctly """
    for i in range(5):
        randNum = random.randint(0, 255)
        ans = sr1(IP(dst=CONTAINER_GATEWAY)/ICMP(id=randNum), timeout=1)
        if ans is None:
            pytest.fail("Timeout waiting for ping reply")
        if not ans.payload.id == randNum:
            pytest.fail("Failed we got a reply for a ping we didn't send.")


#-------------------------------------------------------------------------------
@pytest.mark.dependency()
def test_tcp_options_poison(boot_with_proxy):

    """Sends a malformed packet with tcp options as "0xFF 0x00 0x00 0x00". Some
    TCP/IP implementation may loop infinitely in the attempt of parsing such a
    sequence. The test sends the poisoned packet to the server listening on
    port 5555 in a loop. If no answer occurs then the server TCP stack is to be
    considered affected by the issue described."""

    timeout = 10
    sport = random.randint(1025, 65535)
    dport = 5555
    target_ip = ETH_2_ADDR
    ip_frame = IP(dst = target_ip)

    def ack_and_fin(sack):
        ack = sr1(ip_frame/\
                    TCP(dport = dport,\
                        sport = sport,\
                        flags = "A",\
                        seq=sack.ack,\
                        ack=sack.seq + 1),\
                    timeout=10)
        fack = sr1(ip_frame/\
                    TCP(dport = dport,\
                        sport = sport,\
                        flags = "FA",\
                        seq=sack.ack,\
                        ack=sack.seq + 1),\
                    timeout=10)
        lack = sr1(ip_frame/\
                    TCP(dport = dport,\
                        sport = sport,\
                        flags = "A",\
                        seq=fack.ack,\
                        ack=fack.seq + 1),\
                    timeout=10)

    def is_server_up(timeout):
        from time import time

        time_expired = time() + timeout
        while True:
            sack = sr1(ip_frame/\
                        TCP(dport = dport, sport = sport, flags = "S"),\
                        timeout=10)
            if sack is not None:
                ack_and_fin(sack)
                return True
            if time() > time_expired:
                return False

    print('Check if server is up (before poisoning)...')
    if is_server_up(timeout):
        print ("Server is up.")
    else:
        pytest.fail("Timeout while checking if server is up")

    print('Poisoning...')
    # OK, server is up, now poison it
    poison_pkt = TCP(dport   = dport,\
                     sport   = sport,\
                     options = [(255, b'')],\
                     flags   = "S")

    poison_pkt_raw = bytearray(raw(poison_pkt))

    poison_pkt = ip_frame/TCP(poison_pkt_raw)
    # compute the TCP checksum
    checksum = in4_chksum(socket.IPPROTO_TCP, poison_pkt[IP], poison_pkt_raw)
    # poison the packet and adjust the checksum to still be valid
    checksum = checksum + poison_pkt_raw[-3]
    poison_pkt_raw[-3] = 0
    poison_pkt_raw[-8] = checksum // 256
    poison_pkt_raw[-7] = checksum % 256

    poison_pkt = ip_frame/TCP(poison_pkt_raw)

    sack = sr1(poison_pkt, timeout=10)
    if sack is None:
        print("No answer received right after poisoning, this could be OK, maybe it just dropped the malformed packet")
    else:
        # server reacted fine to poison
        ack_and_fin(sack)

    print('Check if server is up (after poisoning)...')# this time should be not if poisoned
    if is_server_up(timeout):
        print ("Server is up.")
    else:
        pytest.fail("Timeout while checking if server is up")


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented yet")
def test_network_picotcp_unit_tests(boot_with_proxy):
    """Execute all picotcp unit tests"""


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented yet")
def test_network_picotcp_smoke_tests(boot_with_proxy):
    """Execute all picotcp smoke tests"""


#-------------------------------------------------------------------------------
def test_network_api_client(boot_with_proxy):
    """
    Test multisocket implementation. Two applications sharing a network stack
    try each to open 16 sockets and download data from the webserver running in
    the test container. The library signals when all sockets are in use.
    """

    test_run = boot_with_proxy(test_system)

    f_out = test_run[1]

    src = pathlib.Path(__file__).parent.absolute().joinpath('test_network_api/')

    dest = '/tmp/test_network_api'

    if(os.path.exists(dest)):
        shutil.rmtree(dest)

    shutil.copytree(src, dest)

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["No free sockets available 16"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["TCP client test successful"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))

    shutil.rmtree(dest)


#-------------------------------------------------------------------------------
# at the moment the stack can handle these sizes without issues. We will
# increase this sizes and fix the issues in a second moment.
lst = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
@pytest.mark.parametrize('n', lst)
# @pytest.mark.skip(reason="Takes too long")
def test_network_api_echo_server(boot_with_proxy, n):
    """
    Test TCP/IP stack with a server that echoes the data sent to him in blocks.
    The test is repeated using blocks of different sizes.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    src = pathlib.Path(__file__).parent.absolute().joinpath(
            'test_network_api/dante.txt')

    with open(src, 'rb') as data_file:
        # read n bytes from the file
        blob = data_file.read(n)

    run_echo_client(blob)

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["connection closed by server"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))

#-------------------------------------------------------------------------------
def test_network_api_bandwidth_64_Kbit(boot_with_proxy, benchmark):
    """
    Measure the send and receive speed of the echo server.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    # 64 Kbit of data
    num_chars =  8 * 1024

    # 10 Mbit of data
    # num_chars = 10 * 128 * 1024

    gen_str = ''.join(random.choice(string.ascii_letters) for i in range(num_chars))

    result = benchmark(run_echo_client, gen_str.encode())

    ret, text, expr_fail = logs.check_log_match_sequence(
        f_out,
        ["connection closed by server"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))

# ------------------------------------------------------------------------------
@pytest.mark.dependency(depends=server_dos_tests)
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

        # Start a thread to send all the data
        sendThread = threading.Thread(target=sock.sendall, args=(blob,))
        sendThread.start()

        # Look for the response
        while len(received_blob) < len(blob):
            # Try to read the whole frame
            received_blob += sock.recv(1600)
            # print('Received len is ' + str(len(received_blob)) + ' waiting for ' + str(len(blob)))

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
        sendThread.join()
        if not received_blob == blob:
            pytest.fail("Blobs mismatch")



#-------------------------------------------------------------------------------
# --- TCP TESTS ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
@pytest.mark.dependency(depends=server_dos_tests)
def test_network_tcp_connection_establishment(boot_with_proxy):
    """
    Test the SYN/ACK-SYN/ACK sequence with various sequence numbers, delays and
    lost packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    for i in range(10):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=2)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                   seq=s.seq+1, ack=sa.seq+1, flags='A')
        send(a)
        if not (sa.ack == s.ack + 1):
            pytest.fail("ACK mismatch")
        if not (a.ack == sa.seq+1):
            pytest.fail("ACK mismatch")


#-------------------------------------------------------------------------------
FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80
@pytest.mark.dependency(depends=server_dos_tests)
def test_network_tcp_connection_closure(boot_with_proxy):
    """
    Test the FIN sequence with various sequence numbers, delays and lost
    packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=5)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                   seq=s.seq+1, ack=sa.seq+1, flags='A')
        send(a)
        r = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                   seq=a.seq, ack=sa.seq+1, flags='F')
        p = sr1(r, timeout=5)
        if p is None:
            pytest.fail("Didn't receive FIN ack")
        if not (p.haslayer(TCP) and ((p['TCP'].flags & FIN) or (p['TCP'].flags & ACK))):
            pytest.fail("Didn't receive FIN")


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Fails due to picotcp not sending RST")
@pytest.mark.dependency(depends=server_dos_tests)
def test_network_tcp_connection_reset(boot_with_proxy):
    """
    Test the RST sequence with various sequence numbers, delays and lost
    packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=5)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                   seq=s.seq+1, ack=sa.seq+1, flags='A')
        send(a)
        #r = IP(dst=ETH_2_ADDR)/TCP(dport=5555,sport=source_port,seq=a.seq,ack=sa.seq+1,flags='RA')
        r = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                   seq=a.seq, ack=sa.seq+1, flags='R')
        p = sr1(r, timeout=30)
        if p is None:
            pytest.fail("Didn't receive RST ack")


#-------------------------------------------------------------------------------
def test_network_tcp_connection_invalid(boot_with_proxy):
    """
    Test connecting to a port nobody is listening on.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    for i in range(10):
        source_port = random.randint(10256, 65536)
        r = IP(dst=ETH_2_ADDR)/TCP(dport=source_port,
                                   sport=source_port, seq=0, ack=0, flags='S')
        p = sr1(r, timeout=30)
        if p is None:
            pytest.fail("No reply")
        if not (p.haslayer(ICMP) and p.payload.type == 3):
            pytest.fail("Received wrong message. Expected Port unreachable")


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented yet")
def test_network_tcp_window_size_scaling(boot_with_proxy):
    """
    Test the TCP window size scaling with various sequence numbers, delays and
    lost packets.
    """


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented yet")
def test_network_tcp_out_of_band_signaling(boot_with_proxy):
    """
    Test TCP Out of Band signaling various sequence numbers, delays and lost
    packets.
    """


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
@pytest.mark.dependency(depends=server_dos_tests)
def test_network_tcp_out_of_order_receive(boot_with_proxy):
    """
    Test receiving TCP packets out of order with various sequence numbers,
    delays and lost packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=2)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                   seq=s.seq+1, ack=sa.seq+1, flags='A')
        send(a)
        r = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                   seq=a.seq, ack=0, flags='')/"TTTTTTTT"
        p = sr1(r, timeout=2)

        r1 = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port,
                                    seq=p.ack, ack=p.seq+len(p), flags='')/"XXXXXXXX"
        p1 = sr1(r1, timeout=2)


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Fails due to payload mismatch")
@pytest.mark.dependency(depends=server_dos_tests)
def test_network_tcp_data_send(boot_with_proxy):
    """
    Test sending data in TCP pakets with various sequence numbers, delays and
    lost packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    for i in range(5):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555)/Raw(RandString(size=1))
        r = sr1(s, timeout=2)
        if not s.payload == r.payload:
             pytest.fail("Payload mismatch")


#-------------------------------------------------------------------------------
# --- DHCP TESTS ---
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented in TRENTOS")
def test_network_dhcp_get_address(boot_with_proxy):
    """
    Test getting a valid IP configuration from a DHCP server.
    """


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented in TRENTOS")
def test_network_dhcp_renew_address(boot_with_proxy):
    """
    Test renewing the IP address from a DHCP server.
    """


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented in TRENTOS")
def test_network_dhcp_expire_address(boot_with_proxy):
    """
    Test having the existing lease expiring while having active TCP connections.
    """


#-------------------------------------------------------------------------------
# --- ARP TESTS ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Fails in new network setup")
def test_network_arp_request(boot_with_proxy):
    """
    Test asking for the MAC address of a known host.
    """

    test_run = boot_with_proxy(test_system)
    filter = "arp and src host "+ETH_1_ADDR+" and dst host "+NET_GATEWAY
    p = sniff(iface='br0', filter=filter, timeout=60)
    f_out = test_run[1]
    if len(p) == 0:
        pytest.fail("Timeout waiting for arp request")
    p.show()


#-------------------------------------------------------------------------------
def test_network_arp_reply_client(boot_with_proxy):
    """Test if the client implementation component replies to arp request.
        Success: We get a valid arp reply
        Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    ans, uns = arping(ETH_1_ADDR)
    if len(uns) != 0:
        pytest.fail("Timeout waiting for arp reply")


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=server_dos_tests)
def test_network_arp_reply_server(boot_with_proxy):
    """Test if the server implementation component replies to arp request.
        Success: We get a valid arp reply
        Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    ans, uns = arping(ETH_2_ADDR)
    if len(uns) != 0:
        pytest.fail("Timeout waiting for arp reply")


#-------------------------------------------------------------------------------
# --- UDP TESTS ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def test_network_udp_recvfrom(boot_with_proxy):
    """
    Sends an UDP packet to the system, testing the recvfrom() call. It waits
    for the test system to reach the point where it waits for the test packet
    (signaled by the "UDP Receive test" string in the log). Afterwards it looks
    for the payload of the UDP packet in the output log.
    Success: The payload is found in the log
    Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["UDP Receive test"],
        timeout)
    r = IP(dst=ETH_1_ADDR)/UDP(dport=8888,sport=9999)/Raw(load="UDP recvfrom OK\0")
    send(r, iface = "br0")
    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["UDP recvfrom OK"],
        timeout)
    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))


#-------------------------------------------------------------------------------
def test_network_udp_sendto(boot_with_proxy):
    """
    Test and UDP packet to the system, testing recvfrom() and sendto() calls.
    It waits for the test system to reach the point where it waits for the test
    packet (signaled by the "UDP Send test" string in the log). Afterwards it
    waits for a response to the UDP packet it sent.
    Success: The response UDP packet is received
    Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["UDP Send test"],
        timeout)
    r = IP(dst=ETH_1_ADDR)/UDP(dport=8888,sport=9999)/Raw(load="UDP sendto OK\0")
    p = sr1(r, timeout=35, iface = "br0")
    if p is None:
        pytest.fail("Didn't receive UDP reply")

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))


#-------------------------------------------------------------------------------
# --- ICMP TESTS ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented in TRENTOS")
def test_network_ping_request(boot_with_proxy):
    """
    Test pinging a known host.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    filter = "icmp and src host "+ETH_1_ADDR+" and dst host "+CFG_TEST_HTTP_SERVER
    p = sniff(iface='br0', filter=filter, timeout=30)
    if len(p) == 0:
        pytest.fail("Timeout waiting for ping request")
    p.show()


#-------------------------------------------------------------------------------
def test_network_ping_reply_client(boot_with_proxy):
    """
    Test if the client implementation component replies to ping.
    Success: We get a valid ping reply
    Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    lost = 0
    for i in range(5):
        randNum = random.randint(0, 255)
        ans = sr1(IP(dst=ETH_1_ADDR)/ICMP(id=randNum), timeout=5)
        if ans == None:
            pytest.fail("Timeout waiting for ping reply")
        if not ans.payload.id == randNum:
            pytest.fail("Failed. We got a reply for a ping we didn't send.")


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=server_dos_tests)
def test_network_ping_reply_server(boot_with_proxy):
    """
    Test if the server implementation component replies to ping.
    Success: We get a valid ping reply
    Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    lost = 0
    for i in range(5):
        randNum = random.randint(0, 255)
        ans = sr1(IP(dst=ETH_2_ADDR)/ICMP(id=randNum), timeout=5)
        if ans == None:
            pytest.fail("Timeout waiting for ping reply")
        if not ans.payload.id == randNum:
            pytest.fail("Failed. We got a reply for a ping we didn't send.")


#-------------------------------------------------------------------------------
# --- API Tests ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def test_network_dataport_size_check_client(boot_with_proxy):
    """
    Test if the client network stack API handles invalid buffer sizes correctly.
    Success: We get test successful message in the log.
    Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Client dataport test successful"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))


#-------------------------------------------------------------------------------
def test_network_dataport_size_check_lib(boot_with_proxy):
    """
    Test if the library network stack API handles invalid buffer sizes
    correctly.
    Success: We get test successful message in the log.
    Failure: Timeout
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Lib dataport test successful"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))
