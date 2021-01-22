import time
import socket
from scapy.all import *
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
# timeout can be an integer or a Timeout_Checker object
def is_server_up(addr, sport, dport, responsiveness_timeout_sec, timeout_sec):

    """
    Checks whether the server at addr:dport is up. A TCP connection is opened,
    with a timeout. If the connection fail this is repeated over and over again
    until the overall time has expired.

    """

    # timeout_sec can be an integer or a Timeout_Checker object
    timeout = Timeout_Checker(timeout_sec)

    def get_max_remaining_time():
        return min(timeout.get_remaining(), responsiveness_timeout_sec)

    while not timeout.has_expired():

        sack = scapy.sendrecv.sr1(
                IP(dst = addr)/\
                TCP(dport = dport, sport = sport, flags = "S"),
                timeout = get_max_remaining_time())

        if sack is None:
            print('ERROR: connection failed, retrying')
            continue

        # we got a SYNACK. Close the connection, but ignore the result
        if not ack_and_fin(sack, get_max_remaining_time()):
            print('ERROR: ack_and_fin() failed')
        return True

    print('ERROR: could not connect to server')
    return False


#-------------------------------------------------------------------------------
def run_echo_client(server_ip, server_port, blob, timeout):

    print("starting echo client an connect to {}:{}".format(
            server_ip, server_port))

    server_address = (server_ip, server_port)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (sock is None):
        raise  Exception("could not get a socket")

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

    received_blob = b""
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
            raise Exception("Blobs mismatch")
