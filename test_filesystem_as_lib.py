import pytest
import sys
import os
import re
sys.path.append('../common')
import logs

# this timeout is used for most of the tests, but some tests known to run much
# longer use a custom value
timeout = 250

test_system = "test_filesystem_as_lib"

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

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSHWInit: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_init()
#--------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_init_config_error(boot_with_proxy):
    """ This test validates the provided system config file, which contains the disk and partition parameters
    required by the partition manager for initialization.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: Bad config parameters can't be tested as the overall test setup requires exactly one global system config file, containing valid parameters.
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMInit_config_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_init_invalid_parameter_error(boot_with_proxy):
    """ This test initializes the partition manager with an invalid storage backend, provided in form of a non-existing ProxyNVM instance.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMInit_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_init_check_config_error(boot_with_proxy):
    """ This test validates the initialized disk and partition(s) including their parameters.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: Bad config parameters can't be tested as the overall test setup requires exactly one global system config file, containing valid parameters.
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMInit_check_config_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_init(boot_with_proxy):
    """ This test initializes the partition manager with a storage backend, provided in form of a ProxyNVM instance.
    The partition manager initializes the partitions provided via the system config.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMInit: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_getInfoDisk()
#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_disk_invalid_parameter_error(boot_with_proxy):
    """ This test tries to receive disk data from an invalid disk.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMDiskInfo_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_get_info_disk_fail_to_get_struct_error(boot_with_proxy):
    """ This test tries to receive disk data from a valid disk, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMDiskInfo_fail_to_get_struct_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_disk(boot_with_proxy):
    """ This test gets the disk info of a valid disk already available at the host system.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMDiskInfo: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_PartitionManager_getInfoPartition()
#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition_inexistent_partition_error(boot_with_proxy):
    """ This test gets the partition info of an inexistent partition with a partition ID that exceeds the amount of partitions available.
    Example: Maximum number of partitions = 1
    Test: partition id = 2

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMPartitionInfo_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition_empty_shadow_partition_error(boot_with_proxy):
    """ This test gets the partition info of an inexistent partition with a partition ID that equals the amount of partitions available.
    Example: Maximum number of partitions = 1
    Test: partition id = 1

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMPartitionInfo_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition_invalid_parameter_error(boot_with_proxy):
    """ This test tries to get the partition info of an invalid partition.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMPartitionInfo_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_manager_fail_to_get_struct_error(boot_with_proxy):
    """ This test tries to get the partition info of a valid partition, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMPartitionInfo_fail_to_get_struct_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_manager_get_info_partition(boot_with_proxy):
    """ This test gets the partition infos of all valid partitions residing on disk.

        - STATUS: OK
    """
    test_run = boot_with_proxy("test_partition_manager")
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPMPartitionInfo: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_init()
#-------------------------------------------------------------------------------

def test_filesystem_partition_init_inexistent_partition_error(boot_with_proxy):
    """ This test fetches an inexistent partition with a partition ID that exceeds the amount of partitions available and tries to initialize it on the disk.
    Example: Maximum number of partitions = 1
    Test: partition id = 2

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionInit_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_init_empty_shadow_partition_error(boot_with_proxy):
    """ This test fetches an inexistent partition with a partition ID that equals the amount of partitions available and tries to initialize it on the disk.
    Example: Maximum number of partitions = 1
    Test: partition id = 1

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionInit_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_init_invalid_partition_mode_error(boot_with_proxy):
    """ This test fetches an existent partition by using an invalid partition mode and tries to initialize it on the disk.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionInit_invalid_partition_mode_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_init_no_disk_error(boot_with_proxy):
    """ This test fetches all required partitions from the provided system config and initializes them on the disk, but a disk error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionInit_no_disk_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_partition_init_init_error(boot_with_proxy):
    """ This test fetches all required partitions from the provided system config and initializes them on the disk, but an init error occurs.

        - STATUS: NOT IMPLEMENTED
        - PROBLEM: internal objects not reachable
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionInit_init_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_init(boot_with_proxy):
    """ This test fetches all required partitions from the provided system config and initializes them on the disk.
    The partitions are assigned a respective partition mode - either for read and/or write.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionInit: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_open() & OS_FilesystemApi_validatePartitionHandle()
#-------------------------------------------------------------------------------

def test_filesystem_partition_open(boot_with_proxy):
    """ This test opens the initialized partitions.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionOpen: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_open_inexistent_partition_error(boot_with_proxy):
    """ This test fetches an inexistent partition with a partition ID that exceeds the amount of partitions available and tries to initialize it on the disk.
    Example: Maximum number of partitions = 1
    Test: partition id = 2

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionOpen_inexistent_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_partition_open_empty_shadow_partition_error(boot_with_proxy):
    """ This test fetches an inexistent partition with a partition ID that equals the amount of partitions available and tries to initialize it on the disk.

    Example: Maximum number of partitions = 1
    Test: partition id = 1

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionOpen_empty_shadow_partition_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_create()
#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_create_invalid_parameter_error(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available, but an internal error occurs.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS
        Currently, only the FAT filesystem is tested.

        - STATUS: NOT IMPLEMENTED
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSCreate_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_create_no_disk_error(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available, but an internal error occurs.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS
        Currently, only the FAT filesystem is tested.

        - STATUS: NOT IMPLEMENTED
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSCreate_no_disk_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_create_resolve_handle_error(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available, but uses an invalid partition handle.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS
        Currently, only the FAT filesystem is tested.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSCreate_resolve_handle_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_create_invalid_filesystem_error(boot_with_proxy):
    """ This test tries to create a filesystem with an invalid type that is
        neither FAT nor SPIFFS and therefore is expected to fail.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSCreate_invalid_filesystem_mode_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT WORKING")
def test_filesystem_create_error(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available, but uses an invalid partition size.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS
        Currently, only the FAT filesystem is tested.

        - STATUS: NOT WORKING
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSCreate_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_create_format_partition(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available at the system and formats partition 1.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS
        Currently, only the FAT filesystem is tested.

        If partition manager and filesystem are running on top of ChanMux, this test can take up to 2 minutes.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    # The test takes long time to perform, so timeout is set to 250 seconds.
    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSCreate_format_partition: OK"
    ],
    250)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_create(boot_with_proxy):
    """ This test initializes a filesystem instance on each partition available at the system and overwrites the partitions.
        The following filesystem types are available right now:
            - FAT (FAT12, FAT16, FAT32)
            - SPIFFS
        Currently, only the FAT filesystem is tested.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSCreate: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_mount()
#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_mount_invalid_parameter_error(boot_with_proxy):
    """ This test mounts the created filesystem instances on the respective partitions available, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSMount_invalid_parameter_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

@pytest.mark.skip(reason="NOT IMPLEMENTED")
def test_filesystem_mount_no_disk_error(boot_with_proxy):
    """ This test mounts the created filesystem instances on the respective partitions available, but an internal error occurs.

        - STATUS: NOT IMPLEMENTED
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSMount_no_disk_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_mount_resolve_handle_error(boot_with_proxy):
    """ This test mounts the created filesystem instances on the respective partitions available, but an internal error occurs.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSMount_resolve_handle_error: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------

def test_filesystem_mount(boot_with_proxy):
    """ This test mounts the created filesystem instances on the respective partitions available.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSMount: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_openFile(), OS_FilesystemApi_writeFile() & OS_FilesystemApi_closeFile()
#-------------------------------------------------------------------------------

def test_filesystem_file_create(boot_with_proxy):
    """ This test creates different files of varying file size and file content on the provided filesystem instances (and the partitions underneath respectively).
        File creation is utilizing OS_FilesystemApi_openFile(), OS_FilesystemApi_writeFile() & OS_FilesystemApi_closeFile() functions.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSFileCreate: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_getSizeOfFile()
#-------------------------------------------------------------------------------

def test_filesystem_file_size(boot_with_proxy):
    """ This test fetches the file size of selected files on the provided filesystem instances (and the partitions underneath respectively).

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSFileSize: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_openFile(), OS_FilesystemApi_readFile() & OS_FilesystemApi_closeFile()
#-------------------------------------------------------------------------------

def test_filesystem_file_read(boot_with_proxy):
    """ This test reads selected files from provided filesystem instances (and the partitions underneath respectively) and checks the file content for corruption.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSFileRead: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_deleteFile()
#-------------------------------------------------------------------------------

def test_filesystem_file_delete(boot_with_proxy):
    """ This test deletes selected files from provided filesystem instances (and the partitions underneath respectively).

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSFileDelete: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_wipe()
#-------------------------------------------------------------------------------

def test_filesystem_partition_wipe(boot_with_proxy):
    """ This test wipes all files from provided partitions. Currently only works for small partitions, as wiping large partitions takes too long.
    If partition manager and filesystem are running on top of ChanMux, this test can take up to 2 minutes.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    # The test takes long time to perform, so timeout is set to 250 seconds.
    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionWipe: OK"
    ],
    250)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_unmount()
#-------------------------------------------------------------------------------

def test_filesystem_unmount(boot_with_proxy):
    """ This test unmounts selected filesystem instances on provided partitions.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSUnmount: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
# TEST: OS_FilesystemApi_close()
#-------------------------------------------------------------------------------

def test_filesystem_partition_close(boot_with_proxy):
    """ This test closes provided partitions.

        - STATUS: OK
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "TestFSPartitionClose: OK"
    ],
    timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))

#-------------------------------------------------------------------------------
