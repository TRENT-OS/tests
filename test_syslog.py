import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


#-------------------------------------------------------------------------------
def test_hello_world(boot):

    test_run = boot("test_syslog")
    f_out = test_run[1]

    success_msg = "SUCCESS"
    timeout = 60
    (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
    assert match == success_msg
