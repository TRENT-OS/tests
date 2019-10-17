import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_imagepath = '/build-zynq7000-Debug-DEMO_KEYSTORE/images/capdl-loader-image-arm-zynq7000'
timeout = 100


#-------------------------------------------------------------------------------
@pytest.mark.parametrize("img, expected_output_array, timeout", [
    (test_imagepath,
    [
        'Demo with local crypto succeeded!',
        'Demo with remote crypto succeeded!'
    ],
    timeout),
])
def keystore_demo_test(boot_with_proxy, img, expected_output_array, timeout):
    f_out = boot_with_proxy(image_subpath=img)[1]

    for index in range(0, len(expected_output_array)):
        success = expected_output_array[index]
        (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
        print(text)
        assert match == success
