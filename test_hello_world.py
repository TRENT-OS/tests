import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

def test_hello_world(boot):
    """
    Test a minimal SEOS system that has one application saying hello to the
    world
    """

    test_run = boot("test_hello_world")
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["hello world!"],
        15)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
