import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


#def test_hello_world(boot):
#    test_run = boot("build-zynq7000-Debug-HELLO_WORLD/images/capdl-loader-image-arm-zynq7000")
#    f_out = test_run[1]
#
#    success_msg = "hello world!"
#    timeout = 60
#    (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
#    assert match == success_msg
