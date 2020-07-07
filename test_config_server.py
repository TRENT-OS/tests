import pytest
import sys

from tests import run_test_log_match, run_test_log_match_set

test_system = "test_config_server"
timeout = 10  #timeout set to 10sec

#-------------------------------------------------------------------------------
def test_create_handle_ok(boot_with_proxy):
    """
    A handle object is created for a remote and a local SeosConfigLib instance.

    Goal:
        The createHandle function offered by the ConfigServer as library and component
        is successfully tested.
    Success criteria:
        The createHandle function returns OS_SUCCESS for a local and a remote handle.
    """

    result_list = [
        'TestCreateHandle_ok: TestApp1 HandleKind:Local OK',
        'TestCreateHandle_ok: TestApp1 HandleKind:Rpc OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_create_handle_fail(boot_with_proxy):
    """
    The function createHandle is called with empty handles, invalid handle types
    and invalid handle ids.

    Goal:
        The createHandle function offered by the ConfigServer as library and component
        is tested for correct error return codes for the mentioned invalid input.
    Success criteria:
        The The createHandle function correctly returns defined error codes for various
        wrong input data.
    """

    result_list = [
        'TestCreateHandle_fail: TestApp1 HandleKind:Local OK',
        'TestCreateHandle_fail: TestApp1 HandleKind:Rpc OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_domain_enumerator_increment_ok(boot_with_proxy):
    """
    A domain enumerator object is initialized and then incremented by the max domain
    index amount stored in the backend. After testing that the index of the object
    got incremented as expected, the object is closed again.

    Goal:
        The domainEnumeratorIncrement function offered by the ConfigServer as library and component
        is successfully tested.
    Success criteria:
        The index of the domainEnumerator is incremented as expected.
    """

    result_list = [
        'TestDomainEnumerator_increment_ok: TestApp1 HandleKind:Local OK',
        'TestDomainEnumerator_increment_ok: TestApp1 HandleKind:Rpc OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_domain_enumerator_reset_ok(boot_with_proxy):
    """
    A domain enumerator object is initialized and then incremented by the max domain
    index amount stored in the backend. After testing that the index of the object
    got incremented as expected, the index is reset again and it is verified, that
    the new index value is 0 again.

    Goal:
        The domainEnumeratorReset function offered by the ConfigServer as library and component
        is successfully tested.
    Success criteria:
        The index of the domainEnumerator is reset to 0 as expected.
    """
    result_list = [
        'TestDomainEnumerator_reset_ok: TestApp1 HandleKind:Local OK',
        'TestDomainEnumerator_reset_ok: TestApp1 HandleKind:Rpc OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_parameter_enumerator_increment_ok(boot_with_proxy):
    """
    A parameter enumerator object is initialized and then incremented by the max parameter
    index amount stored in the backend for the domain. After testing that the index of the object
    got incremented as expected, the object is closed again.

    Goal:
        The parameterEnumeratorIncrement function offered by the ConfigServer as library and component
        is successfully tested.
    Success criteria:
        The index of the parameterEnumerator is incremented as expected.
    """
    result_list = [
        'TestParameterEnumerator_increment_ok: TestApp1 HandleKind:Local OK',
        'TestParameterEnumerator_increment_ok: TestApp1 HandleKind:Rpc OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_parameter_enumerator_reset_ok(boot_with_proxy):
    """
    A parameter enumerator object is initialized and then incremented by the max parameter
    index amount stored in the backend for the domain. After testing that the index of the object
    got incremented as expected, the index is reset again and it is verified, that
    the new index value is 0 again.

    Goal:
        The parameterEnumeratorReset function offered by the ConfigServer as library and component
        is successfully tested.
    Success criteria:
        The index of the parameterEnumerator is reset to 0 as expected.
    """
    result_list = [
        'TestParameterEnumerator_reset_ok: TestApp1 HandleKind:Local OK',
        'TestParameterEnumerator_reset_ok: TestApp1 HandleKind:Rpc OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
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
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_0 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_0 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_1 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_1 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_2 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_2 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_3 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_3 OK',
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
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_0 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_0 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_1 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_1 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_2 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_2 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_3 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_get_string_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all string parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library.

    Goal:
        The string parameter get functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All string parameters read by the TestApp match the expected written parameters.
    """
    result_list = [
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_0 OK',
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_0 OK',
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_1 OK',
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_1 OK',
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_2 OK',
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_2 OK',
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_3 OK',
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_get_blob_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all blob parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library.

    Goal:
        The blob parameter get functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All blob parameters read by the TestApp match the expected written parameters.
    """
    result_list = [
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_0 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_0 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_1 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_1 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_2 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_2 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_3 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_read_access_rights_from_config_file_ok(boot_with_proxy):
    """
    Asserts that a specific parameter which has been set in the config file with no read access rights
    cannot be accessed from the TestApp.

    Goal:
        The read access rights management of the config server is successfully tested.
    Success criteria:
        Accesssing a parameter which has no read rights will return an error.
    """
    result_list = [
        'TestParameterReadAccessRight_ok: TestApp1 HandleKind:Local Parameter:App2_Parameter_Blob_2 OK',
        'TestParameterReadAccessRight_ok: TestApp1 HandleKind:Rpc Parameter:App2_Parameter_Blob_2 OK',
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
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_0 OK',
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_0 OK',
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_1 OK',
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_1 OK',
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_2 OK',
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_2 OK',
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_3 OK',
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_3 OK',
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
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_0 OK',
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_0 OK',
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_1 OK',
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_1 OK',
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_2 OK',
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_2 OK',
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_3 OK',
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_set_string_values_in_config_file_ok(boot_with_proxy):
    """
    Asserts that all string parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library to test remote and local calls.

    Goal:
        The string parameter set functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All string parameters set by the TestApp can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_0 OK',
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_0 OK',
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_1 OK',
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_1 OK',
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_2 OK',
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_2 OK',
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_3 OK',
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_set_blob_values_in_config_file_ok(boot_with_proxy):
    """
    Asserts that all blob parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by a TestApp connected to a ConfigServer component and additionally
    using the ConfigServer library to test remote and local calls.

    Goal:
        The blob parameter set functions offered by the ConfigServer as library and component
        are successfully tested.
    Success criteria:
        All blob parameters set by the TestApp can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_0 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_0 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_1 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_1 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_2 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_2 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_3 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_set_values_in_config_file_ok(boot_with_proxy):
    """
    Asserts that all parameters of all types written to the config file created in 'test_create_config_file'
    can successfully be set with new values by a TestApp using the more generic parameterSetValue function.
    The TestApp is connected to a ConfigServer component and additionally
    uses the ConfigServer library to test remote and local calls.

    Goal:
        The parameterSetValue() functions offered by the ConfigServer as library and component
        is successfully tested for all parameter types.
    Success criteria:
        All parameters set by the TestApp can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValue_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_32_0 OK',
        'TestParameterSetValue_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_0 OK',
        'TestParameterSetValue_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_64_0 OK',
        'TestParameterSetValue_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_0 OK',
        'TestParameterSetValue_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_String_0 OK',
        'TestParameterSetValue_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_0 OK',
        'TestParameterSetValue_ok: TestApp1 HandleKind:Local Parameter:App1_Parameter_Blob_0 OK',
        'TestParameterSetValue_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_0 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_write_access_rights_from_config_file_ok(boot_with_proxy):
    """
    Asserts that a specific parameter which has been set in the config file with no write access rights
    cannot be set from the TestApp.

    Goal:
        The write access rights management of the config server is successfully tested.
    Success criteria:
        Trying to write to a parameter which has no write rights will return an error.
    """
    result_list = [
        'TestParameterWriteAccessRight_ok: TestApp1 HandleKind:Local Parameter:App2_Parameter_Blob_1 OK',
        'TestParameterWriteAccessRight_ok: TestApp1 HandleKind:Rpc Parameter:App2_Parameter_Blob_1 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)
# Multiclient
#-------------------------------------------------------------------------------
def test_multiclient_get_integer32_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer32 parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by multiple TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.

    Goal:
        The integer32 parameter get functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All integer32 parameters read by the TestApps match the expected written parameters.
    """
    result_list = [
        'TestGetInteger32FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_0 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_32_0 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_32_0 OK',
        'TestGetInteger32FromFsBackend_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_32_0 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)


#-------------------------------------------------------------------------------
def test_multiclient_get_integer64_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer64 parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by multiple TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.

    Goal:
        The integer64 parameter get functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All integer64 parameters read by the TestApps match the expected written parameters.
    """
    result_list = [
        'TestGetInteger64FromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_0 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_64_0 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_64_0 OK',
        'TestGetInteger64FromFsBackend_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_64_0 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_multiclient_get_string_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all string parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by multiple TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.

    Goal:
        The string parameter get functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All string parameters read by the TestApps match the expected written parameters.
    """
    result_list = [
        'TestGetStringsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_0 OK',
        'TestGetStringsFromFsBackend_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_String_0 OK',
        'TestGetStringsFromFsBackend_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_String_0 OK',
        'TestGetStringsFromFsBackend_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_String_0 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_multiclient_get_blob_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all blob parameters written to the config file created in 'test_create_config_file'
    can successfully be read out by multiple TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.
    Different to the tests of the other parameter types, this test checks for two blobs per TestApp.
    This is due to the fact that the second blob is a large blob spanning over several blocks and
    therefore both variants (blob over one block vs several blocks) will be tested.

    Goal:
        The blob parameter get functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All blob parameters read by the TestApps match the expected written parameters.
    """
    result_list = [
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_0 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_3 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_Blob_0 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_Blob_3 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_Blob_0 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_Blob_3 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_Blob_0 OK',
        'TestGetBlobsFromFsBackend_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_Blob_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)


#-------------------------------------------------------------------------------
def test_multiclient_set_integer32_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer32 parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by several TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.

    Goal:
        The integer32 parameter set functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All integer32 parameters set by the TestApps can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsU32_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_32_0 OK',
        'TestParameterSetValueAsU32_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_32_0 OK',
        'TestParameterSetValueAsU32_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_32_0 OK',
        'TestParameterSetValueAsU32_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_32_0 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_multiclient_set_integer64_values_from_config_file_ok(boot_with_proxy):
    """
    Asserts that all integer64 parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by several TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.

    Goal:
        The integer64 parameter set functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All integer64 parameters set by the TestApps can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsU64_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_64_0 OK',
        'TestParameterSetValueAsU64_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_64_0 OK',
        'TestParameterSetValueAsU64_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_64_0 OK',
        'TestParameterSetValueAsU64_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_64_0 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_multiclient_set_string_values_in_config_file_ok(boot_with_proxy):
    """
    Asserts that all string parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by several TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.

    Goal:
        The string parameter set functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All string parameters set by the TestApps can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsString_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_String_0 OK',
        'TestParameterSetValueAsString_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_String_0 OK',
        'TestParameterSetValueAsString_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_String_0 OK',
        'TestParameterSetValueAsString_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_String_0 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)

#-------------------------------------------------------------------------------
def test_multiclient_set_blob_values_in_config_file_ok(boot_with_proxy):
    """
    Asserts that all blob parameters written to the config file created in 'test_create_config_file'
    can successfully be set with new values by several TestApps connected to a ConfigServer component.
    Every TestApp makes use of a unique parameter domain.
    Different to the tests of the other parameter types, this test checks for two blobs per TestApp.
    This is due to the fact that the second blob is a large blob spanning over several blocks and
    therefore both variants (blob over one block vs several blocks) will be tested.

    Goal:
        The blob parameter set functions offered by the ConfigServer are
        successfully tested from several clients, trying to contact the ConfigServer
        simultaneously.
    Success criteria:
        All blob parameters set by the TestApps can in turn be read out successfully.
    """
    result_list = [
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_0 OK',
        'TestParameterSetValueAsBlob_ok: TestApp1 HandleKind:Rpc Parameter:App1_Parameter_Blob_3 OK',
        'TestParameterSetValueAsBlob_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_Blob_0 OK',
        'TestParameterSetValueAsBlob_ok: TestApp2 HandleKind:Rpc Parameter:App2_Parameter_Blob_3 OK',
        'TestParameterSetValueAsBlob_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_Blob_0 OK',
        'TestParameterSetValueAsBlob_ok: TestApp3 HandleKind:Rpc Parameter:App3_Parameter_Blob_3 OK',
        'TestParameterSetValueAsBlob_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_Blob_0 OK',
        'TestParameterSetValueAsBlob_ok: TestApp4 HandleKind:Rpc Parameter:App4_Parameter_Blob_3 OK',
    ]

    run_test_log_match_set(boot_with_proxy,
                           test_system,
                           result_list,
                           timeout)