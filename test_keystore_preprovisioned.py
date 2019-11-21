import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

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

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    expected_output_array = [
        "Preprovisioning keystore demo succeeded",
    ]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        assert match == success_msg