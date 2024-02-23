#
# Copyright (C) 2020-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import pytest, sys
import test_parser as parser

TEST_NAME = 'test_cryptoserver'

# AUTOGENERATED TEST FUNCTIONS BELOW -------------------------------------------

def test_CryptoServer_storeKey_pos_0(boot_with_proxy):
    """
    Positive tests for CryptoServer_storeKey(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 30, 'test_CryptoServer_storeKey_pos', single_thread=False)

def test_CryptoServer_storeKey_neg_0(boot_with_proxy):
    """
    Negative tests for CryptoServer_storeKey(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 15, 'test_CryptoServer_storeKey_neg', single_thread=False)

def test_CryptoServer_loadKey_pos_0(boot_with_proxy):
    """
    Positive tests for CryptoServer_loadKey(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 15, 'test_CryptoServer_loadKey_pos', single_thread=False)

def test_CryptoServer_loadKey_neg_0(boot_with_proxy):
    """
    Negative tests for CryptoServer_loadKey(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 15, 'test_CryptoServer_loadKey_neg', single_thread=False)

def test_CryptoServer_useKey_0(boot_with_proxy):
    """
    Import a key in the Crypto API, then store it on the server. The free it from the
    Crypto API and load it again from the CryptoServer. Finally use the key to make
    sure that we have loaded the correct one.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 10, 'test_CryptoServer_useKey', single_thread=False)

def test_CryptoServer_access_0(boot_with_proxy):
    """
    Run four clients against CryptoServer and check that the configured access
    matrix (lower triagonal form) is respected. Check the output of client with
    ID 101.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 15, 'test_CryptoServer_access', 'my_id=101', single_thread=False)

def test_CryptoServer_storageLimit_0(boot_with_proxy):
    """
    Try to add more and more keys to a client's keystore. At some point, the CryptoServer
    should deny further additions as some defined storageLimit is reached.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 10, 'test_CryptoServer_storageLimit', single_thread=False)

def test_CryptoServer_access_1(boot_with_proxy):
    """
    Run four clients against CryptoServer and check that the configured access
    matrix (lower triagonal form) is respected. Check the output of client with
    ID 101.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 10, 'test_CryptoServer_access', 'my_id=104', single_thread=False)

def test_CryptoServer_access_2(boot_with_proxy):
    """
    Run four clients against CryptoServer and check that the configured access
    matrix (lower triagonal form) is respected. Check the output of client with
    ID 102.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 10, 'test_CryptoServer_access', 'my_id=103', single_thread=False)

def test_CryptoServer_access_3(boot_with_proxy):
    """
    Run four clients against CryptoServer and check that the configured access
    matrix (lower triagonal form) is respected. Check the output of client with
    ID 103.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 5, 'test_CryptoServer_access', 'my_id=102', single_thread=False)
