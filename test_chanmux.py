import pytest

import sys

import test_parser as parser
from tests import run_test_log_match_set

test_system = "test_chanmux"
timeout = 60

#-------------------------------------------------------------------------------
def test_chanmux_return_codes(boot_with_proxy):
    """This test will check the correctness of return values in case of bad
    parameters."""

    parser.check_test(boot_with_proxy(test_system), timeout, 'ChanMuxTest_testReturnCodes')

#-------------------------------------------------------------------------------
def test_chanmux_overflow(boot_with_proxy):
    """This test will check the correct trigger of the overflow condition of
    ChanMux.

    Underlying TRENTOS Test System behavior:

        two TRENTOS Tester components will (in parallel) send a command to the
        Proxy App (via ChanMux) in order to request a shot of an amount of data
        that will result in an overflow.
        After that the ChanMux gets probed to check whether the overflow
        condition happened as expected."""

    parser.check_test(boot_with_proxy(test_system), timeout, 'ChanMuxTest_testOverflow')

#-------------------------------------------------------------------------------
def test_chanmux_max_size(boot_with_proxy):
    """This test will check the correct operation of ChanMux when streaming an
    amount of data which is the MTU of ChanMux.

    Underlying TRENTOS Test System behavior:

        two TRENTOS Tester components will (in parallel) send 3  commands to
        the Proxy App (via ChanMux) with a certain payload (with a give pattern),
        respectively with length ChanMux MTU - 1 , ChanMux MTU and
        ChanMux MTU + 1.
        The Proxy App checks the pattern and sends back a single answer for
        each command with the index of the fist byte that mismatches the
        pattern. This is then checked in the way the amount of bytes correctly
        sent must be at the most exactly as the datalink MTU size. Therefore in
        the +1 case the last byte results to be truncated and not received from
        the othe side"""

    parser.check_test(boot_with_proxy(test_system), timeout, 'ChanMuxTest_testMaxSize')

#-------------------------------------------------------------------------------
def test_chanmux_fullduplex(boot_with_proxy):
    """This test will check the correct operation of ChanMux when streaming in
    full duplex mode.

    Underlying TRENTOS Test System behavior:

        two TRENTOS Tester components will (in parallel) send a command to the
        Proxy App (via ChanMux) with a certain payload (with a give pattern) in
        order to receive it back as in a echo server. While the client
        (TRENTOS) is streaming its data in a loop the server (Proxy) will echo
        and another thread of the client will receive the payload back and check
        the pattern of the data."""

    test_chanmux_full_duplex_lst = [
        "ChanMuxTest_testFullDuplex: SUCCESS (tester 1)",
        "ChanMuxTest_testFullDuplex: SUCCESS (tester 2)"
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           test_chanmux_full_duplex_lst,
                           timeout)
