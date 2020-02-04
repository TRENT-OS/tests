import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_system = "test_chanmux"
timeout = 60

#-------------------------------------------------------------------------------
def test_chanmux_overflow(boot_with_proxy):
    """This test will check the correct trigger of the overflow condition of
    ChanMux.

    The behavior of ChanMux is described at https://wiki.hensoldt-cyber.systems/display/HEN/SEOS+ChanMUX%2C+UART+Proxy+and+Host-Bridge.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) send a command to the
        Proxy App (via ChanMux) in order to request a shot of an amount of data
        that will result in an overflow.
        After that the ChanMux gets probed to check whether the overflow
        condition happened as expected."""

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "ChanMuxTest_testOverflow: SUCCESS",
        "ChanMuxTest_testOverflow: SUCCESS"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

#-------------------------------------------------------------------------------
def test_chanmux_fullduplex(boot_with_proxy):
    """This test will check the correct operation of ChanMux when streaming in
    full duplex mode.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) send a command to the
        Proxy App (via ChanMux) with a certain payload (with a give pattern) in
        order to receive it back as in a echo server. While the client (SEOS) is
        streaming its data in a loop the server (Proxy) will echo and another
        thread of the client will receive the payload back and check the pattern
        of the data."""

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "ChanMuxTest_testFullDuplex: SUCCESS",
        "ChanMuxTest_testFullDuplex: SUCCESS"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
