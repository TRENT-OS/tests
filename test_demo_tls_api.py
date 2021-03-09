import sys, os, re, time
import pytest

import logs # logs module from the common directory in TA

# Timeouts of the tests are set based on CI profiling.

#-------------------------------------------------------------------------------
@pytest.mark.dependency()
def test_demo_tls_api(boot_with_proxy):
    """
    BE AWARE: At the moment we do not test it really because it is required some
    infrastructure in CI which is not yet there (https server). Therefore we
    have chosen to just check that the demo is running until a certain point
    (the point in which the "connection refused" error rises).
    """

    test_run = boot_with_proxy(None)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        # ["Demo completed successfully"],
        ["PICO_SOCK_EV_ERR, OS error = -1303 (OS_ERROR_NETWORK_CONN_REFUSED)"],
        90)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
