#
# Copyright (C) 2019-2023, HENSOLDT Cyber GmbH
#

import pytest
import test_parser as parser

"""
Use global timeout everywhere because, due to the grouping, the parser does not
actually wait for the test outputs in the order in which they are produced. So,
the worst case might be that the first check_test() waits for the last line
produced by the test system.
"""
TEST_TIMEOUT = 30

OS_FileSystem_Type_FATFS = 1
OS_FileSystem_Type_SPIFFS = 2
OS_FileSystem_Type_LITTLEFS = 3


FileSystem_Types = [
    pytest.param(OS_FileSystem_Type_LITTLEFS, id='littlefs'),
    pytest.param(OS_FileSystem_Type_SPIFFS, id='spiffs'),
    pytest.param(OS_FileSystem_Type_FATFS, id='fatfs'),
]


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystem_format(boot, fstype):
    """
    Format storage with all available FS libs, which is expected to work in case
    we have expectRemoval=0; if it is set to 1, we expect formatting to fail
    with a NOT_PRESENT error coming from the storage layer.
    """
    test_runner = boot()
    for r in [0, 1, 0, 0]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystem_format',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystem_mount(boot, fstype):
    """
    Mount storage with all available FS libs, which is expected to work in case
    we have expectRemoval=0; if it is set to 1, we expect mounting to fail
    with a NOT_PRESENT error coming from the storage layer.
    """
    test_runner = boot()
    for r in [0, 1, 0]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystem_mount',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystem_maxHandles(boot, fstype):
    """
    For all available FS libs, verify that the maximum number of file handles
    can be used at a time and check that a subsequent attempt to open a file
    results in an out-of-bounds error. Close all opened file handles afterwards.
    """
    test_runner = boot()
    parser.check_test(
        test_runner,
        TEST_TIMEOUT,
        'test_OS_FileSystem_maxHandles',
        f'type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystemFile_open(boot, fstype):
    """
    For each successful format and mount with one of the existing FS libs, open
    a file on the fs. This is expected to work when expectRemoval=0, and should
    fail with NOT_PRESENT error coming from the storage layer.
    """
    test_runner = boot()
    for r in [0, 1, 0, 0]:
        parser.check_test(
            boot(),
            TEST_TIMEOUT,
            'test_OS_FileSystemFile_open',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystemFile_write(boot, fstype):
    """
    For each successfully opened file perform several writes to it. This is
    expected to work when expectRemoval=0, and should fail with NOT_PRESENT
    error coming from the storage layer.
    """
    test_runner = boot()
    for r in [0, 1, 0]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystemFile_write',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystemFile_read(boot, fstype):
    """
    For each successful writes to the opened file perform a read and check the
    results against what was written. This is expected to work when
    expectRemoval=0, and should fail with NOT_PRESENT error coming from the
    storage layer.
    """
    test_runner = boot()
    for r in [0, 1]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystemFile_read',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystemFile_close(boot, fstype):
    """
    For each successfully opened file close it again after writing/reading from
    it. This is expected to work when expectRemoval=0, and should fail with
    NOT_PRESENT error coming from the storage layer.
    """
    test_runner = boot()
    for r in [0, 0, 1]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystemFile_close',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystemFile_getSize(boot, fstype):
    """
    For each successfully created file read its size and compare with the amount
    of bytes written. This is expected to work when expectRemoval=0, and should
    fail with NOT_PRESENT error coming from the storage layer.
    """
    test_runner = boot()
    for r in [0, 1]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystemFile_getSize',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystemFile_delete(boot, fstype):
    """
    For each successfully created file delete it again. This is expected to work
    when expectRemoval=0, and should fail with NOT_PRESENT error coming from the
    storage layer.
    """
    test_runner = boot()
    for r in [0, 1]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystemFile_delete',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystem_unmount(boot, fstype):
    """
    For each successfully mounted FS (once per each FS lib) unmount it again.
    This is always expected to work, as it should not touch the storage and thus
    won't learn that the medium was removed.
    """
    test_runner = boot()
    for r in [0, 0]:
        parser.check_test(
            test_runner,
            TEST_TIMEOUT,
            'test_OS_FileSystem_unmount',
            f'expectRemoval={r},type={fstype}')


#-------------------------------------------------------------------------------
@pytest.mark.parametrize('fstype', FileSystem_Types)
def test_OS_FileSystem_mount_fail(boot, fstype):
    """
    Format a FS with one FS type, then mount with a different one. Do this for
    all FS types. Calculate SHA256 on storage to make sure failed mounts do not
    change disk contents.
    """
    test_runner = boot()
    parser.check_test(test_runner, TEST_TIMEOUT, 'test_OS_FileSystem_mount_fail')
