#
# Copyright (C) 2019-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import pytest

#-------------------------------------------------------------------------------
def test_timer(boot):
    """
    Test timer
    """

    test_runner = boot()

    # synchronize with test application
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            '[ticker] run',
        ],
        5)

    if not ret:
        pytest.fail('could not detect test start')

    # If the timer works, there is one message per second, but it seems on some
    # system the timer setup is broken:
    # * zynq7000/QEMU: the "subjective second" takes 95 seconds in the real
    #                  world.

    (ret, idx) = test_runner.system_log_match_sequence(
        [
            '[ticker] 1 sec tick, jitter',
        ],
        100)

    if not ret:
        pytest.fail('timer test failed')
