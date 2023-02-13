import time
import socket
from scapy.all import *
import board_automation.tools
from board_automation.tools import Timeout_Checker


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

    #print(f'ping {target_ip} (id={ping_pkt[ICMP].id:#04x}, seq={ping_pkt[ICMP].seq})')

    resp = scapy.sendrecv.sr1(
            ping_pkt,
            timeout = None if timeout.is_infinite() \
                      else timeout.get_remaining())

    if resp is None:
        print(f'ERROR: ping to {target_ip} timeout')
        return False

    # this should never happen, because scapy gives us the proper response
    if not (resp.haslayer(ICMP)):
        print(f'ERROR: ping to {target_ip} returned no ICMP packet')
        return False

    if (resp[ICMP].id != ping_pkt[ICMP].id):
        print(f'ERROR: ping to {target_ip} response ID mismatch, got {resp[ICMP].id}, expected {ping_pkt[ICMP].id}')
        return False

    if (resp[ICMP].seq != ping_pkt[ICMP].seq):
        print(f'ERROR: ping to {target_ip} response SEQ mismatch, got {resp[ICMP].seq}, expected {ping_pkt[ICMP].se}')
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
            print(f'ERROR: timeout reached after {i}/{cnt} pings')
            return False

        # take all the remaining time for the next ping, currently there is no
        # need to support a timeout for each ping.
        if not do_single_network_ping(
                    target_ip,
                    id = icmp_id,
                    seq = i,
                    timeout_sec = None if timeout.is_infinite() \
                                  else timeout.get_remaining()):
            print(f'ERROR: ping {i+1}/{cnt} to {target_ip} failed')
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
            print(f'ERROR: giving up reaching {target_ip} via ping')
            return False

        # ping must answer within 30 secs
        if do_single_network_ping(
                    target_ip,
                    id = icmp_id,
                    seq = seq,
                    timeout_sec = timeout.sub_timeout(30).get_remaining()):
            # ping worked
            break;

        print(f'ERROR: could not ping {target_ip}')
        seq += 1
        # continue loop and try another ping


    # try to open a TCP connection
    while True:

        if timeout.has_expired():
            print(f'ERROR: giving reaching {target_ip}:{port} via TCP')
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
                print(f'ERROR: could not connect to {target_ip}:{port}')
                return False

            # TCP connection worked
            break;

    # server seems up and running
    return True


#-------------------------------------------------------------------------------
def do_tcp_poisoned_syn(target_ip, port, syn_payload, timeout_sec):

    timeout = Timeout_Checker(timeout_sec)

    if not is_server_up(target_ip, port, timeout.sub_timeout(30)):
        print(f'server {target_ip}:{port} seems down (before poisoning)')
        return False

    # server is up, now poison it
    print(f'Server {target_ip}:{port} is up, try poisoning...')

    ip_frame = scapy.layers.inet.IP(dst = target_ip)
    tcp_layer = syn_payload

    syn_resp = scapy.sendrecv.sr1(
                    ip_frame/tcp_layer,
                    timeout = timeout.sub_timeout(20).get_remaining())
    if syn_resp is None:
        print('No answer, maybe server dropped poisoned packet')
        # if poisoning was successful, the server will no longer respond now
    else:
        tcp_flags = syn_resp[TCP].flags
        print(f'server responded to poisoned SYN with <{tcp_flags}>')

        if not (tcp_flags.A):
            print('SYN response: no ACK flag set')

        else:
            # merge SYN-ACK-ACK and FIN into one packet
            del tcp_layer.chksum
            tcp_layer.seq   += 1
            tcp_layer.ack   = syn_resp.seq + 1
            tcp_layer.flags = "FA"

            print('send SYN-ACK-ACK + FIN')
            fin_resp = scapy.sendrecv.sr1(
                            ip_frame/tcp_layer,
                            timeout = timeout.sub_timeout(20).get_remaining())
            if fin_resp is None:
                print('no FIN-ACK received')
            else:

                tcp_flags = fin_resp[TCP].flags # may have RST set besides ACK
                print(f'resp flags: {tcp_flags}')

                if not (tcp_flags.A): print('FIN response: no ACK flag set')

                if not (tcp_flags.F):
                    print('FIN response: no FIN flag set')
                else:
                    # send the last ACK
                    del tcp_layer.chksum
                    tcp_layer.seq   += 1
                    tcp_layer.ack   = fin_resp.seq + 1
                    tcp_layer.flags = "A"

                    print('send FIN-ACK')
                    scapy.sendrecv.send(ip_frame/tcp_layer)

        # if we arrive here the server accepted the poisoned handshake, so it
        # should be able to accept a normal TCP connection

    # if we arrive here, there was either no response after sending the poisoned
    # packet of the handshake when well and we have closed the connection.
    print('Check if server survived the poisoning')
    # ToDo; we should not just check if we can establish a connection, but also
    #       pipe some data though the echo server to check things are really
    #       well.
    if not is_server_up(target_ip, port, timeout.sub_timeout(30)):
        print(f'server {target_ip}:{port} seems down (before poisoning)')
        return False

    # seems the poisoned packet did not make server unresponsive
    return True


#-------------------------------------------------------------------------------
def run_echo_client_tcp(server_ip, server_port, blob, timeout):

    def get_throughput_str(data_len, time_elapsed):
        scale_str = 'KMGTPEZY'
        unit = 'Byte'
        factor = 0
        thoughput = (data_len) / time_elapsed
        while (thoughput >= 1024):
            thoughput /= 1024
            unit = f'{scale_str[factor]}iB'
            factor += 1
            if factor >= len(scale_str): break

        return f'{thoughput:.1f} {unit}/s'

    # send data in a thread, we check what is echoed back in parallel
    def echo_client_thread(thread):
        send_start = time.time()
        sock.sendall(blob)
        time_elapsed = time.time() - send_start
        print(f'sending done, {(time_elapsed*1000):.0f} ms, throughput ' + \
              get_throughput_str(len(blob), time_elapsed))

    print(f'starting echo client, connect to {server_ip}:{server_port} and send {len(blob)} bytes')

    server_address = (server_ip, server_port)
    received_blob = b""
    time_elapsed = 0

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        if (sock is None):
            raise Exception('could not get a socket')

        sock.settimeout(timeout)

        cnt = 3
        retry_timeout = 2
        for attempt in range(cnt):
            try:
                sock.connect(server_address)
                break
            except:
                print(f'connection failed ({attempt+1}/{cnt}), retry in {retry_timeout} seconds')
                time.sleep(retry_timeout)
        else:
            raise Exception('could not connect to server')

        # start thread and keep receiving
        t = board_automation.tools.run_in_thread(echo_client_thread)
        test_time_base = time.time()
        while (len(blob) > len(received_blob)):
            received_part = sock.recv(len(blob) - len(received_blob))
            time_elapsed = time.time() - test_time_base
            if (0 == len(received_part)):
                raise Exception('receive timeout')
            received_blob += received_part
            #throughput =
            #print(f'received {len(received_part)} new bytes, overall ' + \
            #      f'{len(received_blob)}/{len(blob),} byte(s), throughput ' + \
            #      get_throughput_str(len(blob), time_elapsed))

        # wait for thread to finish
        #print('syncing with sender thread')
        t.join()

    print(f'echo test for {len(blob)} bytes took {(time_elapsed*1000):.0f} ms, ' + \
          'throughput ' + get_throughput_str(len(blob), time_elapsed))

    if not received_blob == blob:
        raise Exception("received data does not match sent data")

#-------------------------------------------------------------------------------
def run_echo_client_udp(server_ip, server_port, blob, timeout):

    print(f'Starting echo client, connect to {server_ip}:{server_port} and send {len(blob)} bytes')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def echo_client_thread(thread):
        time.sleep(1)
        s.sendto(blob,(server_ip, server_port))


    s.bind(("0.0.0.0", server_port))

    s.settimeout(timeout)

    t = board_automation.tools.run_in_thread(echo_client_thread)

    try:
        received_blob, addr = s.recvfrom(len(blob)) # buffer size is 1024 bytes
    except socket.timeout:
        raise Exception("Socket timeout")

    t.join()

    if not received_blob == blob:
        raise Exception("Received data does not match sent data")
