from scapy.all import *

def ack_and_fin(sack):
    ack     = None
    fack    = None
    lack    = None

    ack = sr1(IP(dst = sack[IP].src)/\
                TCP(dport = sack.sport,\
                    sport = sack.dport,\
                    flags = "A",\
                    seq=sack.ack,\
                    ack=sack.seq + 1),\
                timeout=10)
    if ack is not None:
        fack = sr1(IP(dst = sack[IP].src)/\
                    TCP(dport = sack.sport,\
                        sport = sack.dport,\
                        flags = "FA",\
                        seq=sack.ack,\
                        ack=sack.seq + 1),\
                    timeout=10)
    if fack is not None:
        lack = sr1(IP(dst = sack[IP].src)/\
                    TCP(dport = sack.sport,\
                        sport = sack.dport,\
                        flags = "A",\
                        seq=fack.ack,\
                        ack=fack.seq + 1),\
                    timeout=10)

def is_server_up(addr, sport, dport, timeout):
    from time import time

    time_expired = time() + timeout
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
