
import pytest, sys
import test_parser as parser

TEST_NAME = 'test_filesystem'

# AUTOGENERATED TEST FUNCTIONS BELOW -------------------------------------------

def test_OS_FileSystem_format_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 4, 'test_OS_FileSystem_format')

def test_OS_FileSystem_mount_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_mount')

def test_OS_FileSystemFile_open_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_open')

def test_OS_FileSystemFile_write_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_write')

def test_OS_FileSystemFile_read_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_read')

def test_OS_FileSystemFile_close_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_close')

def test_OS_FileSystemFile_getSize_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_getSize')

def test_OS_FileSystemFile_delete_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_delete')

def test_OS_FileSystem_unmount_0(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_unmount')

def test_OS_FileSystem_format_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_format')

def test_OS_FileSystem_mount_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_mount')

def test_OS_FileSystemFile_open_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_open')

def test_OS_FileSystemFile_write_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_write')

def test_OS_FileSystemFile_read_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_read')

def test_OS_FileSystemFile_close_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_close')

def test_OS_FileSystemFile_getSize_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_getSize')

def test_OS_FileSystemFile_delete_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_delete')

def test_OS_FileSystem_unmount_1(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_unmount')

def test_OS_FileSystem_format_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_format')

def test_OS_FileSystem_mount_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_mount')

def test_OS_FileSystemFile_open_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_open')

def test_OS_FileSystemFile_write_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_write')

def test_OS_FileSystemFile_read_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_read')

def test_OS_FileSystemFile_close_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_close')

def test_OS_FileSystemFile_getSize_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_getSize')

def test_OS_FileSystemFile_delete_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystemFile_delete')

def test_OS_FileSystem_unmount_2(boot):
    """
    <TODO: Describe here what the test does>
    """
    parser.check_test(boot(TEST_NAME), 3, 'test_OS_FileSystem_unmount')

def test_OS_FileSystem_mount_fail_0(boot):
    """
    Format a FS with one FS type, then mount with a different one. Do this for
    all FS types. Calculate SHA256 on storage to make sure failed mounts do not
    change disk contents.
    """
    parser.check_test(boot(TEST_NAME), 20, 'test_OS_FileSystem_mount_fail')