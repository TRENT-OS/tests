import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


def test_spiffs_integration(boot_with_proxy):
    f_out = boot_with_proxy(image_subpath="/build-zynq7000-Debug-TEST_SPIFFS_INTEGRATION/images/capdl-loader-image-arm-zynq7000")[1]

    #-----------------------------------File 1------------------------------------------
    success = 'Available space in file 1 is equal to file size'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 100)
    print(text)
    assert match == success
    
    success = 'File 1, unsuccesful write to read-only file!'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    success = 'File 1 has no errors!'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success
    
    success = 'Read from file 1: c=1,b=1'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    success = 'Get from file 1: c=1'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success


    #-----------------------------------File 2------------------------------------------
    success = 'Available space in file 2 is equal to file size'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 100)
    print(text)
    assert match == success
    
    success = 'File 2, unsuccesful write to read-only file!'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    success = 'File 2 has no errors!'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success
    
    success = 'Read from file 2: c=2,b=2'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    success = 'Get from file 2: c=2'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success


    #-----------------------------------File 3------------------------------------------
    success = 'Available space in file 3 is equal to file size'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 100)
    print(text)
    assert match == success
    
    success = 'File 3, unsuccesful write to read-only file!'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    success = 'File 3 has no errors!'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success
    
    success = 'Read from file 3: c=3,b=3'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    success = 'Get from file 3: c=3'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success


    #-----------------------------------Closing files------------------------------------------
    success = 'SpiffsFileStream_dtor: closing f1'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 100)
    print(text)
    assert match == success

    success = 'SpiffsFileStream_dtor: closing f2'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    success = 'SpiffsFileStream_dtor: closing f3'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

    #-----------------------------------Destroying the context------------------------------------------
    success = 'Succesfully destroyed the context.'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success
