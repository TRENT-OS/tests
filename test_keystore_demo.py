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
def test_keystore_demo(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            "Demo with local crypto succeeded!",
            "Demo with remote crypto succeeded!"
        ],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
