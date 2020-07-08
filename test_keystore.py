import pytest

import sys

import logs # logs module from the common directory in TA
import os
import re
import time

test_system = "test_keystore"
# based in the profiling in CI, 180 sec should be enough. Most tests finish
# well under 60 seconds, just sometimes tests can take much longer. Might be
# related to CI system load in the end.
timeout = 180


#-------------------------------------------------------------------------------
def test_key_store_unit_tests(boot_with_proxy):
    """
    Run unit tests (import, read, delete) with KeySrore (using FAT file system)
    Scenario 1: local keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            "TestKeyStore_scenario_1 succeeded",
        ],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_AES(boot_with_proxy):
    """
    import AES-256 key to KeyStore using (using FAT file system)
    Scenario 3: local keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            "TestKeyStore_scenario_3 succeeded",
        ],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_keyPair(boot_with_proxy):
    """
    import RSA-128 key pair to KeyStore using FAT file system
    Scenario 5: local keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            "TestKeyStore_scenario_5 succeeded",
        ],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_copy(boot_with_proxy):
    """
    Copy key from one keystore to another (using FAT file system)
    Scenario 7: local keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            "TestKeyStore_scenario_7 succeeded",
        ],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_move(boot_with_proxy):
    """
    Move key from one keystore to another (using FAT file system)
    Scenario 9: local keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        [
            "TestKeyStore_scenario_9 succeeded",
        ],
        timeout
        )


    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
