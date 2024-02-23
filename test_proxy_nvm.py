#
# Copyright (C) 2019-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import pytest

import sys

import logs # logs module from the common directory in TA
import os
import re
import time

import test_parser as parser

test_system = "test_proxy_nvm"
timeout = 300

def test_proxy_nvm_storage_start_address(boot_with_proxy):
    """This test will check writing and reading at the beginning of the storage.

    Underlying TRENTOS Test System behavior:

        Two TRENTOS Tester components will (in parallel) write a data via the
        NVM abstraction exposed by the Proxy app with a known pattern and then
        read it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    parser.check_test(boot_with_proxy(test_system),\
                        timeout,\
                        'testStorageStartAddr',\
                        single_thread = False,\
                        occurrences = 2)

def test_proxy_nvm_storage_mid_address(boot_with_proxy):
    """This test will check writing and reading in the middle of the storage.

    Underlying TRENTOS Test System behavior:

        Two TRENTOS Tester components will (in parallel) write a data via the
        NVM abstraction exposed by the Proxy app with a known pattern and then
        read it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    parser.check_test(boot_with_proxy(test_system),\
                        timeout,\
                        'testStorageMidAddr',\
                        single_thread = False,\
                        occurrences = 2)

def test_proxy_nvm_storage_end_address(boot_with_proxy):
    """This test will check writing and reading at the end of the storage.

    Underlying TRENTOS Test System behavior:

        Two TRENTOS Tester components will (in parallel) write a data via the
        NVM abstraction exposed by the Proxy app with a known pattern and then
        read it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    parser.check_test(boot_with_proxy(test_system),\
                        timeout,\
                        'testStorageEndAddr',\
                        single_thread = False,\
                        occurrences = 2)

def test_proxy_nvm_storage_overflow(boot_with_proxy):
    """This test will check that writing outside of the bounds (when starting
    from the valid address) results in an error condition.

    Underlying TRENTOS Test System behavior:

        Two TRENTOS Tester components will (in parallel) write a data via the
        NVM abstraction exposed by the Proxy app with a known pattern and then
        read it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    parser.check_test(boot_with_proxy(test_system),\
                        timeout,\
                        'testStorageOverflow',\
                        single_thread = False,\
                        occurrences = 2)

def test_proxy_nvm_storage_underflow(boot_with_proxy):
    """This test will check that writing outside of the bounds (when starting
    underflowed address) results in an error condition.

    Underlying TRENTOS Test System behavior:

        Two TRENTOS Tester components will (in parallel) write a data via the
        NVM abstraction exposed by the Proxy app with a known pattern and then
        read it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    parser.check_test(boot_with_proxy(test_system),\
                        timeout,\
                        'testStorageUnderflow',\
                        single_thread = False,\
                        occurrences = 2)

def test_proxy_nvm_far_out_of_bounds_address(boot_with_proxy):
    """This test will check that writing outside of the bounds (invalid start
    addresses) results in an error condition.

    Underlying TRENTOS Test System behavior:

        Two TRENTOS Tester components will (in parallel) write a data via the
        NVM abstraction exposed by the Proxy app with a known pattern and then
        read it and verify it.

    Test is currently limited to the disk size preconfigured by the proxy
    application:
        - 36  MB for 1st NVM channel
        - 128 KB for 2nd NVM channel
    """

    parser.check_test(boot_with_proxy(test_system),\
                        timeout,\
                        'testStorageFarOutOfBoundAddr',\
                        single_thread = False,\
                        occurrences = 2)
