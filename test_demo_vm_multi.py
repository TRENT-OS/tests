#
# Copyright (C) 2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_multi(boot):
    """
    Test a VM system with multiple VMs and a serial server
    """

    test_runner = boot()
    ret = test_runner.system_log_match( ('Welcome to Buildroot', 60) )
    if not ret.ok:
        pytest.fail(f'missing: {ret.get_missing()}')
