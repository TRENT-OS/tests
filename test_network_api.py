import sys
import threading
import time
import random
import pathlib
import os
import shutil
import string
import re
import struct
import socket
import http.server
import socketserver
import distutils.util

import pytest
from pytest_testconfig import config

import logs # logs module from the common directory in TA
import test_parser as parser
from test_network_api_functions import *
from board_automation.tools import Timeout_Checker

from scapy.all import *
# This python file is imported by pydoc which sometimes throws an error about a
# missing IPv6 default route (if the machine building the documentation doesn't
# have it set). To remove this warning we disable IPv6 support in scapy, since
# we don't use it at this time.
from scapy.config import conf
conf.ipv6_enabled = False
conf.verb = 0  # don't print anything from scapy


#-------------------------------------------------------------------------------
# configure in which interface to send out the packets.
conf.iface = "br0"
test_system = "test_network_api"

NET_GATEWAY = "10.0.0.1"

# get the variables from a platform specific configuration file passed to
# pytest-testconfig. In case the keys don't exist in the config file or the
# variables have invalid types/values, raise an exception and stop the test
# execution
try:
    uart_connected = bool(distutils.util.strtobool(config['platform']['uart_connected']))

    timeout = int(config['platform']['timeout'])

    client_ip = config['network']['client_ip']
    socket.inet_aton(client_ip)

    server_ip = config['network']['server_ip']
    socket.inet_aton(server_ip)

    container_gateway_ip = config['network']['container_gateway_ip']
    socket.inet_aton(container_gateway_ip)
except:
    pytest.fail("Invalid configuration value")

# true if there is no UART channel to the system being tested. The tests that
# rely on parsing the output to succeed are skipped.
uart_nc = not uart_connected

# ToDo: could make some tests depend on DoS test results
# server_dos_tests = [
#     'test_tcp_options_poison',
#     'test_tcp_header_length_poison'
# ]


#-------------------------------------------------------------------------------
# --- API Tests ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
def test_network_dataport_size_check_client(boot_with_proxy):
    """
    Test if the client network stack API handles invalid buffer sizes correctly.
    Success: We get test successful message in the log.
    Failure: Timeout
    """

    parser.check_test(
        boot_with_proxy(test_system),
        timeout,
        'test_dataport_size_check_client_functions')

#-------------------------------------------------------------------------------
@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
def test_network_dataport_size_check_lib(boot_with_proxy):
    """
    Test if the library network stack API handles invalid buffer sizes
    correctly.
    Success: We get test successful message in the log.
    Failure: Timeout
    """

    parser.check_test(
        boot_with_proxy(test_system),
        timeout,
        'test_dataport_size_check_client_functions')

#-------------------------------------------------------------------------------
@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
def test_socket_create_neg(boot_with_proxy):
    """
    Test if the library network stack API create() function behave as expected
    in negative cases.
    Success: We get test successful message in the log.
    Failure: asserts in the log
    """

    parser.check_test(
        boot_with_proxy(test_system),
        timeout,
        'test_socket_create_neg')

#-------------------------------------------------------------------------------
@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
def test_socket_create_pos(boot_with_proxy):
    """
    Test if the library network stack API create() function behave as expected
    in positive cases.
    Success: We get test successful message in the log.
    Failure: asserts in the log
    """

    parser.check_test(
        boot_with_proxy(test_system),
        timeout,
        'test_socket_create_pos')

#-------------------------------------------------------------------------------
# --- BlackBox Tests ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def test_network_basic(boot_with_proxy):
    """Check to see if scapy is running correctly """

    target_ip = container_gateway_ip

    for i in range(5):
        randNum = random.randint(0, 255)
        ans = sr1(IP(dst=target_ip)/ICMP(id=randNum), timeout=1)
        if ans is None:
            pytest.fail("Timeout waiting for ping reply")
        if not ans.payload.id == randNum:
            pytest.fail("Failed we got a reply for a ping we didn't send.")


#-------------------------------------------------------------------------------
def test_tcp_options_poison(boot_with_proxy):

    """
    Test for CVE-2020-24337, send a malformed packet with TCP options set to
    "0xFF 0x00 0x00 0x00". Some TCP/IP implementation can't process this and
    may crash or loop infinitely trying to parse it. The test requires a server
    listening on port 5555. If no answer occurs the server's TCP stack should
    be considered affected by the issue.
    The PicoTCP version used in TRENTOS will ignore the broken TCP options in
    the malformed SYN packet used in this test and respond with a SYNACK, so
    the connection can be opened.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip
    dport = 5555

    # RFC793 defines for the TCP option field, that there are two kinds of
    # options. Singe-byte options and options with one byte type, one byte
    # length and the length-2 data bytes. The option type defines if there is
    # data or not. Option type 0 ('EOL') is a single-byte option that indicates
    # the end of the option list. Option type 1 ('NOP') is also single-byte an
    # is a dummy that does nothing. The whole options field is padded with zeros
    # to a multiple of 4 bytes. A list of all defined options can be found at
    # https://www.iana.org/assignments/tcp-parameters/tcp-parameters.xhtml and
    # the definition is, that all option types besides 0 and 1 must have a
    # length field.
    # For this test we first create a TCP payload with an the (undefined) option
    # 0xff without any data, which results in the raw data 0xff 0x02. Scapy will
    # automatically appends an option 'EOL' there which is "0x00" as raw data.
    # Since the option field starts at offset 20 in the TCP data and its length
    # is padded with zeros to a multiple of 4, the resulting option field will
    # be "0xff 0x02 0x00 0x00".
    tcp_template = scapy.layers.inet.TCP(
                    dport   = dport,
                    sport   = random.randint(1025, 65535),
                    seq     = 0,
                    options = [(0xff, b'')], # option 0xff with no data
                    flags   = "S")

    # get the raw template, ie no checksum are calculated yet
    raw_tcp_template = bytearray(raw(tcp_template))

    # change option field from "0xff 0x02 0x00 0x00" to "0xff 0x00 0x00 0x00"
    if (0x02 != raw_tcp_template[-3]):
        pytest.fail('TCP template option 0xFF length is not 0x02')

    raw_tcp_template[-3] = 0

    # set TCP header checksum (at offset 16, big endian)
    if (0 != struct.unpack_from('>H', raw_tcp_template, 16)[0]):
        pytest.fail('TCP template checksum is not 0')

    tcp_checksum = in4_chksum(
                        socket.IPPROTO_TCP,
                        IP(dst = target_ip),
                        raw_tcp_template)
    struct.pack_into('>H', raw_tcp_template, 16, tcp_checksum)
    # print(raw_tcp_template.hex(' '))

    # try setting up a connection with the malformed TCP payload
    if not do_tcp_poisoned_syn(
                target_ip,
                dport,
                TCP(raw_tcp_template),
                Timeout_Checker(30)):
        pytest.fail('poisoning test failed for server {}:{}'.format(
                            target_ip, dport))


#-------------------------------------------------------------------------------
def test_tcp_header_length_poison(boot_with_proxy):

    """
    Test for CVE-2020-24341, send a malformed packet with the invalid TCP header
    length "0xF". Some TCP/IP implementation may crash then. The test requires a
    server listening on port 5555. If no answer occurs the server's TCP stack is
    considered affected by the issue.
    The PicoTCP version used in TRENTOS will drop the malformed SYN from this
    test and thus opening a connection will result in a timeout.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip
    dport = 5555

    # create a TCP SYN packet with invalid data offset 0xf
    tcp_template = scapy.layers.inet.TCP(
                    dport   = dport,
                    sport   = random.randint(1025, 65535),
                    seq     = 0,
                    dataofs = 0xf,
                    flags   = "S")

    # try setting up a connection with the malformed TCP payload
    if not do_tcp_poisoned_syn(
                target_ip,
                dport,
                tcp_template,
                Timeout_Checker(30)):
        pytest.fail('poisoning test failed for server {}:{}'.format(
            target_ip, dport))


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented yet")
def test_network_picotcp_unit_tests(boot_with_proxy):
    """Execute all picotcp unit tests"""


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented yet")
def test_network_picotcp_smoke_tests(boot_with_proxy):
    """Execute all picotcp smoke tests"""


#-------------------------------------------------------------------------------
@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
def test_network_api_client(boot_with_proxy):
    """
    Test multisocket implementation. Two applications sharing a network stack
    try each to open 16 sockets and download data from the webserver running in
    the test container. The library signals when all sockets are in use.
    """

    test_run = boot_with_proxy(test_system)

    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    src = pathlib.Path(__file__).parent.absolute().joinpath('test_network_api/')

    dest = '/tmp/test_network_api'

    if(os.path.exists(dest)):
        shutil.rmtree(dest)

    shutil.copytree(src, dest)

    (ret, text, expr_fail) = logs.check_log_match_set(
        f_out,
        ["No free sockets available 16", "!!! test_tcp_client: OK"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))

    shutil.rmtree(dest)


#-------------------------------------------------------------------------------
# at the moment the stack can handle these sizes without issues. We will
# increase this sizes and fix the issues in a second moment.
lst = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
@pytest.mark.parametrize('n', lst)
def test_network_api_echo_server(boot_with_proxy, n):
    """
    Test TCP/IP stack with a server that echoes the data sent to it in blocks.
    The test is repeated using blocks of different sizes.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip
    target_port = 5555

    src = pathlib.Path(__file__).parent.absolute().joinpath(
        'test_network_api/dante.txt')

    with open(src, 'rb') as data_file:
        # read n bytes from the file
        blob = data_file.read(n)

    try:
        run_echo_client(target_ip, target_port, blob, timeout)
    except Exception as e:
        pytest.fail(
            'run_echo_client for {}:{} failed with exception {}'.format(
                target_ip, target_port, e))

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
    parser.fail_on_assert(f_out)

    target_ip = server_ip
    target_port = 5555

    def do_run_echo_client():
        num_chars =  8 * 1024 # 64 Kbit of data
        # num_chars = 10 * 128 * 1024 # 10 Mbit of data
        gen_str = ''.join(random.choice(string.ascii_letters) for i in range(num_chars))
        try:
            run_echo_client(target_ip, target_port, gen_str.encode(), timeout)
        except Exception as e:
            pytest.fail(
                'run_echo_client for {}:{} failed with exception {}'.format(
                    target_ip, target_port, e))

    benchmark(do_run_echo_client)

    ret, text, expr_fail = logs.check_log_match_sequence(
        f_out,
        ["connection closed by server"],
        timeout)

    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))


#-------------------------------------------------------------------------------
# --- TCP TESTS ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#@pytest.mark.skip(reason="Fails due to test enviroment sending RST")
def test_network_tcp_connection_establishment(boot_with_proxy):
    """
    Test the SYN/ACK-SYN/ACK sequence with various sequence numbers, delays and
    lost packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    for i in range(10):
        source_port = random.randint(1025, 65536)
        s = IP(dst=target_ip)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=2)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
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
def test_network_tcp_connection_closure(boot_with_proxy):
    """
    Test the FIN sequence with various sequence numbers, delays and lost
    packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=target_ip)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=5)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
                                   seq=s.seq+1, ack=sa.seq+1, flags='A')
        send(a)
        r = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
                                   seq=a.seq, ack=sa.seq+1, flags='F')
        p = sr1(r, timeout=5)
        if p is None:
            pytest.fail("Didn't receive FIN ack")
        if not (p.haslayer(TCP) and ((p['TCP'].flags & FIN) or (p['TCP'].flags & ACK))):
            pytest.fail("Didn't receive FIN")


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Fails due to picotcp not sending RST")
def test_network_tcp_connection_reset(boot_with_proxy):
    """
    Test the RST sequence with various sequence numbers, delays and lost
    packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=target_ip)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=5)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
                                   seq=s.seq+1, ack=sa.seq+1, flags='A')
        send(a)
        #r = IP(dst=target_ip)/TCP(dport=5555,sport=source_port,seq=a.seq,ack=sa.seq+1,flags='RA')
        r = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
                                   seq=a.seq, ack=sa.seq+1, flags='R')
        p = sr1(r, timeout=30)
        if p is None:
            pytest.fail("Didn't receive RST ack")


#-------------------------------------------------------------------------------
def test_network_tcp_connection_invalid(boot_with_proxy):
    """
    Test connecting to a port nobody is listening on. RFC792 says a host MAY
    send a destination unreachable message. RFC1122 says a host SHOULD generate
    a destination unreachable messages with code 2 (Protocol Unreachable), when
    the designated transport protocol is not supported or 3 (Port Unreachable),
    when the designated transport protocol (e.g., UDP) is unable to demultiplex
    the datagram but has no protocol mechanism to inform the sender.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    for i in range(10):
        source_port = random.randint(1025, 65536)
        r = IP(dst=target_ip)/TCP(dport=source_port,
                                   sport=source_port, seq=0, ack=0, flags='S')
        p = sr1(r, timeout=30)
        if p is None:
            # actually, this in not a failure, because the host is not required
            # to send anything, it just "may" (RFC792) or "should" (RFC1122).
            pytest.fail("timeout waiting for ICMP message PORT_UNREACHABLE")

        if not p.haslayer(ICMP):
            pytest.fail("expected ICMP message PORT_UNREACHABLE, got something else")

        ICMP_PORT_UNREACHABLE = 3
        if (ICMP_PORT_UNREACHABLE != p.payload.type):
            pytest.fail(
                "expected ICMP message with PORT_UNREACHABLE ({}), got {}".format(
                    ICMP_PORT_UNREACHABLE, p.payload.type) )


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
def test_network_tcp_out_of_order_receive(boot_with_proxy):
    """
    Test receiving TCP packets out of order with various sequence numbers,
    delays and lost packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    for i in range(1):
        source_port = random.randint(1025, 65536)
        s = IP(dst=ETH_2_ADDR)/TCP(dport=5555, sport=source_port, flags='S')
        sa = sr1(s, timeout=2)

        if sa is None:
            pytest.fail("Didn't receive SYN/ACK")

        a = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
                                   seq=s.seq+1, ack=sa.seq+1, flags='A')
        send(a)
        r = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
                                   seq=a.seq, ack=0, flags='')/"TTTTTTTT"
        p = sr1(r, timeout=2)
        if p is None:
            pytest.fail(
                'Timeout waiting for reply to first segment for packet {}'.format(i))

        r1 = IP(dst=target_ip)/TCP(dport=5555, sport=source_port,
                                    seq=p.ack, ack=p.seq+len(p), flags='')/"XXXXXXXX"
        p1 = sr1(r1, timeout=2)
        if p1 is None:
            pytest.fail(
                'Timeout waiting for reply to second segment for packet {}'.format(i))


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Fails due to payload mismatch")
def test_network_tcp_data_send(boot_with_proxy):
    """
    Test sending data in TCP pakets with various sequence numbers, delays and
    lost packets.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    for i in range(5):
        source_port = random.randint(1025, 65536)
        s = IP(dst=target_ip)/TCP(dport=5555)/Raw(RandString(size=1))
        r = sr1(s, timeout=2)
        if r is None:
            pytest.fail('Timeout waiting for reply to packet {}'.format(i))

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
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = client_ip

    filter = "arp and src host "+target_ip+" and dst host "+NET_GATEWAY
    p = sniff(iface='br0', filter=filter, timeout=60)

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
    parser.fail_on_assert(f_out)

    target_ip = client_ip

    ans, uns = arping(target_ip)
    if len(uns) != 0:
        pytest.fail("Timeout waiting for arp reply")


#-------------------------------------------------------------------------------
def test_network_arp_reply_server(boot_with_proxy):
    """Test if the server implementation component replies to arp request.
        Success: We get a valid arp reply
        Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    ans, uns = arping(target_ip)
    if len(uns) != 0:
        pytest.fail("Timeout waiting for arp reply")


#-------------------------------------------------------------------------------
# --- UDP TESTS ---
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
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
    parser.fail_on_assert(f_out)

    target_ip = client_ip

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["UDP Receive test"],
        timeout)
    r = IP(dst=target_ip)/UDP(dport=8888,sport=9999)/Raw(load="UDP recvfrom OK\0")
    send(r, iface = "br0")
    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["UDP recvfrom OK"],
        timeout)
    if not ret:
        pytest.fail("Missing: %s" % (expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.skipif(uart_nc, reason="Target UART not connected to test env")
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
    parser.fail_on_assert(f_out)

    target_ip = client_ip

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["UDP Send test"],
        timeout)
    r = IP(dst=target_ip)/UDP(dport=8888,sport=9999)/Raw(load="UDP sendto OK\0")
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
    parser.fail_on_assert(f_out)

    target_ip = client_ip

    filter = "icmp and src host "+target_ip+" and dst host "+CFG_TEST_HTTP_SERVER
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
    parser.fail_on_assert(f_out)

    target_ip = client_ip

    # must do 5 successful pings in 15 seconds
    if not do_network_ping(target_ip, cnt=5, timeout_sec=15):
        pytest.fail('could not ping {}'.format(target_ip))


#-------------------------------------------------------------------------------
def test_network_ping_reply_server(boot_with_proxy):
    """
    Test if the server implementation component replies to ping.
    Success: We get a valid ping reply
    Failure: Timeout
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    parser.fail_on_assert(f_out)

    target_ip = server_ip

    # must do 5 successful pings in 15 seconds
    if not do_network_ping(target_ip, cnt=5, timeout_sec=15):
        pytest.fail('could not ping {}'.format(target_ip))
