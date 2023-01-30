# Copyright (C) 2020, HENSOLDT Cyber GmbH
import pytest, sys, tests
from collections import namedtuple

TEST_NAME = 'test_storage_interface'
# we place here 10 sec and not less because at the moment (26/6/2020) we do
# no have yet synchronization mechanism with the boot complete
TEST_TIMEOUT = 10


testers = [
'tester_ramDisk',
'tester_storageServer1',
'tester_storageServer2',
'tester_storageServer3',
'tester_chanMux',
'tester_sdhc'
]

"""
White list of platforms supported by the given tester. If the tester is not in
this list, then it supports all platforms.
"""
test_white_list = {'tester_sdhc': ['sabre', 'sabre-hw'] }

@pytest.fixture(scope="module", params=testers)
def context(boot_with_proxy, request):
    tester = request.param
    platform = request.config.getoption("--target")

    if(tester in test_white_list and platform not in test_white_list[tester]):
        pytest.skip(tester + " not supported on the platform " + platform)

    def run_test(string, timeout_sec):
        tests.run_test_log_match_set(boot_with_proxy, None, [string], timeout_sec)

    TestData = namedtuple('TestData', ['tester', 'run_test'])
    return TestData(tester, run_test)

def test_storage_size_pos(context):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_size_pos: OK",
        TEST_TIMEOUT)

def test_storage_blockSize_pos(context):
    """
    Checks if the block size greater than 0.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_blockSize_pos: OK",
        TEST_TIMEOUT)

def test_storage_state_pos(context):
    """
    Checks if the getState function was called.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_state_pos: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseBegin_pos(context):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseBegin_pos: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseMid_pos(context):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseMid_pos: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseEnd_pos(context):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseEnd_pos: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseZeroBytes_pos(context):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseZeroBytes_pos: OK",
        TEST_TIMEOUT)

@pytest.mark.skip(reason="Not implemented yet. See SEOS-1733")
def test_storage_writeReadEraseLargerThanBuf_neg_ramDisk(context):
    """
    Writes, reads and erases values larger than the defined dataport size,
    expecting the interface call to return an error in that case.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseLargerThanBuf_neg: OK",
        TEST_TIMEOUT)

def test_storage_neighborRegionsUntouched_pos(context):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_neighborRegionsUntouched_pos: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseOutside_neg_ramDisk(context):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseOutside_neg: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseNegOffset_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a negative offset.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseNegOffset_neg: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseIntMax_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a max possible offset.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseIntMax_neg: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseIntMin_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that min possible offset.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseIntMin_neg: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseSizeTooLarge_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseSizeTooLarge_neg: OK",
        TEST_TIMEOUT)

def test_storage_writeReadEraseSizeMax_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases of a maximum size.
    """
    context.run_test(
        context.tester + " -> !!! test_storage_writeReadEraseSizeMax_neg: OK",
        TEST_TIMEOUT)

def test_storage_complete(context):
    """
    Checking if all tests has been completed and that there was no
    failure/exception during the tear down phase.
    """
    context.run_test(
        context.tester + " -> !!! All tests successfully completed.",
        TEST_TIMEOUT)
