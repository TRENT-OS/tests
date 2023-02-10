#
# Copyright (C) 2019-2023, HENSOLDT Cyber GmbH
#

import pytest


#-------------------------------------------------------------------------------
def test_keystore_demo(boot_with_proxy):
    test_runner = boot_with_proxy('demo_keystore')

    ret = test_runner.system_log_match(
            ([
                'Demo with local crypto succeeded!',
                'Demo with remote crypto succeeded!'
             ], 30)
          )

    if not ret.ok:
        pytest.fail(f'missing: {ret.get_missing()}')
