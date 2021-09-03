#-------------------------------------------------------------------------------
#
# Test Core
#
# Copyright (C) 2019-2020, Hensoldt Cyber GmbH
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
def get_log_dir(request):
    log_dir = pathlib.Path(request.node.name).stem
    log_dir_str = request.config.option.log_dir
    if (log_dir_str is not None):
        log_dir = os.path.join(log_dir_str, log_dir)

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
    additional_qemu_params = None,
    boot_mode = ba.BootMode.BARE_METAL):

    # setup phase
    print("")

    log_dir = get_log_dir(request)
    resource_dir = request.config.option.resource_dir
    platform = request.config.option.target
    system_image = request.config.option.system_image
    proxy_config = request.config.option.proxy if use_proxy else None
    sd_card_size  = int(request.config.option.sd_card) \
                        if request.config.option.sd_card else 0
    print_logs = request.config.option.print_logs

    is_error = False
    test_runner = None

    try:
        test_runner = board_automation.system_selector.get_test_runner(
                        log_dir,
                        resource_dir,
                        platform,
                        system_image,
                        proxy_config,
                        sd_card_size,
                        additional_qemu_params,
                        print_logs
                    )

        test_runner.start()

        test_runner.check_start_success(boot_mode)

        # pytest will receive the tupel from this "callback" for each test
        # case. The "system" parameter that the test passes in the call is
        # no longer used, since the system image is passed as parameter
        # when the whole test framework is started.
        yield (lambda system = None: (
                            test_runner,
                            test_runner.get_system_log() # kept for legacy compatibility
                        ) )

    except: # catch really *all* exceptions
        exc_info = sys.exc_info()
        msg = exc_info[1]
        print('test_runner exception: {}'.format(msg))
        traceback.print_exception(*exc_info)
        is_error = True

    if test_runner:
        try:
            test_runner.stop()
        except: # catch really *all* exceptions
            exc_info = sys.exc_info()
            msg = exc_info[1]
            print('test_runner.stop() exception: {}'.format(msg))
            traceback.print_exception(*exc_info)
            pytest.exit('test_runner.stop() failed')

    if is_error:
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

        print("[TLS] Started TLS server on port %i" % port)

        while True:
            conn, addr = sock.accept()
            print("[TLS] Client connected:", addr)

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

