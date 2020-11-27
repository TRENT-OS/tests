from scapy.all import *

def ack_and_fin(sack, tcp_template=None):

    """Given a SYNACK packet received from a prio SYN sent it does follow up
        with an ACK and close the connection with FIN. Return true if every
        packet receive an answer"""

    ack         = None
    fack        = None
    lack        = None

    if sack is None:
        print('cannot perform ack_and_fin() without sack')
        return False

    if tcp_template is None:
        tcp_layer = TCP()
    else:
        tcp_layer = tcp_template

    tcp_layer.dport = sack.sport
    tcp_layer.sport = sack.dport
    tcp_layer.flags = "A"
    tcp_layer.seq   = sack.ack
    tcp_layer.ack   = sack.seq + 1

    ack = sr1(IP(dst = sack[IP].src)/tcp_layer, timeout=10)
    if ack is None:
        print('no ack received')
        return False

    tcp_layer.flags = "FA"

    fack = sr1(IP(dst = sack[IP].src)/tcp_layer, timeout=10)
    if fack is None:
        print('no fack received')
        return False

    tcp_layer.flags     = "A"
    tcp_layer.seq       = fack.ack
    tcp_layer.ack       = fack.seq + 1

    lack = sr1(IP(dst = sack[IP].src)/tcp_layer, timeout=10)

    return True

def is_server_up(addr, sport, dport, timeout_sec):

    """Checks whether the server at addr:dport is up or not until either the
        server responds or the timeout expires. Returns True if the server
        answered in time."""

    from time import time

    time_expired = time() + timeout_sec
    while True:
        sack = sr1(IP(dst = addr)/\
                    TCP(dport = dport,\
                        sport = sport,\
                        flags = "S"),\
                    timeout=10)
        if sack is not None:
            ack_and_fin(sack)
            return True
        if time() > time_expired:
            return False
