#
# Copyright (C) 2021-2023, HENSOLDT Cyber GmbH
#

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
        # and eventually, all test have passed
        ('All is well in the universe', 180)
    ])
    if not ret.ok:
        raise Exception(f'sel4test failed, missing: {ret.get_missing()}')
