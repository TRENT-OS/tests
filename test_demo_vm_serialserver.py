#
# Copyright (C) 2022-2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_serialserver(boot):
    """
    Test a VM system with the serial server
    """

    test_runner = boot()
    ret = test_runner.system_log_match( ('Welcome to Buildroot', 60) )
    if not ret.ok:
        pytest.fail(f'missing: {ret.get_missing()}')
