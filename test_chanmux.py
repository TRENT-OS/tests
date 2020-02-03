import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_system = "test_chanmux"
timeout = 300

#@pytest.mark.skip(reason="backend not yet implemented")
#-------------------------------------------------------------------------------
def test_chanmux_overflow(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "ChanMuxTest_testOverflow: SUCCESS",
        "ChanMuxTest_testOverflow: SUCCESS"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

#@pytest.mark.skip(reason="backend not yet implemented")
#-------------------------------------------------------------------------------
def test_chanmux_fullduplex(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    assert False, "NOT YET IMPLEMENTED"
