import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_system = "test_keystore"
timeout = 600


#-------------------------------------------------------------------------------
def test_key_store_unit_tests_fat(boot_with_proxy):
    """
    Run unit tests (import, read, delete) with KeySrore (using FAT file system)
    Scenario 1: local keystore
    Scenario 2: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreFAT_scenario_1 succeeded",
        "TestKeyStoreFAT_scenario_2 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_AES_fat(boot_with_proxy):
    """
    import AES-256 key to KeyStore using (using FAT file system)
    Scenario 3: local keystore
    Scenario 4: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreFAT_scenario_3 succeeded",
        "TestKeyStoreFAT_scenario_4 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_keyPair_fat(boot_with_proxy):
    """
    import RSA-128 key pair to KeyStore using FAT file system
    Scenario 5: local keystore
    Scenario 6: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreFAT_scenario_5 succeeded",
        "TestKeyStoreFAT_scenario_6 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_copy_fat(boot_with_proxy):
    """
    Copy key from one keystore to another (using FAT file system)
    Scenario 7: local keystore
    Scenario 8: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreFAT_scenario_7 succeeded",
        "TestKeyStoreFAT_scenario_8 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_move_fat(boot_with_proxy):
    """
    Move key from one keystore to another (using FAT file system)
    Scenario 9: local keystore
    Scenario 10: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreFAT_scenario_9 succeeded",
        "TestKeyStoreFAT_scenario_10 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

#-------------------------------------------------------------------------------
def test_key_store_unit_tests_spiffs(boot_with_proxy):
    """
    Run unit tests (import, read, delete) with KeySrore (using SPIFFS file system)
    Scenario 1: local keystore
    Scenario 2: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreSPIFFS_scenario_1 succeeded",
        "TestKeyStoreSPIFFS_scenario_2 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_AES_spiffs(boot_with_proxy):
    """
    import AES-256 key to KeyStore using (using SPIFFS file system)
    Scenario 3: local keystore
    Scenario 4: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreSPIFFS_scenario_3 succeeded",
        "TestKeyStoreSPIFFS_scenario_4 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_keyPair_spiffs(boot_with_proxy):
    """
    import RSA-128 key pair to KeyStore (using SPIFFS file system)
    Scenario 5: local keystore
    Scenario 6: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreSPIFFS_scenario_5 succeeded",
        "TestKeyStoreSPIFFS_scenario_6 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_copy_spiffs(boot_with_proxy):
    """
    Copy key from one keystore to another (using SPIFFS file system)
    Scenario 7: local keystore
    Scenario 8: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreSPIFFS_scenario_7 succeeded",
        "TestKeyStoreSPIFFS_scenario_8 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg

#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_move_spiffs(boot_with_proxy):
    """
    Move key from one keystore to another (using SPIFFS file system)
    Scenario 9: local keystore
    Scenario 10: remote keystore
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "TestKeyStoreSPIFFS_scenario_9 succeeded",
        "TestKeyStoreSPIFFS_scenario_10 succeeded"
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg
