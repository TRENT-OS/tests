#
# Copyright (C) 2019-2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_hello_world(boot):
    """
    Test a minimal TRENTOS system that has one application saying hello to the
    world
    """

    test_runner = boot('demo_hello_world')

    ret = test_runner.system_log_match( ('hello world!', 15) )
    if not ret.ok:
        pytest.fail(f'missing: {ret.get_missing()}')
