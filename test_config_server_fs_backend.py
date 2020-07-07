import pytest
import sys

from tests import run_test_log_match, run_test_log_match_set

test_system = "test_config_server_fs_backend"
timeout = 60*10   #due to the heavy usage of the filesystem in the tests, the
                  #timeout is set to 10min

#-------------------------------------------------------------------------------
def test_create_config_file_ok(boot_with_proxy):
    """
    A ConfigFileInjector component is connected to the PartitionManger and creates a
    config file with several parameters of all possible parameter types (int32, int64, string, blob)
    and also at least one blob that spans over several blob blocks.

    Goal:
        The file write functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All parameters are written to the file without any returned error.
    """
    expected_result = 'TestCreateFSBackend: OK'

    run_test_log_match(boot_with_proxy,
                       test_system,
                       expected_result,
                       timeout)

#-------------------------------------------------------------------------------
def test_get_integer32_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer32 parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library.

    Goal:
        The integer32 parameter get functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All integer32 parameters read by the TestApp match the expected written parameters.
    """
    result_list = [
        'TestGetInteger32FromFsBackend_ok: TestApp HandleKind:Local Parameter:App_Parameter_32_0 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp HandleKind:Rpc Parameter:App_Parameter_32_0 OK'
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_get_integer64_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer64 parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library.

    Goal:
        The integer64 parameter get functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All integer64 parameters read by the TestApp match the expected written parameters.
    """
    result_list = [
        'TestGetInteger64FromFsBackend_ok: TestApp HandleKind:Local Parameter:App_Parameter_64_0 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp HandleKind:Rpc Parameter:App_Parameter_64_0 OK'
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_set_integer32_values_in_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer32 parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library to test remote and local calls.

    Goal:
        The integer32 parameter set functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All integer32 parameters set by the TestApp can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsU32_ok: TestApp HandleKind:Local Parameter:App_Parameter_32_0 OK',
        'TestParameterSetValueAsU32_ok: TestApp HandleKind:Rpc Parameter:App_Parameter_32_0 OK'
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_set_integer64_values_in_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer64 parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library to test remote and local calls.

    Goal:
        The integer64 parameter set functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All integer64 parameters set by the TestApp can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsU64_ok: TestApp HandleKind:Local Parameter:App_Parameter_64_0 OK',
        'TestParameterSetValueAsU64_ok: TestApp HandleKind:Rpc Parameter:App_Parameter_64_0 OK'
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)