#
# Copyright (C) 2019-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import os
import pytest
import logs # logs module from the common directory in TA

test_system = "demo_preprovisioned_keystore"
timeout = 200

#-------------------------------------------------------------------------------
def test_key_store_provisioning(boot_with_proxy):

    pre_provisioned_keystore_image = "preProvisionedKeyStoreImg"
    proxy_memory_file = "nvm_06"

    print("pre-preovisioned keystore image: "+pre_provisioned_keystore_image)
    if not os.path.isfile(pre_provisioned_keystore_image):
        print("ERROR: Could not find the pre-preovisioned keystore image!")
        assert False

    # Proxy expect NVM images to be named by index
    if os.path.isfile(proxy_memory_file):
        os.remove(proxy_memory_file)
    os.rename(pre_provisioned_keystore_image, proxy_memory_file)

    test_runner = boot_with_proxy(test_system)

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        test_runner.get_system_log(),
        [
            "Preprovisioning keystore demo succeeded"
        ],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
