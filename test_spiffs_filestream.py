import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


test_imagepath = '/build-zynq7000-Debug-TEST_SPIFFS_FILESTREAM/images/capdl-loader-image-arm-zynq7000'
timeout = 100

expected_output_array_unit_test = [
        'Test_Spiffs_FileStream_test_case_01 succeeded!',
        'Test_Spiffs_FileStream_test_case_02 succeeded!',
        'Test_Spiffs_FileStream_test_case_03 succeeded!'
    ]

expected_output_array_demo_test = [
        'Test_Spiffs_FileStream_test_case_04 succeeded!'
    ]


#-------------------------------------------------------------------------------
def test_spiffs_filestream_unit_tests(boot_with_proxy):
    f_out = boot_with_proxy(image_subpath=test_imagepath)[1]

    for index in range(0, len(expected_output_array_unit_test)):
        success = expected_output_array_unit_test[index]
        (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
        print(text)
        assert match == success


#-------------------------------------------------------------------------------
def test_spiffs_filestream_demo_tests(boot_with_proxy):
    f_out = boot_with_proxy(image_subpath=test_imagepath)[1]

    for index in range(0, len(expected_output_array_demo_test)):
        success = expected_output_array_demo_test[index]
        (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
        print(text)
        assert match == success
