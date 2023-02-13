#
# Copyright (C) 2020-2023, HENSOLDT Cyber GmbH
#

import pytest
import tests

#-------------------------------------------------------------------------------
# Tester and list of platforms supported by it. If the list is None,,then the
# tester supports all platforms.
TESTERS = {
    'tester_ramDisk': None,
    'tester_storageServer1': None,
    'tester_storageServer2': None,
    'tester_storageServer3': None,
    'tester_chanMux': None,
    'tester_sdhc': ['sabre', 'sabre-hw'],
}


#-------------------------------------------------------------------------------
class StorageTestRunner():

    #---------------------------------------------------------------------------
    def __init__(self, fixture, tester):
        self.fixture = fixture
        self.tester = tester

    #---------------------------------------------------------------------------
    def run_test(self, string, timeout_sec = 10):
        tests.run_test_log_match_set(
            self.fixture,
            'test_storage_interface',
            [ f'{self.tester} -> !!! {string}' ],
            timeout_sec)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module", params=list(TESTERS.keys()))
def context(boot_with_proxy, request):
    tester = request.param
    platform = request.config.option.target

    if not tester in TESTERS:
        pytest.fail(f'unknown tester: {tester}')

    plat_list = TESTERS.get(tester)
    if (plat_list is not None) and (platform not in plat_list):
        pytest.skip(f'{tester} not supported on the platform {platform}')

    return StorageTestRunner(boot_with_proxy, tester)


#-------------------------------------------------------------------------------
def test_storage_size_pos(context):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    context.run_test('test_storage_size_pos: OK')


#-------------------------------------------------------------------------------
def test_storage_blockSize_pos(context):
    """
    Checks if the block size greater than 0.
    """
    context.run_test('test_storage_blockSize_pos: OK')


#-------------------------------------------------------------------------------
def test_storage_state_pos(context):
    """
    Checks if the getState function was called.
    """
    context.run_test('test_storage_state_pos: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseBegin_pos(context):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    context.run_test('test_storage_writeReadEraseBegin_pos: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseMid_pos(context):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    context.run_test('test_storage_writeReadEraseMid_pos: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseEnd_pos(context):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    context.run_test('test_storage_writeReadEraseEnd_pos: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseZeroBytes_pos(context):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    context.run_test('test_storage_writeReadEraseZeroBytes_pos: OK')


#-------------------------------------------------------------------------------
@pytest.mark.skip(reason="Not implemented yet. See SEOS-1733")
def test_storage_writeReadEraseLargerThanBuf_neg_ramDisk(context):
    """
    Writes, reads and erases values larger than the defined dataport size,
    expecting the interface call to return an error in that case.
    """
    context.run_test('test_storage_writeReadEraseLargerThanBuf_neg: OK')


#-------------------------------------------------------------------------------
def test_storage_neighborRegionsUntouched_pos(context):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    context.run_test('test_storage_neighborRegionsUntouched_pos: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseOutside_neg_ramDisk(context):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    context.run_test('test_storage_writeReadEraseOutside_neg: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseNegOffset_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a negative offset.
    """
    context.run_test('test_storage_writeReadEraseNegOffset_neg: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseIntMax_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a max possible offset.
    """
    context.run_test('test_storage_writeReadEraseIntMax_neg: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseIntMin_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that min possible offset.
    """
    context.run_test('test_storage_writeReadEraseIntMin_neg: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseSizeTooLarge_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    context.run_test('test_storage_writeReadEraseSizeTooLarge_neg: OK')


#-------------------------------------------------------------------------------
def test_storage_writeReadEraseSizeMax_neg_ramDisk(context):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases of a maximum size.
    """
    context.run_test('test_storage_writeReadEraseSizeMax_neg: OK')


#-------------------------------------------------------------------------------
def test_storage_complete(context):
    """
    Checking if all tests has been completed and that there was no
    failure/exception during the tear down phase.
    """
    context.run_test('All tests successfully completed.')
