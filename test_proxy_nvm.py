import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "test_system, expected_output_array, timeout", [(
    "test_proxy_nvm",
    [
        #every test case output needs to happen twice (for both channels)
        'TEST SMALL SECTION: Read values match the write values!',
        'TEST SMALL SECTION: Read values match the write values!',
        'TEST WHOLE MEMORY: Read values match the write values!',
        'TEST WHOLE MEMORY: Read values match the write values!',
        'TEST SIZE OUT OF BOUNDS: Write failed!',
        'TEST SIZE OUT OF BOUNDS: Write failed!',
        'TEST ADDRESS OUT OF BOUNDS: Write failed!',
        'TEST ADDRESS OUT OF BOUNDS: Write failed!',
    ],
    350
)])
def test_output_against_expected_str(boot_with_proxy, test_system, expected_output_array, timeout):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
