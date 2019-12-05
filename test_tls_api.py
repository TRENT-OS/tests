import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time
import socket

test_system = "test_tls_api"
timeout = 60

def test_tls_api_library(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    success = 'testTls_lib: OK'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    assert match == success

def test_tls_api_rpc(boot_with_proxy):
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]
    success = 'testTls_rpc: OK'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
    assert match == success