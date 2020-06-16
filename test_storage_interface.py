import pytest, sys
sys.path.append('../common')
import test_parser as parser

TEST_NAME = 'test_storage_interface'
# May not be used
TEST_TIMEOUT = 5*60

def test_storage_size_pos(boot_with_proxy):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_size_pos')

def test_storage_writeReadEraseBegin_pos(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_writeReadEraseBegin_pos')

def test_storage_writeReadEraseMid_pos(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_writeReadEraseMid_pos')

def test_storage_writeReadEraseEnd_pos(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_writeReadEraseEnd_pos')

def test_storage_writeReadEraseZeroBytes_pos(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_writeReadEraseZeroBytes_pos')

@pytest.mark.skip(reason="Proxy Nvm crashes.")
def test_storage_writeReadEraseOutside_neg(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_writeReadEraseOutside_neg')

@pytest.mark.skip(reason="Proxy Nvm causes fault.")
def test_storage_writeReadEraseTooLarge_neg(boot_with_proxy):
    """
    Proxy Nvm shall validate input paramaters and do not allow write, reads, and
    erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_writeReadEraseTooLarge_neg')

def test_storage_neighborRegionsUntouched_pos(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        1,
        'test_storage_neighborRegionsUntouched_pos')
