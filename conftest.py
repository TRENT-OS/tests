#-------------------------------------------------------------------------------
#
# Test Core
#
# Copyright (C) 2019-2020, HENSOLDT Cyber GmbH
#
#-------------------------------------------------------------------------------

import sys, os, subprocess, multiprocessing
import traceback
import time, datetime
import socket, ssl
import re

import pytest

import logs # logs module from the common directory in TA

import board_automation.system_selector
import board_automation.board_automation as ba


#-------------------------------------------------------------------------------
# pytest invokes this as iterator. Everything up to the yield is executed only
# once when the iterator is created. Then this "yields" the handle tuple for
# each iteration. When the iterator is destroyed, the code after the yield runs
# to clean things up.
def start_or_attach_to_test_runner(run_context):

    # setup phase
    print("")

    base_log_dir = run_context.log_dir

    for retries in range(4):

        if (retries > 0):
            sleep_time = 2**retries
            print(f'Succesful start not detected. Retrying after {sleep_time} seconds')
            time.sleep(sleep_time)

        log_dir = base_log_dir
        if (retries > 0):
            log_dir += f'-retry-{retries}'
        # ensure the log dir exists
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        run_context.log_dir = log_dir

        test_runner = None
        do_retry = True
        is_error = False

        try:
            # Create the test runner and start the board. If this fails, then
            # keep retrying, as this can happen sometimes, e.g. with QEMU where
            # the system still has some resources locked.
            test_runner = board_automation.system_selector.get_test_runner(run_context)
            test_runner.start()
            # We could start the test system, so there is no point in retrying
            # if the test fails.
            do_retry = False
            # PyTest will receive the test runner from this "callback" for each
            # test case. The "system" parameter that the test can pass in the
            # call is no longer used, since the system image is passed as
            # parameter when the whole test framework is started.
            yield (lambda system = None: test_runner)
            # If we arrive here, the test runner finished normally. This does
            # not mean the test(s) passed successfully, it just means there was
            # no fatal problem.
        except Exception as e:
            is_error = True
            print(f'Test_runner exception: {e}')
            print(''.join(traceback.format_exception(
                etype=type(e),
                value=e,
                tb=e.__traceback__)))

        if test_runner:
            try:
                test_runner.stop()
            except Exception as e:
                # failing to stop the test runner is really fatal, there is no
                # point in retrying then.
                do_retry = False
                is_error = True
                print(f'Test_runner stop exception: {e}')
                print(''.join(traceback.format_exception(
                    etype=type(e),
                    value=e,
                    tb=e.__traceback__)))

        if not is_error:
            break

        if not do_retry:
            pytest.exit('test_runner failed')

    # We arrive here after the loop, the test runner finished normally. This
    # does not mean the test(s) passed successfully, it just means there was no
    # fatal problem.
    print('test_runner finished' + \
          ('' if (0 == retries) else f' (after {retries} retries)') )


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
def start_or_attach_to_mosquitto(run_context):

    mosquitto_log_file = os.path.join(run_context.log_dir, "mosquitto_log.txt")
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
                    ba.Run_Context(
                        request,
                        boot_mode = ba.BootMode.SEL4_CAMKES,
                    )
               )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(request):
    yield from start_or_attach_to_test_runner(
                    ba.Run_Context(
                        request,
                        boot_mode = ba.BootMode.SEL4_CAMKES,
                        use_proxy = True,
                    )
               )

#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy_no_sdcard(request):
    yield from start_or_attach_to_test_runner(
                    ba.Run_Context(
                        request,
                        boot_mode = ba.BootMode.SEL4_CAMKES,
                        use_proxy = True,
                        sd_card_size = 0,
                    )
               )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_sel4_native(request):
    yield from start_or_attach_to_test_runner(
                    ba.Run_Context(
                        request,
                        boot_mode = ba.BootMode.SEL4_NATIVE,
                    )
               )


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_bare_metal(request):
    yield from start_or_attach_to_test_runner(
                    ba.Run_Context(
                        request,
                        boot_mode = ba.BootMode.BARE_METAL,
                    )
               )


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
    start_or_attach_to_mosquitto(ba.Run_Context(request))


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

    # Optional parameter in case multiple boards exist
    parser.addoption(
        "--instance",
        type="int", default=1,
        help="select instance in case multiple board are available."
    )

