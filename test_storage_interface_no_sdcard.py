#
# Copyright (C) 2020-2023, HENSOLDT Cyber GmbH
#

import pytest

#-------------------------------------------------------------------------------
# Tester and list of platforms supported by it. If the list is None,,then the
# tester supports all platforms.
TESTERS = {
    'tester_sdhc': ['sabre', 'sabre-hw']
}


#-------------------------------------------------------------------------------
class StorageTestRunner():

    #---------------------------------------------------------------------------
    def __init__(self, fixture, tester):
        self.fixture = fixture
        self.tester = tester

    #---------------------------------------------------------------------------
    def run_test(self, string, timeout_sec = 10):
        test_runner = self.fixture()
        match_obj = (f'{self.tester} -> !!! {string}', timeout_sec)
        ret = test_runner.system_log_match(match_obj)
        if not ret.ok:
            pytest.fail(f'missing: {ret.get_missing()}')


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module", params=list(TESTERS.keys()))
def context(boot_with_proxy_no_sdcard, request):
    tester = request.param
    platform = request.config.option.target

    if not tester in TESTERS:
        pytest.fail(f'unknown tester: {tester}')

    plat_list = TESTERS.get(tester)
    if (plat_list is not None) and (platform not in plat_list):
        pytest.skip(f'{tester} not supported on the platform {platform}')

    return StorageTestRunner(boot_with_proxy_no_sdcard, tester)



#-------------------------------------------------------------------------------
def test_storage_noSDcardInserted(context):
    """
    Checking if the API is returning the correct error code
    (OS_ERROR_DEVICE_NOT_PRESENT) when media is not present
    """
    context.run_test('test_storage_apiWithMediumNotPresent: OK')

#-------------------------------------------------------------------------------
def test_storage_complete(context):
    """
    Checking if all tests has been completed and that there was no
    failure/exception during the tear down phase.
    """
    context.run_test('All tests successfully completed.')
