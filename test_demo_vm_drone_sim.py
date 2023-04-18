#
# Copyright (C) 2022-2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_drone_sim(boot_with_proxy):
    """
    Test a VirtIO VM system
    """

    test_runner = boot_with_proxy()
    ret = test_runner.system_log_match(
            ( [
                 'Ping test was successful',
                 '!Welcome to Buildroot'
              ], 6000 )
          )
    if not ret.ok:
        pytest.fail(f'missing string: {ret.get_missing()}')
