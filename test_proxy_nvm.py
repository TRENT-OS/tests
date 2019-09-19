import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

#use this variable to point to the image you want to run the tests with.
test_imagepath = '/build-zynq7000-Debug-TEST_PROXY_NVM/images/capdl-loader-image-arm-zynq7000'
timeout = 2000

#Add in all your different testcases in here.
@pytest.mark.parametrize("img, expected_output_array, timeout", [
    (test_imagepath,
    [
        #every test case output needs to happen twice (for both channels) 
        'TEST SMALL SECTION: Read values match the write values!',
        'TEST SMALL SECTION: Read values match the write values!',
        'TEST WHOLE MEMORY: Read values match the write values!',
        'TEST WHOLE MEMORY: Read values match the write values!',
        'TEST SIZE OUT OF BOUNDS: Write failed!',
        'TEST SIZE OUT OF BOUNDS: Write failed!',
        'TEST ADDRESS OUT OF BOUNDS: Write failed!',
        'TEST ADDRESS OUT OF BOUNDS: Write failed!',
    ],
    timeout),
])
def test_output_against_expected_str(boot_with_proxy, img,  expected_output_array, timeout):
        f_out = boot_with_proxy(image_subpath=img)[1]

        for index in range(0, len(expected_output_array)):
                success = expected_output_array[index]
                (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
                print(text)
                assert match == success