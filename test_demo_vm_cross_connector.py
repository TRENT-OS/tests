#
# Copyright (C) 2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_cross_connector(boot):
    """
    Test a VM system with a cross connector
    """

    test_runner = boot()
    ret = test_runner.system_log_match( ('Welcome to Buildroot', 60) )
    if not ret.ok:
        pytest.fail(f'missing: {ret.get_missing()}')
