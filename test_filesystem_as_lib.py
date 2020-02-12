import pytest
import sys
import os
import re
sys.path.append('../common')
import logs

timeout = 15

#-------------------------------------------------------------------------------
# TEST: partition_manager_init()
#-------------------------------------------------------------------------------

def test_filesystem_hw_init(boot_with_proxy):
    """This test creates a ChanMuxClient and a ProxyNVM instance to allow the initialization of the NVM storage backend.
    Both instances provide and represent the underlying HW storage. 
    
    The behavior of the FileSystem is described at https://wiki.hensoldt-cyber.systems/pages/viewpage.action?spaceKey=HEN&title=SEOS+File+System.

    Underlying SEOS Test System behavior:

        a NVM backend is created at the host system, which can be used as a 
        disk by the SEOS partition manager. """
    proxy_memory_file = "nvm_06"
    if os.path.isfile(proxy_memory_file):
        os.remove(proxy_memory_file)
    with  open(proxy_memory_file,"wb") as f:
        # create 36 MiB NVM file. The size comes from the partition sizes that
        # are defined in the define SEOS system config file. One day we should
        # extend things, so the SEOS system can request the proxy to create a
        # NVM of a given size and that is can quesry the currenty NVM size and
        # fail if this is too small. For now, we have to sync the value here
        # with the SEOSM system manually.
        f.seek( (36*1024*1024) -1 )
        f.write(b"\0")

    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSHWInit: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result    

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_init(boot_with_proxy):
    """ This test initializes the partition manager with the provided storage backend, provided in form of a ProxyNVM instance. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionManagerInit: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_disk(boot_with_proxy):
    """ This test creates an abstract disk representation of the physical storage backend. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionManagerDisk: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_create(boot_with_proxy):
    """ This test fetches all required partitions from the provided system config and initializes them on the disk."""
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionCreate: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_open(boot_with_proxy):
    """ This test opens the created partitions. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionOpen: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_create(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available at the system.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS 
        Currently, only the FAT filesystem is tested. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSCreate: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_mount(boot_with_proxy):
    """ This test mounts all created filesystem instances on each of the partitions available. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionMount: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_file_create(boot_with_proxy):
    """ This test creates different files of different file size and file content on provided partitions. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileCreate: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_file_size(boot_with_proxy):
    """ This test fetches the file size of selected files on provided partitions. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileSize: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_file_read(boot_with_proxy):
    """ This test reads selected files from a provided partition and checks the file content for corruption. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileRead: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_file_delete(boot_with_proxy):
    """ This test deletes selected files from provided partitions. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileDelete: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_wipe(boot_with_proxy):
    """ This test wipes all files from provided partitions. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionWipe: NOT OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_unmount(boot_with_proxy):
    """ This test unmounts selected filesystem instances on provided partitions. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionUnmount: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_close(boot_with_proxy):
    """ This test closes provided partitions. """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionClose: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------