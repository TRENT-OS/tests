#
# Copyright (C) 2019-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import pytest
import logs # logs module from the common directory in TA

def test_hello_world(boot_sel4_native):
    """
    Test a minimal TRENTOS system that has one application saying hello to the
    world
    """

    test_runner = boot_sel4_native()

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        test_runner.get_system_log(),
        ["Hello, world!"],
        15)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
