#
# Copyright (C) 2019-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import pytest

# Timeouts of the tests are set based on CI profiling.

#-------------------------------------------------------------------------------
@pytest.mark.dependency()
def test_demo_tls_api(boot_with_proxy):
    """
    The success of this demo depends on internet access from the CI network,
    thus we consider both a success and a connection failure as acceptable.
    """

    test_runner = boot_with_proxy()

    (ret, idx) = test_runner.system_log_match_sequence(
                    ["Demo completed successfully"],
                    90)

    if not ret:
        # accept a connection failure also, seems CI can't access the internet.
        (ret, idx) = test_runner.system_log_match_sequence(
                        ["PICO_SOCK_EV_ERR, OS error = -1303 (OS_ERROR_NETWORK_CONN_REFUSED)"],
                        5)

        if not ret:
            pytest.fail("Expected demo success or connection error")
