import pytest
import sys
import os
import re
sys.path.append('../common')
import logs

timeout = 60

test_system = "test_partition_manager"

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_getInfoDisk()
#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_partition_manager_get_info_disk_invalid_parameter_error(boot_with_proxy):
    """ This test tries to receive disk data from an invalid disk. 

        - STATUS: NOT WORKING
        - PROBLEM: providing NULL as parameter leads to undefined behavior 
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMDiskInfo_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
        
#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_get_info_disk_fail_to_get_struct_error(boot_with_proxy):
    """ This test tries to receive disk data from a valid disk, but an internal error occurs. 
    
        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMDiskInfo_fail_to_get_struct_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_partition_manager_get_info_disk(boot_with_proxy):
    proxy_memory_file = "nvm_06"
    if os.path.isfile(proxy_memory_file):
        os.remove(proxy_memory_file)
    with  open(proxy_memory_file,"wb") as f:
        # create 36 MiB NVM file. The size comes from the partition sizes that
        # are defined in the define SEOS system config file. One day we should
        # extend things, so the SEOS system can request the proxy to create a
        # NVM of a given size and that is can query the currenty NVM size and
        # fail if this is too small. For now, we have to sync the value here
        # with the SEOSM system manually.
        f.seek( (36*1024*1024) -1 )
        f.write(b"\0")

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]   

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMDiskInfo: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_partition_manager_get_info_partition_inexistent_partition_error(boot_with_proxy):
    """ This test gets the partition info of an inexistent partition with a partition ID that exceeds the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 2
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMPartitionInfo_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_partition_manager_get_info_partition_empty_shadow_partition_error(boot_with_proxy):
    """ This test gets the partition info of an inexistent partition with a partition ID that equals the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 1
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMPartitionInfo_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))   

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_partition_manager_get_info_partition_invalid_parameter_error(boot_with_proxy):
    """ This test tries to get the partition info of an invalid partition.

        - STATUS: NOT WORKING
        - PROBLEM: providing NULL as parameter leads to undefined behavior
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMPartitionInfo_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_fail_to_get_struct_error(boot_with_proxy):
    """ This test gets the partition info of a valid partition, but an internal error occurs.
        
        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMPartitionInfo_fail_to_get_struct_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_get_info_partition(boot_with_proxy):
    """ This test gets the partition infos of all valid partitions residing on disk.
            
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMPartitionInfo: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))   

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_open()
#-------------------------------------------------------------------------------

def test_partition_manager_open_inexistent_partition_error(boot_with_proxy):
    """ This test opens an inexistent partition with a partition ID that exceeds the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 2
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMOpen_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_open_empty_shadow_partition_error(boot_with_proxy):
    """ This test opens an inexistent partition with a partition ID that equals the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 1
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMOpen_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_open_internal_object_error(boot_with_proxy):
    """ This test opens a valid partition, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMOpen_internal_object_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_open_error(boot_with_proxy):
    """ This test opens a valid partition, but an open error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMOpen_open_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_open(boot_with_proxy):
    """ This test opens a valid partition residing on a valid disk, available at the host system.
            
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMOpen: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_open_again(boot_with_proxy):
    """ This test opens an already opened valid partition again.
                
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMOpen: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_write()
#-------------------------------------------------------------------------------

def test_partition_manager_write_insufficient_databuffer_error(boot_with_proxy):
    """ This test writes several times to different locations (offsets) on a valid partition, 
    using a length that exceeds the databuffer (DATABUFFER_SIZE) provided within the system config file. 

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_insufficient_databuffer_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_partition_manager_write_invalid_buffer_error(boot_with_proxy):
    """ This test writes several times from different locations (offsets) on a valid partition, providing an invalid buffer. 

        - STATUS: NOT WORKING
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_invalid_buffer_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_write_inexistent_partition_error(boot_with_proxy):
    """ This test writes to an inexistent partition with a partition ID that exceeds the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 2
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_write_empty_shadow_partition_error(boot_with_proxy):
    """ This test writes to an inexistent partition with a partition ID that equals the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 1
  
        - STATUS: OK
        - PROBLEM: providing a partition id that equals the amount of partitions available detects the creation of an empty shadow partition
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_write_invalid_parameter_error(boot_with_proxy):
    """ This test writes to different locations (offsets) on a valid partition, providing invalid parameters. 

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: 
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_write_internal_object_error(boot_with_proxy):
    """ This test writes to a valid partition, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_internal_object_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_write_offset_error(boot_with_proxy):
    """ This test writes to a valid partition, but uses an invalid offset.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_offset_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_write_error(boot_with_proxy):
    """ This test writes to a valid partition, but a write error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite_write_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_write(boot_with_proxy):
    """ This test writes several times with varying length at different locations (offsets) on a valid partition, residing on a valid disk, available at the host system. 

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMWrite: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_read()
#-------------------------------------------------------------------------------

def test_partition_manager_read_insufficient_databuffer_error(boot_with_proxy):
    """ This test reads several times from different locations (offsets) on a valid partition, providing an invalid buffer. 

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_insufficient_databuffer_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_partition_manager_read_invalid_buffer_error(boot_with_proxy):
    """ This test reads several times from different locations (offsets) on a valid partition, providing an invalid buffer. 

        - STATUS: NOT WORKING
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_invalid_buffer_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_read_inexistent_partition_error(boot_with_proxy):
    """ This test reads from an inexistent partition with a partition ID that exceeds the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 2
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_read_empty_shadow_partition_error(boot_with_proxy):
    """ This test reads from an inexistent partition with a partition ID that equals the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 1
  
        - STATUS: OK
        - PROBLEM: providing a partition id that equals the amount of partitions available detects the creation of an empty shadow partition
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_read_invalid_parameter_error(boot_with_proxy):
    """ This test reads from different locations (offsets) on a valid partition, providing invalid parameters. 

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: 
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_read_internal_object_error(boot_with_proxy):
    """ This test reads from a valid partition, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_internal_object_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_read_offset_error(boot_with_proxy):
    """ This test reads from a valid partition, but uses an invalid offset.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_offset_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_read_error(boot_with_proxy):
    """ This test reads from a valid partition, but a read error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead_read_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_read(boot_with_proxy):
    """ This test reads several times from different locations (offsets) on a valid partition, residing on a valid disk, available at the host system. 

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMRead: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_close()
#-------------------------------------------------------------------------------

def test_partition_manager_close_inexistent_partition_error(boot_with_proxy):
    """ This test closes an inexistent partition with a partition ID that exceeds the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 2
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMClose_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_close_empty_shadow_partition_error(boot_with_proxy):
    """ This test closes an inexistent partition with a partition ID that equals the amount of partitions available. 
    Example: Maximum number of partitions = 1
    Test: partition id = 1
  
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMClose_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_close_internal_object_error(boot_with_proxy):
    """ This test closes a valid partition, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMClose_internal_object_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 
        
#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_partition_manager_close_error(boot_with_proxy):
    """ This test closes a valid partition, but a close error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMClose_close_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_close(boot_with_proxy):
    """ This test closes a valid partition residing on a valid disk, available at the host system.
        Side test: check if partition had to be opended before closing  

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMClose: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------

def test_partition_manager_close_again(boot_with_proxy):
    """ This test closes an already closed valid partition again.
                
        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestPMClose: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail)) 

#-------------------------------------------------------------------------------