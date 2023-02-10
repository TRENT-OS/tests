#
# Copyright (C) 2022-2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_virtio_net(boot):
    """
    Test a VirtIO VM system
    """

    test_runner = boot()
    ret = test_runner.system_log_match(
            ( [
                 'Ping test was successful',
                 'Welcome to Buildroot'
              ], 60 )
          )
    if not ret.ok:
        pytest.fail(f'missing string: {ret.get_missing()}')
