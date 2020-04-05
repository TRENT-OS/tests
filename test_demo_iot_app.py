import sys, os, re, time
import pytest
sys.path.append('../common')
import logs

#-------------------------------------------------------------------------------
def test_demo_iot_app(boot):
    """
    Test that the CapDL Loader suspends itself after it has successfully set
    the IoT demo system up
    """

    test_run = boot("demo_iot_app")
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Done; suspending..."],
        15)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
