import pytest

import sys

import logs # logs module from the common directory in TA
import os
import re
import time

test_system = "test_proxy_nvm"
timeout = 300

def test_proxy_nvm_storage_start_address(boot_with_proxy):
    """This test will check writing and reading at the beginning of the storage.

    Underlying SEOS Test System behavior:

        Two SEOS Tester components will (in parallel) write a data via the NVM
        abstraction exposed by the Proxy app with a known pattern and then read
        it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST STORAGE START ADDRESS: Read values match the write values!",
        "TEST STORAGE START ADDRESS: Read values match the write values!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(
                                f_out,
                                re.compile(success_msg),
                                timeout)

        assert match == success_msg

def test_proxy_nvm_storage_mid_address(boot_with_proxy):
    """This test will check writing and reading in the middle of the storage.

    Underlying SEOS Test System behavior:

        Two SEOS Tester components will (in parallel) write a data via the NVM
        abstraction exposed by the Proxy app with a known pattern and then read
        it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST STORAGE MID ADDRESS: Read values match the write values!",
        "TEST STORAGE MID ADDRESS: Read values match the write values!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(
                                f_out,
                                re.compile(success_msg),
                                timeout)

        assert match == success_msg

def test_proxy_nvm_storage_end_address(boot_with_proxy):
    """This test will check writing and reading at the end of the storage.

    Underlying SEOS Test System behavior:

        Two SEOS Tester components will (in parallel) write a data via the NVM
        abstraction exposed by the Proxy app with a known pattern and then read
        it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST STORAGE END ADDRESS: Read values match the write values!",
        "TEST STORAGE END ADDRESS: Read values match the write values!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(
                                f_out,
                                re.compile(success_msg),
                                timeout)

        assert match == success_msg

def test_proxy_nvm_storage_overflow(boot_with_proxy):
    """This test will check that writing outside of the bounds (when starting
    from the valid address) results in an error condition.

    Underlying SEOS Test System behavior:

        Two SEOS Tester components will (in parallel) write a data via the NVM
        abstraction exposed by the Proxy app with a known pattern and then read
        it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST STORAGE OVERFLOW: Write failed!",
        "TEST STORAGE OVERFLOW: Write failed!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(
                                f_out,
                                re.compile(success_msg),
                                timeout)

        assert match == success_msg

def test_proxy_nvm_far_out_of_bounds_address(boot_with_proxy):
    """This test will check that writing outside of the bounds (invalid start
    addresses) results in an error condition.

    Underlying SEOS Test System behavior:

        Two SEOS Tester components will (in parallel) write a data via the NVM
        abstraction exposed by the Proxy app with a known pattern and then read
        it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        #every test case output needs to happen twice (for both channels)
        "TEST STORAGE FAR OUT OF BOUNDS ADDRESS: Write failed!",
        "TEST STORAGE FAR OUT OF BOUNDS ADDRESS: Write failed!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(
                                f_out,
                                re.compile(success_msg),
                                timeout)

        assert match == success_msg
