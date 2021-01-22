import time
import socket
from scapy.all import *
import board_automation.tools
from board_automation.tools import Timeout_Checker

#-------------------------------------------------------------------------------
# timeout can be an integer or a Timeout_Checker object
def ack_and_fin(sack, timeout_sec, tcp_template=None):

    """
    Given a SYNACK packet was received from a previous SYN sent, this function
    will send an ACK and close the connection with FIN. Returns true if every
    packet receive the expected answer.
    """

    if sack is None:
        print('cannot perform ack_and_fin() without sack')
        return False

    timeout = Timeout_Checker(timeout_sec)

    tcp_layer = TCP() if tcp_template is None else tcp_template
    tcp_layer.dport = sack.sport
    tcp_layer.sport = sack.dport
    tcp_layer.flags = "A"
    tcp_layer.seq   = sack.ack
    tcp_layer.ack   = sack.seq + 1

    # send the ACK for the SYNACK
    scapy.sendrecv.send(IP(dst = sack[IP].src)/tcp_layer)

    # send the FIN and wait for FINACK
    tcp_layer.flags = "FA"
    fack = scapy.sendrecv.sr1(
            IP(dst = sack[IP].src)/tcp_layer,
            timeout = timeout.get_remaining())
    if fack is None:
        print('no FINACK received')
        return False

    tcp_layer.flags = "A"
    tcp_layer.seq   = fack.ack
    tcp_layer.ack   = fack.seq + 1

    # send the last ACK
    scapy.sendrecv.send(IP(dst = sack[IP].src)/tcp_layer)

    return True


#-------------------------------------------------------------------------------
# timeout_sec can be an integer or a Timeout_Checker object.
# ICMP Echo packet uses the 32 bit header data filed for a 16 bit ID and
# 16 bis sequence number field.
def do_single_network_ping(target_ip, timeout_sec=None, id=None, seq=None):

    timeout = Timeout_Checker(timeout_sec)

    # ping is an ICMP echo packet
    ping_pkt = scapy.layers.inet.IP(dst = target_ip)/\
               scapy.layers.inet.ICMP(
                    type = 8, # ICMP ECHO
                    code = 0,
                    id = 0 if id is None else id,
                    seq = 0 if seq is None else seq)

    #print('ping {} (id={:#04x}, seq={})'.format(
    #        target_ip, ping_pkt[ICMP].id, ping_pkt[ICMP].seq))

    resp = scapy.sendrecv.sr1(
            ping_pkt,
            timeout = None if timeout.is_infinite() \
                      else timeout.get_remaining())

    if resp is None:
        print('ERROR: ping to {} timeout'.format(target_ip))
        return False

    # this should never happen, because scapy gives us the proper response
    if not (resp.haslayer(ICMP)):
        print('ERROR: ping to {} returned no ICMP packet'.format(target_ip))
        return False

    if (resp[ICMP].id != ping_pkt[ICMP].id):
        print('ERROR: ping to {} response ID mismatch, got {}, expected {}'.format(
                    target_ip, resp[ICMP].id, ping_pkt[ICMP].id) )
        return False

    if (resp[ICMP].seq != ping_pkt[ICMP].seq):
        print('ERROR: ping to {} response SEQ mismatch, got {}, expected {}'.format(
                    target_ip, resp[ICMP].seq, ping_pkt[ICMP].seq) )
        return False

    # ping was successful
    return True


#-------------------------------------------------------------------------------
# timeout_sec can be an integer or a Timeout_Checker object
# ping_timeout_sec is an integer
def do_network_ping(target_ip, cnt=1, timeout_sec=None):

    timeout = Timeout_Checker(timeout_sec)

    # pick a random number for the 16 bit ID field.
    icmp_id = random.randrange(0x10000)

    for i in range(cnt):

        if timeout.has_expired():
            print('ERROR: timeout reached after {}/{} pings', i, cnt)
            return False

        # take all the remaining time for the next ping, currently there is no
        # need to support a timeout for each ping.
        if not do_single_network_ping(
                    target_ip,
                    id = icmp_id,
                    seq = i,
                    timeout_sec = None if timeout.is_infinite() \
                                  else timeout.get_remaining()):
            print('ERROR: ping {}/{} to {} failed', i+1, cnt, target_ip)
            return False

    # all pings were successful
    return True


#-------------------------------------------------------------------------------
# timeout can be an integer or a Timeout_Checker object
def is_server_up(target_ip, port, timeout_sec):

    """
    Checks whether the server is up and a TCP connection can be opened on the
    given port. If the connection fails this is repeated over and over again
    until the overall time has expired.

    """

    timeout = Timeout_Checker(timeout_sec)

    # try to ping the remote server
    icmp_id = random.randrange(0x10000)
    seq = 0
    while True:

        if timeout.has_expired():
            print('ERROR: giving up reaching {} via ping'.format(target_ip))
            return False

        # ping must answer within 30 secs
        if do_single_network_ping(
                    target_ip,
                    id = icmp_id,
                    seq = seq,
                    timeout_sec = timeout.sub_timeout(30).get_remaining()):
            # ping worked
            break;

        print('ERROR: could not ping {}'.format(target_ip))
        seq += 1
        # continue loop and try another ping


    # try to open a TCP connection
    while True:

        if timeout.has_expired():
            print('ERROR: giving reaching {}:{} via TCP'.format(
                    target_ip, port))
            return False

        # open a connection, automatically close it when this block if left
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if (sock is None):
                print('ERROR: could not create socket')
                # we consider this a fatal error and don't retry
                return False

            # TCP connection must be set up within 30 secs
            sock.settimeout( timeout.sub_timeout(30).get_remaining() )
            try:
                sock.connect( (target_ip, port) )

            except Exception as e:
                print('ERROR: could not connect to {}:{}'.format(
                        target_ip, port))
                return False

            # TCP connection worked
            break;

    # server seems up and running
    return True


#-------------------------------------------------------------------------------
def run_echo_client(server_ip, server_port, blob, timeout):

    print('starting echo client, connect to {}:{} and send {} bytes'.format(
            server_ip, server_port, len(blob)))

    server_address = (server_ip, server_port)

    received_blob = b""

    def get_throughput_str(data_len, time_elapsed):
        scale_str = 'KMGTPEZY'
        unit = 'Byte'
        factor = 0
        thoughput = (data_len) / time_elapsed
        while (thoughput >= 1024):
            thoughput /= 1024
            unit = '{}iB'.format(scale_str[factor])
            factor += 1
            if factor >= len(scale_str): break

        return '{:.1f} {}/s'.format(thoughput, unit)

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        if (sock is None):
            raise Exception('could not get a socket')

        sock.settimeout(timeout)

        cnt = 3
        for attempt in range(cnt):
            try:
                sock.connect(server_address)
                break
            except:
                print('connection failed ({}/{}), retry in 2 seconds'.format(
                        attempt+1, cnt))
                time.sleep(2)
        else:
            raise Exception('could not connect to server')

        # send data in a thread, we check what is echoed back in parallel
        def echo_client_thread(thread):
            send_start = time.time()
            sock.sendall(blob)
            time_elapsed = time.time() - test_time_base
            print('sending done, {:.0f} ms, throughput {}'.format(
                    time_elapsed * 1000,
                    get_throughput_str(len(blob), time_elapsed) ))


        received_blob = b''
        time_elapsed = 0
        test_time_base = time.time()
        # start thread and keep receiving
        t = board_automation.tools.run_in_thread(echo_client_thread)
        while (len(blob) > len(received_blob)):
            received_part = sock.recv(len(blob) - len(received_blob))
            time_elapsed = time.time() - test_time_base
            if (0 == len(received_part)):
                raise Exception('receive timeout')
            received_blob += received_part
            # print('received {} new bytes, overall {}/{} byte(s), throughput {}'.format(
            #         len(received_part),
            #         len(received_blob),
            #         len(blob),
            #         get_throughput_str(len(blob), time_elapsed) ))

        # wait for thread to finish
        #print('syncing with sender thread')
        t.join()

    print('echo test for {} bytes took {:.0f} ms, throughput {}'.format(
            len(blob),
            time_elapsed * 1000,
            get_throughput_str(len(blob), time_elapsed) ))

    if not received_blob == blob:
        raise Exception("received data does not match sent data")
