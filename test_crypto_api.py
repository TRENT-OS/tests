import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time


def test_random_data(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success1 = 'Printing random bytes... 0xb9 0x01 0x1b 0x41 0x77 0xd8 0x76 0x9e 0x7a 0x16 0x2b 0x88 0x53 0xc4 0x4e 0xf0'
    success2 = 'Printing random bytes... 0xcc 0x39 0xe2 0x53 0xe5 0xcd 0xeb 0x89 0x1a 0xd8 0x4f 0x5f 0x3c 0xd5 0x02 0xb4'
    success3 = 'Printing random bytes... 0x50 0x3b 0x8f 0xe4 0x88 0xe9 0xff 0x0a 0x39 0x8f 0x83 0x1d 0x90 0xcb 0x03 0xc1'

    (text, match) = logs.get_match_in_line(f_out, re.compile(success1), 5)
    print(text)
    assert match == success1

    (text, match) = logs.get_match_in_line(f_out, re.compile(success2), 5)
    print(text)
    assert match == success2

    (text, match) = logs.get_match_in_line(f_out, re.compile(success3), 5)
    print(text)
    assert match == success3

    (text, match) = logs.get_match_in_line(f_out, re.compile(success1), 5)
    print(text)
    assert match == success1

    (text, match) = logs.get_match_in_line(f_out, re.compile(success2), 5)
    print(text)
    assert match == success2

    (text, match) = logs.get_match_in_line(f_out, re.compile(success3), 5)
    print(text)
    assert match == success3

def test_key(boot):
    timeout = 15
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]
    result_list = [
        'testKey_init_ok: OK',
        'testKey_init_fail: OK',
        'testKey_export_ok: OK',
        'testKey_export_fail: OK',
        'testKey_import_ok: OK',
        'testKey_import_fail: OK',
        'testKey_generate_ok: OK',
        'testKey_generate_fail: OK',
        'testKey_generatePair_ok: OK',
        'testKey_generatePair_fail: OK',
        'testKey_init_ok: OK',
        'testKey_init_fail: OK',
        'testKey_export_ok: OK',
        'testKey_export_fail: OK',
        'testKey_import_ok: OK',
        'testKey_import_fail: OK',
        'testKey_generate_ok: OK',
        'testKey_generate_fail: OK',
        'testKey_generatePair_ok: OK',
        'testKey_generatePair_fail: OK',
    ]
    for result in result_list:
        (text, match) = logs.get_match_in_line(f_out, re.compile(result), timeout)
        assert match == result

def test_md5(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success = 'Printing MD5 digest... 0x78 0x1e 0x5e 0x24 0x5d 0x69 0xb5 0x66 0x97 0x9b 0x86 0xe2 0x8d 0x23 0xf2 0xc7'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

def test_sha256(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success = 'Printing SHA256 digest... 0x84 0xd8 0x98 0x77 0xf0 0xd4 0x04 0x1e 0xfb 0x6b 0xf9 0x1a 0x16 0xf0 0x24 0x8f 0x2f 0xd5 0x73 0xe6 0xaf 0x05 0xc1 0x9f 0x96 0xbe 0xdb 0x9f 0x88 0x2f 0x78 0x82'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match == success

def test_aes_ecb(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success1 = 'Printing AES-ECB encrypted data ... 0x8d 0x83 0x5d 0x0c 0xff 0xd8 0xba 0xd5 0x85 0xfe 0x8b 0x42 0x94 0xc4 0x21 0x88'
    success2 = 'Printing AES-ECB decrypted data ... 0x30 0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x41 0x42 0x43 0x44 0x45 0x46'

    # first check is aes enrcyption of well known string and then decryption using the library locally
    (text, match) = logs.get_match_in_line(f_out, re.compile(success1), 5)
    print(text)
    assert match == success1

    (text, match) = logs.get_match_in_line(f_out, re.compile(success2), 5)
    print(text)
    assert match == success2

    # second check is aes enrcyption of well known string and then decryption using the library on a server component
    (text, match) = logs.get_match_in_line(f_out, re.compile(success1), 5)
    print(text)
    assert match == success1

    (text, match) = logs.get_match_in_line(f_out, re.compile(success2), 5)
    print(text)
    assert match == success2

def test_aes_gcm(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success1 = 'Printing AES-GCM encrypted data ... 0xb7 0x0b 0x29 0xf6 0x93 0x8b 0x17 0x4a 0xb3 0x9f 0xe2 0xd6 0x85 0x40 0x8c 0xab 0x1d 0x96 0xcf 0xdf 0x31 0xb8 0x57 0x00 0x27 0xa9 0xc4 0x2e 0xde 0x1a'
    success2 = 'Printing AES-GCM tag ... 0x6e 0xf3 0x07 0xcb 0x2b 0x13 0xa2 0x2f 0x55 0xe0 0x38 0xc2 0x11 0x63 0x2f 0x51'
    success3 = 'Printing AES-GCM decrypted data ... 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x46 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30 0x30'

    # first check is aes enrcyption of well known string and then decryption using the library locally
    (text, match) = logs.get_match_in_line(f_out, re.compile(success1), 5)
    print(text)
    assert match == success1

    (text, match) = logs.get_match_in_line(f_out, re.compile(success2), 5)
    print(text)
    assert match == success2

    (text, match) = logs.get_match_in_line(f_out, re.compile(success3), 5)
    print(text)
    assert match == success3

    # second check is aes enrcyption of well known string and then decryption using the library on a server component
    (text, match) = logs.get_match_in_line(f_out, re.compile(success1), 5)
    print(text)
    assert match == success1

    (text, match) = logs.get_match_in_line(f_out, re.compile(success2), 5)
    print(text)
    assert match == success2

    (text, match) = logs.get_match_in_line(f_out, re.compile(success3), 5)
    print(text)
    assert match == success3

def test_rsa(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success = 'INFO:.*testSignatureRSA: RSA signature correctly generated'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match != None

    success = 'INFO:.*testSignatureRSA: RSA signature correctly verified'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match != None

def test_dh(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success = 'Computed DH-shared secret for CLIENT: 0x0a 0x01 0xa3 0x91 0x9f 0x2b 0xa3 0x69 0xdc 0x5b 0x11 0xde 0x2c'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match != None

def test_ecdh(boot):
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]

    success = 'Computed ECDH-shared secret for CLIENT: 0xd6 0x84 0x0f 0x6b 0x42 0xf6 0xed 0xaf 0xd1 0x31 0x16 0xe0 0xe1 0x25 0x65 0x20 0x2f 0xef 0x8e 0x9e 0xce 0x7d 0xce 0x03 0x81 0x24 0x64 0xd0 0x4b 0x94 0x42 0xde'
    (text, match) = logs.get_match_in_line(f_out, re.compile(success), 5)
    print(text)
    assert match != None
