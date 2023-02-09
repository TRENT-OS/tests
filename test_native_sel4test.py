#
# Copyright (C) 2021-2023, HENSOLDT Cyber GmbH
#

import re
import pytest

#-------------------------------------------------------------------------------
def test_run_native_sel4test(boot_sel4_native):
    """
    run native sel4test
    """

    test_runner = boot_sel4_native()
    log = test_runner.get_system_log_line_reader()

    ret = log.find_matches_in_lines([
        # the sel4test system prints the untypeds when it starts
        ('List of untypeds', 1),
        # the sel4test application starts
        ('seL4 Test', 1),
        # and it will start running tests
        # the delay is relatively high (increased from to 2 to 15 seconds) due
        # to a slower boot process on the zynqmp, and can be potentially
        # reverted if the said boot process improves
        ('Starting test suite sel4test', 15),
        ('Starting test 0: Test that there are tests', 1),
    ])
    if not ret.ok:
        raise Exception(f'sel4test failed, missing: {ret.get_missing()}')

    # If we are here, the tests are running. Check for failure or passing,
    STR_OK = 'All is well in the universe'
    STR_FAIL = '*** FAILURES DETECTED ***'
    REGEX_END = '|'.join( [ re.escape(s) for s in [STR_OK, STR_FAIL] ] )
    ret = log.find_matches_in_lines( (re.compile(REGEX_END), 180) )
    if not ret.ok:
        raise Exception(f'sel4test did not finish properly: {ret.get_missing()}')

    match_str = ret.match
    if match_str == STR_OK:
        return

    if match_str != STR_FAIL:
        pytest.fail(f'sel4test result unknown: {match_str}')

    # ToDo: we should also capture all "Test xxx failed" from the lists and
    #       print them, so it's easier to see what tests have failed.
    #       REGEX_TEST_FAILED = 'Test\ .* \failed'

    pytest.fail(f'sel4test did no pass completely')
