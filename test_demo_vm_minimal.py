#
# Copyright (C) 2022-2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_minimal(boot):
    """
    Test a minimal TRENTOS VM system
    """

    test_runner = boot()
    ret = test_runner.system_log_match( ( 'Welcome to Buildroot', 60 ) )
    if not ret.ok:
        pytest.fail(f'missing: {ret.get_missing()}')
