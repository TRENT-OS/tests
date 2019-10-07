import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time

test_imagepath = '/build-zynq7000-Debug-PRE_PROVISIONED_KEYSTORE/images/capdl-loader-image-arm-zynq7000'
timeout = 60

@pytest.mark.parametrize("img, expected_output_array, timeout", [
    (test_imagepath,
    [
        'Preprovisioning keystore demo succeeded'
    ],
    timeout),
])

def test_key_store_provisioning(boot_with_proxy, img, expected_output_array, timeout):
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

    f_out = boot_with_proxy(image_subpath=img)[1]

    for index in range(0, len(expected_output_array)):
        success = expected_output_array[index]
        (text, match) = logs.get_match_in_line(f_out, re.compile(success), timeout)
        print(text)
        assert match == success
