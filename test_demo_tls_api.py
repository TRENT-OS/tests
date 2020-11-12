import sys, os, re, time
import pytest

import logs # logs module from the common directory in TA

# Timeouts of the tests are set based on CI profiling.

#-------------------------------------------------------------------------------
@pytest.mark.dependency()
def test_demo_tls_api(boot_with_proxy):
    """
    Test that demo_tls_api completed successfully
    """

    test_run = boot_with_proxy(None)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Demo completed successfully"],
        90)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
