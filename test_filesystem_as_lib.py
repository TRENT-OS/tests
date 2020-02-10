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

def test_filesystem_init_test(boot_with_proxy):
    """This test relies on a ChanMuxClient and a ProxyNVM instance to allow the initialization of the NVM storage backend.
    
    The behavior of the FileSystem is described at https://wiki.hensoldt-cyber.systems/pages/viewpage.action?spaceKey=HEN&title=SEOS+File+System.

    Underlying SEOS Test System behavior:

        a NVM backend is created at the host system, which can be used as a 
        disk by the SEOS partition manager. The partition manager uses the existing
        disk to get the required information."""
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
        'TestFSHWInit_test: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result    

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_create(boot_with_proxy):
    """ This test fetches all required partitions from the SEOS system config and initializes them on disk."""
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
    """ """
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
    """ """
    test_run = boot_with_proxy("test_filesystem_as_lib")
    f_out = test_run[1]

    result_list = [
        'TestFSCreate: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  

#-------------------------------------------------------------------------------