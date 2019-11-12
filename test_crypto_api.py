import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_system = "test_crypto_api"
timeout = 15

#-------------------------------------------------------------------------------

def test_agreement(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'testAgreement_init_ok: OK',
        'testAgreement_init_fail: OK',
        'testAgreement_compute_DH_ok: OK',
        'testAgreement_compute_DH_rnd_ok: OK',
        'testAgreement_compute_ECDH_ok: OK',
        'testAgreement_compute_ECDH_rnd_ok: OK',
        'testAgreement_compute_fail: OK',
        'testAgreement_free_ok: OK',
        'testAgreement_free_fail: OK',
        'testAgreement_agree_buffer: OK',
        'testAgreement_init_ok: OK',
        'testAgreement_init_fail: OK',
        'testAgreement_compute_DH_ok: OK',
        'testAgreement_compute_DH_rnd_ok: OK',
        'testAgreement_compute_ECDH_ok: OK',
        'testAgreement_compute_ECDH_rnd_ok: OK',
        'testAgreement_compute_fail: OK',
        'testAgreement_free_ok: OK',
        'testAgreement_free_fail: OK',
        'testAgreement_agree_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_cipher(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

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
        'testCipher_init_buffer: OK',
        'testCipher_start_buffer: OK',
        'testCipher_process_buffer: OK',
        'testCipher_finalize_buffer: OK',
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
        'testCipher_init_buffer: OK',
        'testCipher_start_buffer: OK',
        'testCipher_process_buffer: OK',
        'testCipher_finalize_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_mac(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'testMac_init_ok: OK',
        'testMac_init_fail: OK',
        'testMac_free_ok: OK',
        'testMac_free_fail: OK',
        'testMac_mac_HMAC_MD5: OK',
        'testMac_mac_HMAC_SHA256: OK',
        'testMac_start_fail: OK',
        'testMac_process_fail: OK',
        'testMac_finalize_fail: OK',
        'testMac_start_buffer: OK',
        'testMac_process_buffer: OK',
        'testMac_finalize_buffer: OK',
        'testMac_init_ok: OK',
        'testMac_init_fail: OK',
        'testMac_free_ok: OK',
        'testMac_free_fail: OK',
        'testMac_mac_HMAC_MD5: OK',
        'testMac_mac_HMAC_SHA256: OK',
        'testMac_start_fail: OK',
        'testMac_process_fail: OK',
        'testMac_finalize_fail: OK',
        'testMac_start_buffer: OK',
        'testMac_process_buffer: OK',
        'testMac_finalize_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_digest(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'testDigest_init_ok: OK',
        'testDigest_init_fail: OK',
        'testDigest_free_ok: OK',
        'testDigest_free_fail: OK',
        'testDigest_hash_SHA256: OK',
        'testDigest_hash_MD5: OK',
        'testDigest_clone_ok: OK',
        'testDigest_clone_fail: OK',
        'testDigest_process_fail: OK',
        'testDigest_finalize_fail: OK',
        'testDigest_process_buffer: OK',
        'testDigest_finalize_buffer: OK',
        'testDigest_init_ok: OK',
        'testDigest_init_fail: OK',
        'testDigest_free_ok: OK',
        'testDigest_free_fail: OK',
        'testDigest_hash_SHA256: OK',
        'testDigest_hash_MD5: OK',
        'testDigest_clone_ok: OK',
        'testDigest_clone_fail: OK',
        'testDigest_process_fail: OK',
        'testDigest_finalize_fail: OK',
        'testDigest_process_buffer: OK',
        'testDigest_finalize_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_key(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'testKey_import_ok: OK',
        'testKey_import_fail: OK',
        'testKey_export_ok: OK',
        'testKey_export_fail: OK',
        'testKey_generate_ok: OK',
        'testKey_generate_fail: OK',
        'testKey_makePublic_ok: OK',
        'testKey_makePublic_fail: OK',
        'testKey_getParams_ok: OK',
        'testKey_getParams_fail: OK',
        'testKey_loadParams_ok: OK',
        'testKey_loadParams_fail: OK',
        'testKey_free_ok: OK',
        'testKey_free_fail: OK',
        'testKey_getParams_buffer: OK',
        'testKey_loadParams_buffer: OK',
        'testKey_import_ok: OK',
        'testKey_import_fail: OK',
        'testKey_export_ok: OK',
        'testKey_export_fail: OK',
        'testKey_generate_ok: OK',
        'testKey_generate_fail: OK',
        'testKey_makePublic_ok: OK',
        'testKey_makePublic_fail: OK',
        'testKey_getParams_ok: OK',
        'testKey_getParams_fail: OK',
        'testKey_loadParams_ok: OK',
        'testKey_loadParams_fail: OK',
        'testKey_free_ok: OK',
        'testKey_free_fail: OK',
        'testKey_getParams_buffer: OK',
        'testKey_loadParams_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_rng(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    timeout = 15
    result_list = [
        'testRng_getBytes_ok: OK',
        'testRng_getBytes_fail: OK',
        'testRng_reSeed_ok: OK',
        'testRng_reSeed_fail: OK',
        'testRng_reSeed_buffer: OK',
        'testRng_getBytes_buffer: OK',
        'testRng_getBytes_ok: OK',
        'testRng_getBytes_fail: OK',
        'testRng_reSeed_ok: OK',
        'testRng_reSeed_fail: OK',
        'testRng_reSeed_buffer: OK',
        'testRng_getBytes_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_signature(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    timeout = 15
    result_list = [
        'testSignature_init_ok: OK',
        'testSignature_init_fail: OK',
        'testSignature_free_ok: OK',
        'testSignature_free_fail: OK',
        'testSignature_sign_RSA_ok: OK',
        'testSignature_sign_fail: OK',
        'testSignature_verify_RSA_ok: OK',
        'testSignature_verify_fail: OK',
        'testSignature_sign_buffer: OK',
        'testSignature_verify_buffer: OK',
        'testSignature_init_ok: OK',
        'testSignature_init_fail: OK',
        'testSignature_free_ok: OK',
        'testSignature_free_fail: OK',
        'testSignature_sign_RSA_ok: OK',
        'testSignature_sign_fail: OK',
        'testSignature_verify_RSA_ok: OK',
        'testSignature_verify_fail: OK',
        'testSignature_sign_buffer: OK',
        'testSignature_verify_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result
