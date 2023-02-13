#
# Copyright (C) 2019-2023, HENSOLDT Cyber GmbH
#

import os
import pytest
import logs # logs module from the common directory in TA


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

    test_runner = boot_with_proxy('demo_preprovisioned_keystore')

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        test_runner.get_system_log(),
        [
            'Preprovisioning keystore demo succeeded'
        ],
        200)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
