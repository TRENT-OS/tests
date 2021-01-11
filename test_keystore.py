import pytest

import sys

import logs # logs module from the common directory in TA
import os
import re
import time

import test_parser as parser

test_system = "test_keystore"
# based in the profiling in CI, 180 sec should be enough. Most tests finish
# well under 60 seconds, just sometimes tests can take much longer. Might be
# related to CI system load in the end.
timeout = 180


#-------------------------------------------------------------------------------
def test_key_store_unit_tests(boot_with_proxy):
    """
    Run unit tests (import, read, delete) with KeySrore (using FAT file system)
    Scenario 1: local keystore
    """

    parser.check_test(boot_with_proxy(test_system),\
                        timeout,\
                        'keyStoreUnitTests')


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_AES(boot_with_proxy):
    """
    import AES-256 key to KeyStore using (using FAT file system)
    Scenario 3: local keystore
    """

    parser.check_test(boot_with_proxy(test_system),
                        timeout,
                        'testKeyStoreAES')


#-------------------------------------------------------------------------------
def test_key_store_integration_tests_keyPair(boot_with_proxy):
    """
    import RSA-128 key pair to KeyStore using FAT file system
    Scenario 5: local keystore
    """

    parser.check_test(boot_with_proxy(test_system),
                        timeout,
                        'testKeyStoreKeyPair')


#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_copy(boot_with_proxy):
    """
    Copy key from one keystore to another (using FAT file system)
    Scenario 7: local keystore
    """

    parser.check_test(boot_with_proxy(test_system),
                        timeout,
                        'keyStoreCopyKeyTest')


#-------------------------------------------------------------------------------
def test_key_store_multi_instance_tests_move(boot_with_proxy):
    """
    Move key from one keystore to another (using FAT file system)
    Scenario 9: local keystore
    """

    parser.check_test(boot_with_proxy(test_system),
                        timeout,
                        'keyStoreMoveKeyTest')
