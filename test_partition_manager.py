import pytest
import sys
import os
import re
sys.path.append('../common')
import logs

timeout = 15

def test_partition_manager_get_info_disk(boot_with_proxy):
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

    test_run = boot_with_proxy("demo_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestPMInit_get_info_disk: OK'
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result    

#-------------------------------------------------------------------------------

def test_partition_manager_get_info_disk_fake_disk(boot_with_proxy):
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestPMInit_get_info_disk_fake_disk: OK'
        
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  


#-------------------------------------------------------------------------------

def test_partition_manager_get_info_disk_fail(boot_with_proxy):
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    result_list = [
        'TestPMInit_get_info_disk_fail: OK'
        
    ]
    for result in result_list:
        (text,match) = logs.get_match_in_line(f_out,re.compile(result),timeout)
        assert match == result  