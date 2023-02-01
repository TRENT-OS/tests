#-------------------------------------------------------------------------------
#
# Test Core
#
# Copyright (C) 2019-2020, HENSOLDT Cyber GmbH
#
#-------------------------------------------------------------------------------

import sys, os, pathlib, subprocess, multiprocessing
import traceback
import time, datetime
import socket, ssl
import re

import pytest

import logs # logs module from the common directory in TA

import board_automation.system_selector
import board_automation.board_automation as ba

#-------------------------------------------------------------------------------
def get_log_dir(request, retries=0):
    log_dir = pathlib.Path(request.node.name).stem
    log_dir_str = request.config.option.log_dir
    if (log_dir_str is not None):
        log_dir = os.path.join(log_dir_str, log_dir)

    if (retries > 0):
        log_dir += f'-retry-{retries}'

    # if the log dir does not exist yet, go ahead and create one
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    return log_dir


#-------------------------------------------------------------------------------
# pytest invokes this as iterator. Everything up to the yield is executed only
# once when the iterator is created. Then this "yields" the handle tuple for
# each iteration. When the iterator is destroyed, the code after the yield runs
# to clean things up.
def start_or_attach_to_test_runner(
    request,
    use_proxy = False,
    additional_params = None,
    boot_mode = ba.BootMode.BARE_METAL):

    # setup phase
    print("")

    resource_dir = request.config.option.resource_dir
    platform = request.config.option.target
    system_image = request.config.option.system_image
    proxy_config = request.config.option.proxy if use_proxy else None
    sd_card_size  = int(request.config.option.sd_card) \
                        if request.config.option.sd_card else 0
    print_logs = request.config.option.print_logs

    for retries in range(4):

        if (retries > 0):
            sleep_time = 2**retries
            print(f'Succesful start not detected. Retrying after {sleep_time} seconds')
            time.sleep(sleep_time)

        log_dir = get_log_dir(request, retries)
        do_retry = True
        is_error = False

        try:
            test_runner = board_automation.system_selector.get_test_runner(
                            log_dir,
                            resource_dir,
                            platform,
                            system_image,
                            proxy_config,
                            sd_card_size,
                            additional_params,
                            print_logs
                        )

            try:
                test_runner.start()
                # Check if starting worked. If not, then keep retrying, as this
                # can happen sometimes, e.g. with QEMU where the system still
                # has some resources locked. Actually, it's a bit annoying that
                # this check throws an exception instead of just returning an
                # error.
                test_runner.check_start_success(boot_mode)
                # We could start the test system, so there is no point in
                # retrying if the test fails.
                do_retry = False
                # PyTest will receive the test runner from this "callback" for
                # each test case. The "system" parameter that the test can pass
                # in the call is no longer used, since the system image is
                # passed as parameter when the whole test framework is started.
                yield (lambda system = None: test_runner )
                # If we arrive here, the test runner finished normally. This
                # does no mean the test(s) passed successfully, it just means
                # there was no fatal problem.
            finally:
                try:
                    test_runner.stop()
                except Exception as e:
                    # failing to stop the test runner is really fatal, there is
                    # no point in retrying then.
                    do_retry = False
                    is_error = True
                    print(f'Test_runner stop exception: {e}')
                    print(''.join(traceback.format_exception(
                        etype=type(e),
                        value=e,
                        tb=e.__traceback__)))

        except Exception as e:
            is_error = True
            print(f'Test_runner exception: {e}')
            print(''.join(traceback.format_exception(
                etype=type(e),
                value=e,
                tb=e.__traceback__)))

        if not is_error:
            status_msg = 'test_runner finished'
            if (retries > 0):
                status_msg += f' (after {retries} retries)'
            print(status_msg)
            return

        if not do_retry:
            break

    # if we arrive here the test run failed
    pytest.exit('test_runner failed')


#-------------------------------------------------------------------------------
def tls_server_proc(port = 8888, timeout = 180):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(
            certfile=os.path.dirname(__file__) + "/test_tls_api/cert.pem",
            keyfile=os.path.dirname(__file__) + "/test_tls_api/key.pem"
        )

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow re-use of socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Set *some* timeout
        sock.settimeout(timeout)

        # Allow any IP
        sock.bind(('', port))
        # Expect one client
        sock.listen(1)

        print(f'[TLS] Started TLS server on port {port}')

        while True:
            conn, addr = sock.accept()
            print(f'[TLS] Client connected: {addr}')

            stream = context.wrap_socket(conn, server_side=True)
            try:
                # Simply echo back to sender, receiving blocks of up to 1 KiB
                # is sufficient for the current test implementation
                data = stream.recv(1024)
                print("[TLS] Received data", data)
                stream.send(data)
                print("[TLS] Sent data back")
            except ssl.SSLEOFError:
                # This happens during the test of the re-set, where we do a handshake
                # and then simply close the socket..
                pass
            finally:
                stream.shutdown(socket.SHUT_RDWR)
                stream.close()
    finally:
        sock.close()


#-------------------------------------------------------------------------------
def start_or_attach_to_mosquitto(request):
    log_dir = get_log_dir(request)

    mosquitto_log_file = os.path.join(log_dir, "mosquitto_log.txt")

    with open(mosquitto_log_file, "w") as f:
        try:
            subprocess.Popen(
                ['mosquitto', '-c', '/etc/mosquitto/mosquitto.conf'],
                stderr=f,
                stdout=f)
        except OSError:
            # no need to run the tests without the broker
            pytest.fail("Couldn't run mosquitto broker!")


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot(request):
    yield from start_or_attach_to_test_runner(
                request,
                boot_mode = ba.BootMode.SEL4_CAMKES )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(request):
    yield from start_or_attach_to_test_runner(
                request,
                use_proxy = True,
                boot_mode = ba.BootMode.SEL4_CAMKES )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy_no_sdcard(request):
    request.config.option.sd_card = 0
    yield from start_or_attach_to_test_runner(
                request,
                use_proxy = True,
                boot_mode = ba.BootMode.SEL4_CAMKES )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_sel4_native(request):
    yield from start_or_attach_to_test_runner(
                request,
                use_proxy = False,
                boot_mode = ba.BootMode.SEL4_NATIVE )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_bare_metal(request):
    yield from start_or_attach_to_test_runner(
                request,
                use_proxy = False,
                boot_mode = ba.BootMode.BARE_METAL )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def tls_server():
    proc = multiprocessing.Process(target=tls_server_proc)
    proc.start()
    yield proc
    proc.terminate()


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def mosquitto_broker(request):
    start_or_attach_to_mosquitto(request)


#-------------------------------------------------------------------------------
def pytest_addoption(parser):

    # test image
    parser.addoption(
        "--system_image",
        required=True,
        help="location of the system image")

    # proxy is an optional parameter, because some tests don't need it
    parser.addoption(
        "--proxy",
        help="<binary_location>[,<connection>]")

    # Optional parameter as only some tests need the SD Card.
    parser.addoption(
        "--sd_card",
        default="1048576", # 1 MiB
        help="SD card shall be available."
    )

    parser.addoption(
        "--target",
        required=True,
        help="target platform")

    parser.addoption(
        "--log_dir",
        help="folder where to put the logs")

    parser.addoption(
        "--resource_dir",
        help="folder where the platform resources are located")

    parser.addoption(
        "--print_logs",
        action="store_true",
        help="print logs to console")

