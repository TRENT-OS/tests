import pytest
import sys
import os
import re

import logs # logs module from the common directory in TA

def test_run_demo(boot_with_proxy):
    test_run = boot_with_proxy("demo_configuration_as_component")
    f_out = test_run[1]

    success_msg = "finished successfully"
    timeout = 15
    (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
    assert match == success_msg
