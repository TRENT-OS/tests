import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_system = "test_proxy_nvm"
timeout = 300

#-------------------------------------------------------------------------------
def test_proxy_nvm_small_section_test(boot_with_proxy):
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

#-------------------------------------------------------------------------------
def test_proxy_nvm_whole_memory_test(boot_with_proxy):
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

#-------------------------------------------------------------------------------
def test_proxy_nvm_size_out_of_bounds_test(boot_with_proxy):
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

#-------------------------------------------------------------------------------
def test_proxy_nvm_address_out_of_bounds_test(boot_with_proxy):
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
