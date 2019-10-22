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
    "demo_keystore",
    [
        'Demo with local crypto succeeded!',
        'Demo with remote crypto succeeded!'
    ],
    100
)])
def keystore_demo_test(boot_with_proxy, test_system, expected_output_array, timeout):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        print(text)
        assert match == success_msg
