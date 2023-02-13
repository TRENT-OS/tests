#
# Copyright (C) 2019-2023, HENSOLDT Cyber GmbH
#

import pytest
import logs # logs module from the common directory in TA


#-------------------------------------------------------------------------------
def test_keystore_demo(boot_with_proxy):
    test_runner = boot_with_proxy('demo_keystore')

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        test_runner.get_system_log(),
        [
            'Demo with local crypto succeeded!',
            'Demo with remote crypto succeeded!'
        ],
        100)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
