import pytest

import sys
import logs # logs module from the common directory in TA
import os
import re
import time

test_system = "test_seos_filestream"
timeout = 200

#-------------------------------------------------------------------------------
def test_seos_filestream_spiffs(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "Test_Seos_FileStream_test_case_01 succeeded!",
        "Test_Seos_FileStream_test_case_02 succeeded!",
        "Test_Seos_FileStream_test_case_03 succeeded!",
        "Test_Seos_FileStream_test_case_04 succeeded!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_seos_filestream_fat(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "Test_Seos_FileStream_test_case_01 succeeded!",
        "Test_Seos_FileStream_test_case_02 succeeded!",
        "Test_Seos_FileStream_test_case_03 succeeded!",
        "Test_Seos_FileStream_test_case_04 succeeded!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
