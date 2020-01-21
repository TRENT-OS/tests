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
        'TestAgreement_init_ok: OK',
        'TestAgreement_init_fail: OK',
        'TestAgreement_compute_DH_ok: OK',
        'TestAgreement_compute_DH_rnd_ok: OK',
        'TestAgreement_compute_ECDH_ok: OK',
        'TestAgreement_compute_ECDH_rnd_ok: OK',
        'TestAgreement_compute_fail: OK',
        'TestAgreement_free_ok: OK',
        'TestAgreement_free_fail: OK',
        'TestAgreement_agree_buffer: OK',
        'TestAgreement_init_ok: OK',
        'TestAgreement_init_fail: OK',
        'TestAgreement_compute_DH_ok: OK',
        'TestAgreement_compute_DH_rnd_ok: OK',
        'TestAgreement_compute_ECDH_ok: OK',
        'TestAgreement_compute_ECDH_rnd_ok: OK',
        'TestAgreement_compute_fail: OK',
        'TestAgreement_free_ok: OK',
        'TestAgreement_free_fail: OK',
        'TestAgreement_agree_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_cipher(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'TestCipher_init_ok: OK',
        'TestCipher_init_fail: OK',
        'TestCipher_free_ok: OK',
        'TestCipher_free_fail: OK',
        'TestCipher_encrypt_AES_ECB: OK',
        'TestCipher_decrypt_AES_ECB: OK',
        'TestCipher_encrypt_AES_CBC: OK',
        'TestCipher_decrypt_AES_CBC: OK',
        'TestCipher_encrypt_AES_GCM: OK',
        'TestCipher_decrypt_AES_GCM_ok: OK',
        'TestCipher_decrypt_AES_GCM_fail: OK',
        'TestCipher_start_fail: OK',
        'TestCipher_process_fail: OK',
        'TestCipher_finalize_fail: OK',
        'TestCipher_init_buffer: OK',
        'TestCipher_start_buffer: OK',
        'TestCipher_process_buffer: OK',
        'TestCipher_finalize_buffer: OK',
        'TestCipher_init_ok: OK',
        'TestCipher_init_fail: OK',
        'TestCipher_free_ok: OK',
        'TestCipher_free_fail: OK',
        'TestCipher_encrypt_AES_ECB: OK',
        'TestCipher_decrypt_AES_ECB: OK',
        'TestCipher_encrypt_AES_CBC: OK',
        'TestCipher_decrypt_AES_CBC: OK',
        'TestCipher_encrypt_AES_GCM: OK',
        'TestCipher_decrypt_AES_GCM_ok: OK',
        'TestCipher_decrypt_AES_GCM_fail: OK',
        'TestCipher_start_fail: OK',
        'TestCipher_process_fail: OK',
        'TestCipher_finalize_fail: OK',
        'TestCipher_init_buffer: OK',
        'TestCipher_start_buffer: OK',
        'TestCipher_process_buffer: OK',
        'TestCipher_finalize_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_mac(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'TestMac_init_ok: OK',
        'TestMac_init_fail: OK',
        'TestMac_free_ok: OK',
        'TestMac_free_fail: OK',
        'TestMac_mac_HMAC_MD5: OK',
        'TestMac_mac_HMAC_SHA256: OK',
        'TestMac_start_fail: OK',
        'TestMac_process_fail: OK',
        'TestMac_finalize_fail: OK',
        'TestMac_start_buffer: OK',
        'TestMac_process_buffer: OK',
        'TestMac_finalize_buffer: OK',
        'TestMac_init_ok: OK',
        'TestMac_init_fail: OK',
        'TestMac_free_ok: OK',
        'TestMac_free_fail: OK',
        'TestMac_mac_HMAC_MD5: OK',
        'TestMac_mac_HMAC_SHA256: OK',
        'TestMac_start_fail: OK',
        'TestMac_process_fail: OK',
        'TestMac_finalize_fail: OK',
        'TestMac_start_buffer: OK',
        'TestMac_process_buffer: OK',
        'TestMac_finalize_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_digest(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'TestDigest_init_ok: OK',
        'TestDigest_init_fail: OK',
        'TestDigest_free_ok: OK',
        'TestDigest_free_fail: OK',
        'TestDigest_hash_SHA256: OK',
        'TestDigest_hash_MD5: OK',
        'TestDigest_clone_ok: OK',
        'TestDigest_clone_fail: OK',
        'TestDigest_process_fail: OK',
        'TestDigest_finalize_fail: OK',
        'TestDigest_process_buffer: OK',
        'TestDigest_finalize_buffer: OK',
        'TestDigest_init_ok: OK',
        'TestDigest_init_fail: OK',
        'TestDigest_free_ok: OK',
        'TestDigest_free_fail: OK',
        'TestDigest_hash_SHA256: OK',
        'TestDigest_hash_MD5: OK',
        'TestDigest_clone_ok: OK',
        'TestDigest_clone_fail: OK',
        'TestDigest_process_fail: OK',
        'TestDigest_finalize_fail: OK',
        'TestDigest_process_buffer: OK',
        'TestDigest_finalize_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_key(boot):
    test_run = boot(test_system)
    f_out = test_run[1]

    result_list = [
        'TestKey_import_ok: OK',
        'TestKey_import_fail: OK',
        'TestKey_export_ok: OK',
        'TestKey_export_fail: OK',
        'TestKey_generate_ok: OK',
        'TestKey_generate_fail: OK',
        'TestKey_makePublic_ok: OK',
        'TestKey_makePublic_fail: OK',
        'TestKey_getParams_ok: OK',
        'TestKey_getParams_fail: OK',
        'TestKey_loadParams_ok: OK',
        'TestKey_loadParams_fail: OK',
        'TestKey_free_ok: OK',
        'TestKey_free_fail: OK',
        'TestKey_getParams_buffer: OK',
        'TestKey_loadParams_buffer: OK',
        'TestKey_import_ok: OK',
        'TestKey_import_fail: OK',
        'TestKey_export_ok: OK',
        'TestKey_export_fail: OK',
        'TestKey_generate_ok: OK',
        'TestKey_generate_fail: OK',
        'TestKey_makePublic_ok: OK',
        'TestKey_makePublic_fail: OK',
        'TestKey_getParams_ok: OK',
        'TestKey_getParams_fail: OK',
        'TestKey_loadParams_ok: OK',
        'TestKey_loadParams_fail: OK',
        'TestKey_free_ok: OK',
        'TestKey_free_fail: OK',
        'TestKey_getParams_buffer: OK',
        'TestKey_loadParams_buffer: OK',
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
        'TestRng_getBytes_ok: OK',
        'TestRng_getBytes_fail: OK',
        'TestRng_reSeed_ok: OK',
        'TestRng_reSeed_fail: OK',
        'TestRng_reSeed_buffer: OK',
        'TestRng_getBytes_buffer: OK',
        'TestRng_getBytes_ok: OK',
        'TestRng_getBytes_fail: OK',
        'TestRng_reSeed_ok: OK',
        'TestRng_reSeed_fail: OK',
        'TestRng_reSeed_buffer: OK',
        'TestRng_getBytes_buffer: OK',
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
        'TestSignature_init_ok: OK',
        'TestSignature_init_fail: OK',
        'TestSignature_free_ok: OK',
        'TestSignature_free_fail: OK',
        'TestSignature_sign_RSA_ok: OK',
        'TestSignature_sign_fail: OK',
        'TestSignature_verify_RSA_ok: OK',
        'TestSignature_verify_fail: OK',
        'TestSignature_sign_buffer: OK',
        'TestSignature_verify_buffer: OK',
        'TestSignature_init_ok: OK',
        'TestSignature_init_fail: OK',
        'TestSignature_free_ok: OK',
        'TestSignature_free_fail: OK',
        'TestSignature_sign_RSA_ok: OK',
        'TestSignature_sign_fail: OK',
        'TestSignature_verify_RSA_ok: OK',
        'TestSignature_verify_fail: OK',
        'TestSignature_sign_buffer: OK',
        'TestSignature_verify_buffer: OK',
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result
