import pytest

import sys

import logs # logs module from the common directory in TA
import os
import re
import time

def test_hello_world(boot_sel4_native):
    """
    Test a minimal TRENTOS-M system that has one application saying hello to the
    world
    """

    test_run = boot_sel4_native()
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Hello, world!"],
        15)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))