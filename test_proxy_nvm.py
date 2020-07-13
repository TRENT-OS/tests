import pytest

import sys

import logs # logs module from the common directory in TA
import os
import re
import time

test_system = "test_proxy_nvm"
timeout = 300

def test_proxy_nvm_small_section_test(boot_with_proxy):
    """This test will check that a small section (few bytes somewhere in the
    file is correctly written.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) write a small section of
        the NVM abstraction exposed by the Proxy app with a known pattern and
        then read it and check it.

    Test is currently limited to the disk size preconfigured by the proxy application:
        - 36 MiB for 1st NVM channel
        - 128 KiB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST SMALL SECTION: Read values match the write values!",
        "TEST SMALL SECTION: Read values match the write values!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

def test_proxy_nvm_whole_memory_test(boot_with_proxy):
    """This test will check that a small section is correctly written.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) write the full size of
        the NVM abstraction exposed by the Proxy app with a known pattern and
        then read it and check it.

    Test is currently limited to the disk size preconfigured by the proxy application:
        - 36 MiB for 1st NVM channel
        - 128 KiB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST WHOLE MEMORY: Read values match the write values!",
        "TEST WHOLE MEMORY: Read values match the write values!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

def test_proxy_nvm_size_out_of_bounds_test(boot_with_proxy):
    """This test will check that writing outside of the bounds (by exceeding in
    the size but starting from a valid address) results in an error condition.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) try to write outside of
        the boundaries of the NVM abstraction exposed by the Proxy app then
        check that an error condition is raised.

    Test is currently limited to the disk size preconfigured by the proxy application:
        - 36 MiB for 1st NVM channel
        - 128 KiB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST SIZE OUT OF BOUNDS: Write failed!",
        "TEST SIZE OUT OF BOUNDS: Write failed!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

def test_proxy_nvm_address_out_of_bounds_test(boot_with_proxy):
    """This test will check that writing outside of the bounds (by using
    invalid addresses) results in an error condition.

    Underlying SEOS Test System behavior:

        two SEOS Tester components will (in parallel) try to write outside of
        the boundaries of the NVM abstraction exposed by the Proxy app then
        check that an error condition is raised.

    Test is currently limited to the disk size preconfigured by the proxy application:
        - 36 MiB for 1st NVM channel
        - 128 KiB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST ADDRESS OUT OF BOUNDS: Write failed!",
        "TEST ADDRESS OUT OF BOUNDS: Write failed!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
