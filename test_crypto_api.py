import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

def test_agreement(boot):
    timeout = 15
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]
    result_list = [
        'testAgreement_init_ok: OK',
        'testAgreement_init_fail: OK',
        'testAgreement_compute_DH_ok: OK',
        'testAgreement_compute_ECDH_ok: OK',
        'testAgreement_compute_fail: OK',
        'testAgreement_free_ok: OK',
        'testAgreement_free_fail: OK',
        'testAgreement_init_ok: OK',
        'testAgreement_init_fail: OK',
        'testAgreement_compute_DH_ok: OK',
        'testAgreement_compute_ECDH_ok: OK',
        'testAgreement_compute_fail: OK',
        'testAgreement_free_ok: OK',
        'testAgreement_free_fail: OK'
    ]
    for result in result_list:
        (text, match) = logs.get_match_in_line(f_out, re.compile(result), timeout)
        assert match == result

def test_cipher(boot):
    timeout = 15
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]
    result_list = [
        'testCipher_init_ok: OK',
        'testCipher_init_fail: OK',
        'testCipher_free_ok: OK',
        'testCipher_free_fail: OK',
        'testCipher_encrypt_AES_ECB: OK',
        'testCipher_decrypt_AES_ECB: OK',
        'testCipher_encrypt_AES_CBC: OK',
        'testCipher_decrypt_AES_CBC: OK',
        'testCipher_encrypt_AES_GCM: OK',
        'testCipher_decrypt_AES_GCM_ok: OK',
        'testCipher_decrypt_AES_GCM_fail: OK',
        'testCipher_start_fail: OK',
        'testCipher_process_fail: OK',
        'testCipher_finalize_fail: OK',
        'testCipher_init_ok: OK',
        'testCipher_init_fail: OK',
        'testCipher_free_ok: OK',
        'testCipher_free_fail: OK',
        'testCipher_encrypt_AES_ECB: OK',
        'testCipher_decrypt_AES_ECB: OK',
        'testCipher_encrypt_AES_CBC: OK',
        'testCipher_decrypt_AES_CBC: OK',
        'testCipher_encrypt_AES_GCM: OK',
        'testCipher_decrypt_AES_GCM_ok: OK',
        'testCipher_decrypt_AES_GCM_fail: OK',
        'testCipher_start_fail: OK',
        'testCipher_process_fail: OK',
        'testCipher_finalize_fail: OK',
    ]
    for result in result_list:
        (text, match) = logs.get_match_in_line(f_out, re.compile(result), timeout)
        assert match == result

def test_digest(boot):
    timeout = 15
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]
    result_list = [
        'testDigest_init_ok: OK',
        'testDigest_init_fail: OK',
        'testDigest_free_ok: OK',
        'testDigest_free_fail: OK',
        'testDigest_hash_SHA256: OK',
        'testDigest_hash_MD5: OK',
        'testDigest_process_fail: OK',
        'testDigest_finalize_fail: OK',
        'testDigest_init_ok: OK',
        'testDigest_init_fail: OK',
        'testDigest_free_ok: OK',
        'testDigest_free_fail: OK',
        'testDigest_hash_SHA256: OK',
        'testDigest_hash_MD5: OK',
        'testDigest_process_fail: OK',
        'testDigest_finalize_fail: OK',
    ]
    for result in result_list:
        (text, match) = logs.get_match_in_line(f_out, re.compile(result), timeout)
        assert match == result

def test_key(boot):
    timeout = 15
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]
    result_list = [
        'testKey_export_ok: OK',
        'testKey_export_fail: OK',
        'testKey_import_ok: OK',
        'testKey_import_fail: OK',
        'testKey_generate_ok: OK',
        'testKey_generate_fail: OK',
        'testKey_generatePair_ok: OK',
        'testKey_generatePair_fail: OK',
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

def test_rng(boot):
    timeout = 15
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]
    result_list = [
        'testRng_getBytes_ok: OK',
        'testRng_getBytes_fail: OK',
        'testRng_reSeed_ok: OK',
        'testRng_reSeed_fail: OK',
        'testRng_getBytes_ok: OK',
        'testRng_getBytes_fail: OK',
        'testRng_reSeed_ok: OK',
        'testRng_reSeed_fail: OK',
    ]
    for result in result_list:
        (text, match) = logs.get_match_in_line(f_out, re.compile(result), timeout)
        assert match == result

def test_signature(boot):
    timeout = 15
    f_out = boot(image_subpath="/build-zynq7000-Debug-TEST_CRYPTO_API/images/capdl-loader-image-arm-zynq7000")[1]
    result_list = [
        'testSignature_init_ok: OK',
        'testSignature_init_fail: OK',
        'testSignature_sign_RSA_ok: OK',
        'testSignature_sign_fail: OK',
        'testSignature_verify_RSA_ok: OK',
        'testSignature_verify_fail: OK',
        'testSignature_init_ok: OK',
        'testSignature_init_fail: OK',
        'testSignature_sign_RSA_ok: OK',
        'testSignature_sign_fail: OK',
        'testSignature_verify_RSA_ok: OK',
        'testSignature_verify_fail: OK',
    ]
    for result in result_list:
        (text, match) = logs.get_match_in_line(f_out, re.compile(result), timeout)
        assert match == result
