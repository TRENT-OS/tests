# Copyright (C) 2020, HENSOLDT Cyber GmbH
import pytest, sys

import test_parser as parser

TEST_NAME = 'test_storage_interface'
# we place here 10 sec and not less because at the moment (26/6/2020) we do
# no have yet synchronization mechanism with the boot complete
TEST_TIMEOUT = 10

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
        'test_storage_size_pos', 'idx=0')

def test_storage_blockSize_pos_ramDisk(boot_with_proxy):
    """
    Checks if the block size greater than 0.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_blockSize_pos', 'idx=0')

def test_storage_writeReadEraseBegin_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseBegin_pos', 'idx=0')

def test_storage_writeReadEraseMid_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseMid_pos', 'idx=0')

def test_storage_writeReadEraseEnd_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseEnd_pos', 'idx=0')

def test_storage_writeReadEraseZeroBytes_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseZeroBytes_pos', 'idx=0')

def test_storage_neighborRegionsUntouched_pos_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_neighborRegionsUntouched_pos', 'idx=0')

def test_storage_writeReadEraseOutside_neg_ramDisk(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseOutside_neg', 'idx=0')

def test_storage_writeReadEraseNegOffset_neg_ramDisk(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a negative offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseNegOffset_neg', 'idx=0')

def test_storage_writeReadEraseIntMax_neg_ramDisk(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a max possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMax_neg', 'idx=0')

def test_storage_writeReadEraseIntMin_neg_ramDisk(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that min possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMin_neg', 'idx=0')

def test_storage_writeReadEraseSizeTooLarge_neg_ramDisk(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeTooLarge_neg', 'idx=0')

def test_storage_writeReadEraseSizeMax_neg_ramDisk(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases of a maximum size.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeMax_neg', 'idx=0')

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
        'test_storage_size_pos', 'idx=1')

def test_storage_blockSize_pos_chanmuxStorage(boot_with_proxy):
    """
    Checks if the block size greater than 0.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_blockSize_pos', 'idx=1')

def test_storage_writeReadEraseBegin_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseBegin_pos', 'idx=1')

def test_storage_writeReadEraseMid_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseMid_pos', 'idx=1')

def test_storage_writeReadEraseEnd_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseEnd_pos', 'idx=1')

def test_storage_writeReadEraseZeroBytes_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseZeroBytes_pos', 'idx=1')

def test_storage_neighborRegionsUntouched_pos_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_neighborRegionsUntouched_pos', 'idx=1')

def test_storage_writeReadEraseOutside_neg_chanmuxStorage(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseOutside_neg', 'idx=1')

def test_storage_writeReadEraseNegOffset_neg_chanmuxStorage(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a negative offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseNegOffset_neg', 'idx=1')

def test_storage_writeReadEraseIntMax_neg_chanmuxStorage(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a max possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMax_neg', 'idx=1')

def test_storage_writeReadEraseIntMin_neg_chanmuxStorage(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that min possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMin_neg', 'idx=1')

def test_storage_writeReadEraseSizeTooLarge_neg_chanmuxStorage(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeTooLarge_neg', 'idx=1')

def test_storage_writeReadEraseSizeMax_neg_chanmuxStorage(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases of a maximum size.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeMax_neg', 'idx=1')

"""
.     .######..########..#######..########.....###.....######...########..
.     ##....##....##....##.....##.##.....##...##.##...##....##..##........
.     ##..........##....##.....##.##.....##..##...##..##........##........
.     .######.....##....##.....##.########..##.....##.##...####.######....
.     ......##....##....##.....##.##...##...#########.##....##..##........
.     ##....##....##....##.....##.##....##..##.....##.##....##..##........
.     .######.....##.....#######..##.....##.##.....##..######...########..

.          .######..########.########..##.....##.########.########.
.          ##....##.##.......##.....##.##.....##.##.......##.....##
.          ##.......##.......##.....##.##.....##.##.......##.....##
.          .######..######...########..##.....##.######...########.
.          ......##.##.......##...##....##...##..##.......##...##..
.          ##....##.##.......##....##....##.##...##.......##....##.
.          .######..########.##.....##....###....########.##.....##

           #                    #####
          ##    ####  #####    #     # #      # ###### #    # #####
         # #   #        #      #       #      # #      ##   #   #
           #    ####    #      #       #      # #####  # #  #   #
           #        #   #      #       #      # #      #  # #   #
           #   #    #   #      #     # #      # #      #   ##   #
         #####  ####    #       #####  ###### # ###### #    #   #
"""

def test_storage_size_pos_StorageServer1(boot_with_proxy):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_size_pos', 'idx=2')

def test_storage_blockSize_pos_StorageServer1(boot_with_proxy):
    """
    Checks if the block size greater than 0.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_blockSize_pos', 'idx=2')

def test_storage_writeReadEraseBegin_pos_StorageServer1(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseBegin_pos', 'idx=2')

def test_storage_writeReadEraseMid_pos_StorageServer1(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseMid_pos', 'idx=2')

def test_storage_writeReadEraseEnd_pos_StorageServer1(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseEnd_pos', 'idx=2')

def test_storage_writeReadEraseZeroBytes_pos_StorageServer1(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseZeroBytes_pos', 'idx=2')

def test_storage_neighborRegionsUntouched_pos_StorageServer1(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_neighborRegionsUntouched_pos', 'idx=2')

def test_storage_writeReadEraseOutside_neg_StorageServer1(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseOutside_neg', 'idx=2')

def test_storage_writeReadEraseNegOffset_neg_StorageServer1(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a negative offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseNegOffset_neg', 'idx=2')

def test_storage_writeReadEraseIntMax_neg_StorageServer1(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a max possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMax_neg', 'idx=2')

def test_storage_writeReadEraseIntMin_neg_StorageServer1(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that min possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMin_neg', 'idx=2')

def test_storage_writeReadEraseSizeTooLarge_neg_StorageServer1(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeTooLarge_neg', 'idx=2')

def test_storage_writeReadEraseSizeMax_neg_StorageServer1(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases of a maximum size.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeMax_neg', 'idx=2')

"""
         #####                    #####
        #     # #    # #####     #     # #      # ###### #    # #####
              # ##   # #    #    #       #      # #      ##   #   #
         #####  # #  # #    #    #       #      # #####  # #  #   #
        #       #  # # #    #    #       #      # #      #  # #   #
        #       #   ## #    #    #     # #      # #      #   ##   #
        ####### #    # #####      #####  ###### # ###### #    #   #
"""

def test_storage_size_pos_StorageServer2(boot_with_proxy):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_size_pos', 'idx=3')

def test_storage_blockSize_pos_StorageServer2(boot_with_proxy):
    """
    Checks if the block size greater than 0.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_blockSize_pos', 'idx=3')

def test_storage_writeReadEraseBegin_pos_StorageServer2(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseBegin_pos', 'idx=3')

def test_storage_writeReadEraseMid_pos_StorageServer2(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseMid_pos', 'idx=3')

def test_storage_writeReadEraseEnd_pos_StorageServer2(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseEnd_pos', 'idx=3')

def test_storage_writeReadEraseZeroBytes_pos_StorageServer2(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseZeroBytes_pos', 'idx=3')

def test_storage_neighborRegionsUntouched_pos_StorageServer2(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_neighborRegionsUntouched_pos', 'idx=3')

def test_storage_writeReadEraseOutside_neg_StorageServer2(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseOutside_neg', 'idx=3')

def test_storage_writeReadEraseNegOffset_neg_StorageServer2(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a negative offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseNegOffset_neg', 'idx=3')

def test_storage_writeReadEraseIntMax_neg_StorageServer2(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a max possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMax_neg', 'idx=3')

def test_storage_writeReadEraseIntMin_neg_StorageServer2(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that min possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMin_neg', 'idx=3')

def test_storage_writeReadEraseSizeTooLarge_neg_StorageServer2(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeTooLarge_neg', 'idx=3')

def test_storage_writeReadEraseSizeMax_neg_StorageServer2(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases of a maximum size.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeMax_neg', 'idx=3')

"""
         #####                    #####
        #     # #####  #####     #     # #      # ###### #    # #####
              # #    # #    #    #       #      # #      ##   #   #
         #####  #    # #    #    #       #      # #####  # #  #   #
              # #####  #    #    #       #      # #      #  # #   #
        #     # #   #  #    #    #     # #      # #      #   ##   #
         #####  #    # #####      #####  ###### # ###### #    #   #
"""

def test_storage_size_pos_StorageServer3(boot_with_proxy):
    """
    Checks if the storage is big enough i.e. three times greater than the test
    string, so that the test string can be written at the beginning, in the
    center and at the end of it.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_size_pos', 'idx=4')

def test_storage_blockSize_pos_StorageServer3(boot_with_proxy):
    """
    Checks if the block size greater than 0.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_blockSize_pos', 'idx=4')

def test_storage_writeReadEraseBegin_pos_StorageServer3(boot_with_proxy):
    """
    Writes, reads and erases the test string at the beginning of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseBegin_pos', 'idx=4')

def test_storage_writeReadEraseMid_pos_StorageServer3(boot_with_proxy):
    """
    Writes, reads and erases the test string in the center of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseMid_pos', 'idx=4')

def test_storage_writeReadEraseEnd_pos_StorageServer3(boot_with_proxy):
    """
    Writes, reads and erases the test string at the end of the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseEnd_pos', 'idx=4')

def test_storage_writeReadEraseZeroBytes_pos_StorageServer3(boot_with_proxy):
    """
    Writes, reads and erases zero bytes in the storage.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseZeroBytes_pos', 'idx=4')

def test_storage_neighborRegionsUntouched_pos_StorageServer3(boot_with_proxy):
    """
    Writes, reads and erases the test string, and verifies that the data in
    front of it and at the back were not corrupted.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_neighborRegionsUntouched_pos', 'idx=4')

def test_storage_writeReadEraseOutside_neg_StorageServer3(boot_with_proxy):
    """
    Writes, reads and erases outside of the storage area expecting the storage
    to report an error in that case.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseOutside_neg', 'idx=4')

def test_storage_writeReadEraseNegOffset_neg_StorageServer3(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a negative offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseNegOffset_neg', 'idx=4')

def test_storage_writeReadEraseIntMax_neg_StorageServer3(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases for a max possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMax_neg', 'idx=4')

def test_storage_writeReadEraseIntMin_neg_StorageServer3(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that min possible offset.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseIntMin_neg', 'idx=4')

def test_storage_writeReadEraseSizeTooLarge_neg_StorageServer3(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases that are too large.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeTooLarge_neg', 'idx=4')

def test_storage_writeReadEraseSizeMax_neg_StorageServer3(boot_with_proxy):
    """
    Storage driver shall validate input paramaters and do not allow
    write, reads, and erases of a maximum size.
    """
    parser.check_test(
        boot_with_proxy(TEST_NAME),
        TEST_TIMEOUT,
        'test_storage_writeReadEraseSizeMax_neg', 'idx=4')
