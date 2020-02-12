import pytest

import sys
sys.path.append('../common')

import tests
import os
import time

test_system = "test_chanmux"
timeout = 60

#-------------------------------------------------------------------------------
test_chanmux_return_codes_lst = [
    "ChanMuxTest_testReturnCodes: SUCCESS (tester 1)",
    "ChanMuxTest_testReturnCodes: SUCCESS (tester 2)"
]
@pytest.mark.parametrize('expr', test_chanmux_return_codes_lst)
def test_chanmux_return_codes(boot_with_proxy, expr):
    """This test will check the correctness of return values in case of bad
    parameters."""

    tests.simple(boot_with_proxy, test_system, expr, timeout)

#-------------------------------------------------------------------------------
test_chanmux_overflow_lst = [
    "ChanMuxTest_testOverflow: SUCCESS (tester 1)",
    "ChanMuxTest_testOverflow: SUCCESS (tester 2)"
]
@pytest.mark.parametrize('expr', test_chanmux_overflow_lst)
def test_chanmux_overflow(boot_with_proxy, expr):
    """This test will check the correct trigger of the overflow condition of
    ChanMux.

    The behavior of ChanMux is described at https://wiki.hensoldt-cyber.systems/display/HEN/SEOS+ChanMUX%2C+UART+Proxy+and+Host-Bridge.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) send a command to the
        Proxy App (via ChanMux) in order to request a shot of an amount of data
        that will result in an overflow.
        After that the ChanMux gets probed to check whether the overflow
        condition happened as expected."""

    tests.simple(boot_with_proxy, test_system, expr, timeout)

#-------------------------------------------------------------------------------
test_chanmux_full_duplex_lst = [
    "ChanMuxTest_testFullDuplex: SUCCESS (tester 1)",
    "ChanMuxTest_testFullDuplex: SUCCESS (tester 2)"
]
@pytest.mark.parametrize('expr', test_chanmux_full_duplex_lst)
def test_chanmux_fullduplex(boot_with_proxy, expr):
    """This test will check the correct operation of ChanMux when streaming in
    full duplex mode.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) send a command to the
        Proxy App (via ChanMux) with a certain payload (with a give pattern) in
        order to receive it back as in a echo server. While the client (SEOS) is
        streaming its data in a loop the server (Proxy) will echo and another
        thread of the client will receive the payload back and check the pattern
        of the data."""

    tests.simple(boot_with_proxy, test_system, expr, timeout)
