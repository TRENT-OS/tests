import pytest

import sys

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

    test_runner = boot(None)[0]

    # synchronize with test application, timeout is 10 secs based on empirical
    # evidence. System load can likely impact this timing.
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'UART tester loop running',
            'initialize UART ok',
        ],
        10)

    if not ret:
        pytest.fail('could not detect test start')

    serial_socket = test_runner.get_serial_socket()

    # send data all at once, may block eventually
    arr = bytearray(range(256)) * 4  # array of 1 KiB
    loops = 2 * 1024 # send 2 MiB data,
    t1 = time.time()
    for i in range(loops):
        serial_socket.send(arr)
    t2 = time.time()

    # due to a 2.5 MByte TCP buffer we see a TCP throughput of over 800 MiB/s,
    # the data is cached somewhere then. For a larger amount things will start
    # to block and the QEMU UART emulation consuming it determines the speed.
    print('Throughput host send: ' + throughput_str(len(arr)*loops, t2-t1) )

    # When the serial port is configured at 115200 baud 8N1 (ie 10 bit times
    # per byte due to the start and stop bit), we can expect a throughput of
    # 115200 / 10 = 11.52 KiByte/s. Sending 2 MiByte will take a bit under 178
    # seconds then.
    # For physical platform we should see really this, if the clocks are set up
    # properly. On QEMU we may see higher speeds because the baudrate is
    # usually not emulated and so the host CPU's emulation power effectively
    # determines the speed. What we have seen for 2 MiByte is:
    #   QEMU/sabre: 8.5 KiByte/s -> 121 secs
    #   QEMU/zynq7000: 130 KiByte/s -> 16 secs

    # check if the test started
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'bytes processed: 0x10000', # 64 KiByte
        ],
        20)

    if not ret:
        pytest.fail('throughput start failed')

    # check if the test processed all data
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'bytes processed: 0x100000', # 1 MiByte
            'bytes processed: 0x200000', # 2 MiByte
        ],
        300)

    if not ret:
        pytest.fail('throughput test failed')

    t3 = time.time()
    delta = t3 - t1
    print('Throughput serial: {} (took {:.2f} secs)'.format(
            throughput_str(len(arr)*loops, delta),
            delta) )
