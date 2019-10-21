import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "test_image, expected_output_array, timeout", [(
    "build-zynq7000-Debug-DEMO_KEYSTORE/images/capdl-loader-image-arm-zynq7000",
    [
        'Demo with local crypto succeeded!',
        'Demo with remote crypto succeeded!'
    ],
    100
)])
def keystore_demo_test(boot_with_proxy, test_image, expected_output_array, timeout):
    test_run = boot_with_proxy(image)
    f_out = test_run[1]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        print(text)
        assert match == success_msg
