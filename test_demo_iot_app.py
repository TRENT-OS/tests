import sys, os, re, time
import pytest
sys.path.append('../common')
import logs

test_system = "demo_iot_app"

# Timeouts of the tests are set based on CI profiling.

#-------------------------------------------------------------------------------
@pytest.mark.dependency()
def test_config_backend_init_ok(boot_with_proxy):
    """
    Test that the configuration backend is successfully initialized by the
    Config Server component.
    """

    # Assert that a provisioned image was placed in the test workspace,
    # otherwise it makes no sense to run the test
    assert(os.path.isfile("nvm_06"))

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["Config Server initialized"],
        60)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_config_backend_init_ok"])
def test_server_connect_ok(boot_with_proxy, mosquitto_broker):
    """
    Test that the TCP connection with the configured server is successfully established.
    """

    test_run = boot_with_proxy(test_system)
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
        f_out,
        ["TCP connection established successfully"],
        180)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))


#-------------------------------------------------------------------------------
@pytest.mark.dependency(depends=["test_config_backend_init_ok",
                                 "test_server_connect_ok"])
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