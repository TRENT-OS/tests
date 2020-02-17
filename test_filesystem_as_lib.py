import pytest
import sys
import os
import re
sys.path.append('../common')
import logs

timeout = 15

#-------------------------------------------------------------------------------
# TEST: HW setup init
#-------------------------------------------------------------------------------

def test_filesystem_hw_init(boot_with_proxy):
    """This test initializes the underlying HW platform for the filesystem. 
    The HW platform consists of two components, which have to be created:
        - a ChanMuxClient instance, allowing the communication between the OS and the host proxy application
        - a ProxyNVM instance, which uses the ChanMuxClient to provide the required NVM storage backend
    
    The behavior of the FileSystem is described at https://wiki.hensoldt-cyber.systems/pages/viewpage.action?spaceKey=HEN&title=SEOS+File+System.

    Underlying SEOS Test System behavior:

        a NVM backend is created at the host system, which can be used as a 
        disk by the SEOS partition manager. 
    """
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
# TEST: partition_manager_init()
#--------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_init_config_error(boot_with_proxy):
    """ This test validates the provided system config file, which contains the disk and partition parameters 
    required by the partition manager for initialization. 
    
        - STATUS: NOT IMPLEMENTED
        - PROBLEM: Bad config parameters can't be tested as the overall test setup requires exactly one global system config file, containing valid parameters.
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPMInit_config_error: NOT IMPLEMENTED'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_init_invalid_parameter_error(boot_with_proxy):
    """ This test initializes the partition manager with an invalid storage backend, provided in form of a non-existing ProxyNVM instance. 

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPMInit_invalid_parameter_error: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_init_check_config_error(boot_with_proxy):
    """ This test validates the initialized disk and partition(s) including their parameters.
    
        - STATUS: NOT IMPLEMENTED
        - PROBLEM: Bad config parameters can't be tested as the overall test setup requires exactly one global system config file, containing valid parameters.
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPMInit_check_config_error: NOT IMPLEMENTED'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_init(boot_with_proxy):
    """ This test initializes the partition manager with a storage backend, provided in form of a ProxyNVM instance.
    The partition manager initializes the partitions provided via the system config. 
            
        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPMInit: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_manager_get_info_disk()
#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_disk_invalid_parameter_error(boot_with_proxy):
    """ This test tries to receive disk data from an invalid disk. 
            
        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPMDiskInfo_invalid_parameter_error: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_get_info_disk_fail_to_get_struct_error(boot_with_proxy):
    """ This test tries to receive disk data from a valid disk, but an internal error occurs. 
    
        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPMDiskInfo_fail_to_get_struct_error: NOT IMPLEMENTED'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_disk(boot_with_proxy):
    """ This test gets the disk info of a valid disk already available at the host system.
        
        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPMDiskInfo: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_manager_get_info_partition()
#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition_inexistent_partition_error(boot_with_proxy):
    """ This test gets the partition info of an inexistent partition with a partition ID that exceeds the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 2
  
        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestFSPMPartitionInfo_inexistent_partition_error: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result 

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition_empty_shadow_partition_error(boot_with_proxy):
    """ This test gets the partition info of an inexistent partition with a partition ID that equals the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 1
  
        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestFSPMPartitionInfo_empty_shadow_partition_error: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result 

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition_invalid_parameter_error(boot_with_proxy):
    """ This test tries to get the partition info of an invalid partition. 

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestFSPMPartitionInfo_invalid_parameter_error: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_fail_to_get_struct_error(boot_with_proxy):
    """ This test tries to get the partition info of a valid partition, but an internal error occurs.
        
        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestFSPMPartitionInfo_fail_to_get_struct_error: NOT IMPLEMENTED'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition(boot_with_proxy):
    """ This test gets the partition infos of all valid partitions residing on disk.
            
        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestFSPMPartitionInfo: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_init()
#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_filesystem_partition_init_inexistent_partition_error(boot_with_proxy):
    """ This test fetches an inexistent partition with a partition ID that exceeds the amount of partitions available and tries to initialize it on the disk.
    Example: Maximum number of partitions = 1
    Test: partition id = 2

        - STATUS: NOT WORKING
        - PROBLEM: Expected return value SEOS_FS_ERROR_INVALID_PARAMETER is not returned -> SEOS_FS_SUCCESS 
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionInit_inexistent_partition_error: NOT WORKING'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_filesystem_partition_init_empty_shadow_partition_error(boot_with_proxy):
    """ This test fetches an inexistent partition with a partition ID that equals the amount of partitions available and tries to initialize it on the disk.
    Example: Maximum number of partitions = 1
    Test: partition id = 1

        - STATUS: NOT WORKING
        - PROBLEM: Expected return value SEOS_FS_ERROR_INVALID_PARAMETER is not returned -> SEOS_FS_SUCCESS
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionInit_empty_shadow_partition_error: NOT WORKING'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_filesystem_partition_init_invalid_partition_mode_error(boot_with_proxy):
    """ This test fetches an existent partition by using an invalid partition mode and tries to initialize it on the disk.

        - STATUS: NOT WORKING
        - PROBLEM: Expected return value SEOS_FS_ERROR_INVALID_PARAMETER is not returned -> SEOS_FS_SUCCESS
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionInit_invalid_partition_mode_error: NOT WORKING'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_init_no_disk_error(boot_with_proxy):
    """ This test fetches all required partitions from the provided system config and initializes them on the disk, but a disk error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionInit_no_disk_error(): NOT IMPLEMENTED'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_init_init_error(boot_with_proxy):
    """ This test fetches all required partitions from the provided system config and initializes them on the disk, but an init error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionInit_init_error(): NOT IMPLEMENTED'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result

#-------------------------------------------------------------------------------

def test_filesystem_partition_init(boot_with_proxy):
    """ This test fetches all required partitions from the provided system config and initializes them on the disk.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionInit: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_open() & is_valid_partition_handle()
#-------------------------------------------------------------------------------

def test_filesystem_partition_open(boot_with_proxy):
    """ This test opens the initialized partitions.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionOpen: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_fs_create()
#-------------------------------------------------------------------------------

def test_filesystem_create(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available at the system.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS 
        Currently, only the FAT filesystem is tested.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSCreate: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_fs_mount()
#-------------------------------------------------------------------------------

def test_filesystem_mount(boot_with_proxy):
    """ This test mounts the created filesystem instances on the respective partitions available.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSMount: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: file_open(), file_write() & file_close()
#-------------------------------------------------------------------------------

def test_filesystem_file_create(boot_with_proxy):
    """ This test creates different files of varying file size and file content on the provided filesystem instances (and the partitions underneath respectively).

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileCreate: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: file_getSize()
#-------------------------------------------------------------------------------

def test_filesystem_file_size(boot_with_proxy):
    """ This test fetches the file size of selected files on the provided filesystem instances (and the partitions underneath respectively).

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileSize: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: file_open(), file_read() & file_close()
#-------------------------------------------------------------------------------

def test_filesystem_file_read(boot_with_proxy):
    """ This test reads selected files from provided filesystem instances (and the partitions underneath respectively) and checks the file content for corruption.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileRead: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: file_delete()
#-------------------------------------------------------------------------------

def test_filesystem_file_delete(boot_with_proxy):
    """ This test deletes selected files from provided filesystem instances (and the partitions underneath respectively).

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSFileDelete: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_wipe()
#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_filesystem_partition_wipe(boot_with_proxy):
    """ This test wipes all files from provided partitions.

        - STATUS: NOT WORKING
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionWipe: NOT WORKING'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_fs_unmount()
#-------------------------------------------------------------------------------

def test_filesystem_unmount(boot_with_proxy):
    """ This test unmounts selected filesystem instances on provided partitions.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSUnmount: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------
# TEST: partition_close()
#-------------------------------------------------------------------------------

def test_filesystem_partition_close(boot_with_proxy):
    """ This test closes provided partitions.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSPartitionClose: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------