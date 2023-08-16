#
# Copyright (C) 2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_drone_sim(boot_with_proxy):
    """
    Test demo_vm_drone_sim.
    For test setup of refer to demo README.
    """

    test_runner = boot_with_proxy()
    ret = test_runner.system_log_match(
            ( [
                 'MAVLink: info: Disarmed by landing'
              ], 400 )
          )
    if not ret.ok:
        pytest.fail(f'missing string: {ret.get_missing()}')
