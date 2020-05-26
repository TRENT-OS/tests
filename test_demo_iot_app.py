import sys, os, re, time
import pytest
sys.path.append('../common')
import logs

test_system = "demo_iot_app"

# Timeout set to 6 min for the tests that utilize the filesystem heavily.
# Other tests have specific timeouts based on profiling.
timeout = 360

#-------------------------------------------------------------------------------
@pytest.mark.dependency()
def test_capdl_loader_ok(boot_with_proxy):
    """
    Test that the CapDL Loader suspends itself after it has successfully set
    the IoT demo system up
    """
    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Done; suspending..."],
        15)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_capdl_loader_ok"])
def test_create_config_backend_ok(boot_with_proxy):
    """
    Test that the configuration backend is successfully initialized by the
    Config Server component.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Config Server initialized"],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_create_config_backend_ok"])
def test_set_system_config_ok(boot_with_proxy):
    """
    Test that the system settings are successfully written to the configuration
    backend by the Admin component utilizing the Config Server component.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["System configuration set"],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_set_system_config_ok",
                                 "test_create_config_backend_ok"])
def test_connect_to_server_ok(boot_with_proxy, mosquitto_broker):
    """
    Test that the TCP connection with the configured server is successfully established.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["incoming connection established"],
        timeout)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_set_system_config_ok",
                                 "test_create_config_backend_ok",
                                 "test_connect_to_server_ok"])
def test_tls_handshake_ok(boot_with_proxy, mosquitto_broker):
    """
    Test that the TLS Handshake is successfully completed.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["handshake wrapup"],
        60)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_tls_handshake_ok"])
def test_mqtt_connect_ok(boot_with_proxy, mosquitto_broker):
    """
    Test that the MQTT connect step is successfully acknowledged by the broker.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["CloudConnector initialized"],
        60)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_mqtt_connect_ok"])
def test_mqtt_publish_ok(boot_with_proxy, mosquitto_broker):
    """
    Test that the MQTT message is successfully published to the broker.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["MQTT publish on WAN successful"],
        60)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))