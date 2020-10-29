# Copyright (C) 2020, HENSOLDT Cyber GmbH
import pytest, sys, tests
from collections import namedtuple

# we place here 10 sec and not less because at the moment (26/6/2020) we do
# no have yet synchronization mechanism with the boot complete
TEST_TIMEOUT = 10

testers = [
'tester_sdhc'
]

"""
White list of platforms supported by the given tester. If the tester is not in
this list, then it supports all platforms.
"""
test_white_list = {'tester_sdhc': ['sabre', 'sabre-hw'] }

#-------------------------------------------------------------------------------
@pytest.fixture(scope="module", params=testers)
def context_no_sdcard(boot_with_proxy_no_sdcard, request):
    tester = request.param
    platform = request.config.option.target

    if (tester in test_white_list and platform not in test_white_list[tester]):
        pytest.skip(tester + " not supported on the platform " + platform)

    TestData = namedtuple('TestData', ['parent_fixture', 'tester'])
    return TestData(boot_with_proxy_no_sdcard, tester)

def test_storage_noSDcardInserted_sdhc(context_no_sdcard):
    """
    Checking if the API is returning the correct error code
    (OS_ERROR_DEVICE_NOT_PRESENT) when media is not present
    """
    result_list = [
        context_no_sdcard.tester + " -> !!! test_storage_apiWithMediumNotPresent: OK",
        context_no_sdcard.tester + " -> !!! All tests successfully completed.",
    ]
    tests.run_test_log_match_sequence(
        context_no_sdcard.parent_fixture,
        None,
        result_list,
        TEST_TIMEOUT)
