#
# Copyright (C) 2019-2023, HENSOLDT Cyber GmbH
#

import pytest
import logs # logs module from the common directory in TA

#-------------------------------------------------------------------------------
def test_hello_world(boot):
    """
    Test a minimal TRENTOS system that has one application saying hello to the
    world
    """

    test_runner = boot('demo_hello_world')

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        test_runner.get_system_log(),
        ['hello world!'],
        15)

    if not ret:
        pytest.fail(f'missing: {expr_fail}')
