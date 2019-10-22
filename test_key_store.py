import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_system = "test_keystore"
timeout = 400


#-------------------------------------------------------------------------------
def test_key_store_unit_tests(boot_with_proxy):

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStore_scenario_1 succeeded",
        "TestKeyStore_scenario_2 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_AES(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStore_scenario_3 succeeded",
        "TestKeyStore_scenario_4 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_keyPair(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStore_scenario_5 succeeded",
        "TestKeyStore_scenario_6 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
