import pytest

import sys

import logs # logs module from the common directory in TA
import os
import re
import time
import threading
import socket


#-------------------------------------------------------------------------------
def throughput_str(cnt, delta):
    t = cnt / delta
    p = ''

    if (t > 1024):
        t = t / 1024
        p = 'K'

    if (t > 1024):
        t = t / 1024
        p = 'M'

    if (t > 1024):
        t = t / 1024
        p = 'G'

    if (t > 1024):
        t = t / 1024
        p = 'T'

    return '{:.2f} {}iB/s'.format(t, p)


#-------------------------------------------------------------------------------
def test_uart(boot):
    """
    Test UART data stream handling and throughput
    """


    arr = bytearray(range(256)) * 4  # array of 1 KiB
    loops = 4 * 1024 # send 4 MiB data,

    test_run = boot('')
    f_out = test_run[1]
    serial_socket = test_run[3]

    # synchronize with test application
    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            'UART tester loop running',
        ],
        2)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

    # send data
    t1 = time.time()
    for i in range(loops):
        serial_socket.send(arr)
    t2 = time.time()

    # due to a 2.5 MByte TCP buffer we see a TCP througput of 400 MiB/s if all
    # data can be cached there. For a larger amount things start to block and
    # the QEMU UART emulation determines the speed.
    print('Throughput TCP: ' + throughput_str(len(arr)*loops, t2-t1) )

    # at 36 KiByte/s this takes about 114 secs, but the latest UART driver
    # reaches up to 130 KiByte/s.
    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            'bytes processed: 0x400000',
        ],
        130)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

    t3 = time.time()
    delta = t3 - t1
    print('Throughput QEMU serial: {} (took {:.2f} secs)'.format(
            throughput_str(len(arr)*loops, delta),
            delta) )
