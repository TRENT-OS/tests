# Copyright (C) 2020, HENSOLDT Cyber GmbH
import pytest, sys
sys.path.append('../common')
import test_parser as parser

TEST_NAME = 'test_storage_interface'
TEST_TIMEOUT = 1

"""
             #####                          #     #
            #     # #    #   ##   #    #    ##   ## #    # #    #
            #       #    #  #  #  ##   #    # # # # #    #  #  #
            #       ###### #    # # #  #    #  #  # #    #   ##
            #       #    # ###### #  # #    #     # #    #   ##
            #     # #    # #    # #   ##    #     # #    #  #  #
             #####  #    # #    # #    #    #     #  ####  #    #
"""

def test_storage_size_pos_chanmuxStorage(boot_with_proxy):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_size_pos', 'idx=0')

def test_storage_writeReadEraseBegin_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseBegin_pos', 'idx=0')

def test_storage_writeReadEraseMid_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseMid_pos', 'idx=0')

def test_storage_writeReadEraseEnd_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseEnd_pos', 'idx=0')

def test_storage_writeReadEraseZeroBytes_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseZeroBytes_pos', 'idx=0')

@pytest.mark.skip(reason="ChanMux crashes, see SEOS-1431")
def test_storage_writeReadEraseOutside_neg_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseOutside_neg', 'idx=0')

@pytest.mark.skip(reason="ChanMux causes fault, see SEOS-1431")
def test_storage_writeReadEraseTooLarge_neg_chanmuxStorage(boot_with_proxy):
    """
    ChanMuxStorage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseTooLarge_neg_0', 'idx=0')

def test_storage_neighborRegionsUntouched_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_neighborRegionsUntouched_pos', 'idx=0')

"""
        ########.....###....##.....##       ########..####..######..##....##
        ##.....##...##.##...###...###       ##.....##..##..##....##.##...##.
        ##.....##..##...##..####.####       ##.....##..##..##.......##..##..
        ########..##.....##.##.###.##       ##.....##..##...######..#####...
        ##...##...#########.##.....##       ##.....##..##........##.##..##..
        ##....##..##.....##.##.....##       ##.....##..##..##....##.##...##.
        ##.....##.##.....##.##.....##       ########..####..######..##....##
"""

def test_storage_size_pos_ramDisk(boot_with_proxy):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_size_pos', 'idx=1')

def test_storage_writeReadEraseBegin_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseBegin_pos', 'idx=1')

def test_storage_writeReadEraseMid_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseMid_pos', 'idx=1')

def test_storage_writeReadEraseEnd_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseEnd_pos', 'idx=1')

def test_storage_writeReadEraseZeroBytes_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseZeroBytes_pos', 'idx=1')

@pytest.mark.skip(reason="ChanMux crashes, see SEOS-1431")
def test_storage_writeReadEraseOutside_neg_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseOutside_neg', 'idx=1')

@pytest.mark.skip(reason="ChanMux causes fault, see SEOS-1431")
def test_storage_writeReadEraseTooLarge_neg_ramDisk(boot_with_proxy):
    """
    ChanMuxStorage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseTooLarge_neg_0', 'idx=1')

def test_storage_neighborRegionsUntouched_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_neighborRegionsUntouched_pos', 'idx=1')