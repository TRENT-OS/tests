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
    mqtt_proxy_memory_file='nvm_06'
    pre_provisioned_keystore_image='preProvisionedKeyStoreImg'

    #remove the existing mqtt_proxy_demo memory file
    if os.path.isfile(mqtt_proxy_memory_file):
        os.remove(mqtt_proxy_memory_file)

    #place the prepared keystore image in its place
    if os.path.isfile(pre_provisioned_keystore_image):
        os.rename(pre_provisioned_keystore_image, mqtt_proxy_memory_file)
    else:
        print("ERROR: Could not find the pre-preovisioned keystore image!")
        assert os.path.isfile(pre_provisioned_keystore_image)

    test_run = boot_with_proxy(test_image)
    f_out = test_run[1]

    for success_msg in expected_output_array:
        (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
        print(text)
        assert match == success_msg
