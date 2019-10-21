import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "test_image, expected_output_array, timeout", [(
    "build-zynq7000-Debug-DEMO_PREPROVISIONED_KEYSTORE/images/capdl-loader-image-arm-zynq7000",
    [
        "Preprovisioning keystore demo succeeded"
    ],
    200
)])
def test_key_store_provisioning(boot_with_proxy, test_image, expected_output_array, timeout):

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

    test_run = boot_with_proxy(test_image)
    f_out = test_run[1]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        print(text)
        assert match == success_msg
