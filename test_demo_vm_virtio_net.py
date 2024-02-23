#
# Copyright (C) 2022-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import pytest


#-------------------------------------------------------------------------------
def test_demo_vm_virtio_net(boot):
    """
    Test a VirtIO VM system
    """

    test_runner = boot()
    (ret, idx, idx2) = test_runner.system_log_match_multiple_sequences([
        ( [
            'Ping test was successful',
            'Welcome to Buildroot'
          ], 60 )
    ])
    if not ret:
        pytest.fail('string #{}.{} not found'.format(idx, idx2))
