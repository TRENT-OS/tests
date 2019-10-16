import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


#def test_hello_world(boot):
#    f_out = boot(image_subpath="build-zynq7000-Debug-HELLO_WORLD/images/capdl-loader-image-arm-zynq7000")[1]
#
#    hello_world_ok = 'hello world!';
#    (text, match) = logs.get_match_in_line(f_out, re.compile(hello_world_ok), 60)
#    print(text)
#    assert match == hello_world_ok

