import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


def test_hello_world(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_SYSLOG/images/capdl-loader-image-arm-zynq7000")[1]

    success = 'SUCCESS'
    (text, match) = logs.get_match_in_line(f_out, re.compile('SUCCESS'), 60)
    print(text)
    assert match == success

