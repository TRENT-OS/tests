import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

image = "build-zynq7000-Debug-TEST_HELLO_WORLD/images/capdl-loader-image-arm-zynq7000"
timeout = 15


# ToDo: actually, this test case should run first and if it fails, then the
#       whole test should be aborted.
def test_hello_world(boot):
    test_run = boot(image)
    f_out = test_run[1]

    success_msg = "hello world!"
    timeout = 60
    (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
    assert match == success_msg

