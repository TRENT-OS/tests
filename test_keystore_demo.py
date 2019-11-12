import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_system = "demo_keystore"
timeout = 100

#-------------------------------------------------------------------------------
def keystore_demo_test(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "Demo with local crypto succeeded!",
        "Demo with remote crypto succeeded!"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
