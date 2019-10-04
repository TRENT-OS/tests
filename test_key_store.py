import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_imagepath = '/build-zynq7000-Debug-TEST_KEYSTORE/images/capdl-loader-image-arm-zynq7000'
timeout = 400

expected_output_array_unit_tests = [
    'TestKeyStore_scenario_1 succeeded',
    'TestKeyStore_scenario_2 succeeded'
    ]

expected_output_array_integration_tests_AES = [
    'TestKeyStore_scenario_3 succeeded',
    'TestKeyStore_scenario_4 succeeded'
    ]

expected_output_array_integration_tests_keyPair = [
    'TestKeyStore_scenario_5 succeeded',
    'TestKeyStore_scenario_6 succeeded'
    ]

def test_key_store_unit_tests(boot_with_proxy):
    f_out = boot_with_proxy(image_subpath=test_imagepath)[1]

    for index in range(0, len(expected_output_array_unit_tests)):
        success = expected_output_array_unit_tests[index]
        (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
        print(text)
        assert match == success

def test_key_store_integration_tests_AES(boot_with_proxy):
    f_out = boot_with_proxy(image_subpath=test_imagepath)[1]

    for index in range(0, len(expected_output_array_integration_tests_AES)):
        success = expected_output_array_integration_tests_AES[index]
        (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
        print(text)
        assert match == success

def test_key_store_integration_tests_keyPair(boot_with_proxy):
    f_out = boot_with_proxy(image_subpath=test_imagepath)[1]

    for index in range(0, len(expected_output_array_integration_tests_keyPair)):
        success = expected_output_array_integration_tests_keyPair[index]
        (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
        print(text)
        assert match == success