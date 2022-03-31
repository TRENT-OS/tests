import pytest
import logs # logs module from the common directory in TA

test_system = "demo_keystore"
timeout = 100

#-------------------------------------------------------------------------------
def test_keystore_demo(boot_with_proxy):
    test_runner = boot_with_proxy(test_system)

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        test_runner.get_system_log(),
        [
            "Demo with local crypto succeeded!",
            "Demo with remote crypto succeeded!"
        ],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
