import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


test_system = "test_spiffs_filestream"
timeout = 100

#-------------------------------------------------------------------------------
def test_spiffs_filestream_unit_tests(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "Test_Spiffs_FileStream_test_case_01 succeeded!",
        "Test_Spiffs_FileStream_test_case_02 succeeded!",
        "Test_Spiffs_FileStream_test_case_03 succeeded!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_spiffs_filestream_demo_tests(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "Test_Spiffs_FileStream_test_case_04 succeeded!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
