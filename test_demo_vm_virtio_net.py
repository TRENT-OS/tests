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
            [
                ( 'Starting ping echo component', 2 ),
                ( 'Testing ping on virtual interface', 10 ),
                ( '5 packets transmitted, 5 packets received, 0% packet loss', 10 ),
                ( 'Ping test was successful', 1 ),
                ( 'Welcome to Buildroot', 5 ),
            ]
          )
    if not ret.ok:
        pytest.fail(f'missing string: {ret.get_missing()}')
