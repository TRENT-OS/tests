#-------------------------------------------------------------------------------
#
# Test Core
#
# Copyright (C) 2019-2020, Hensoldt Cyber GmbH
#
#-------------------------------------------------------------------------------

import sys, os, pathlib, subprocess, multiprocessing
import time, datetime
import socket, ssl
import re

import pytest

import logs # logs module from the common directory in TA


#-------------------------------------------------------------------------------
def get_pid_from_pid_file(
    pid_file
):
    if not os.path.exists(pid_file):
        return None

    with open(pid_file,"r") as f:
        return int(f.read())


#-------------------------------------------------------------------------------
def start_process_and_create_pid_file(
    cmd_line,
    pid_file
):
    print(cmd_line)
    os.system(cmd_line + " & echo $! > " + pid_file)


#-------------------------------------------------------------------------------
def terminate_process_by_pid_file(
    pid_file
):
    if not os.path.isfile(pid_file):
        print("missing PID file: " + pid_file);
        return

    old_pid_file = pid_file+"-terminated"
    if os.path.exists(old_pid_file):
        os.remove(old_pid_file)
    os.rename(pid_file, old_pid_file)
    os.system("kill $(cat "+old_pid_file+")")


#-------------------------------------------------------------------------------
def get_qemu_serial_connection_params(mode):

    if(mode == "PTY"):

        # must use "-S" to freeze the QEMU at startup, unfreezing when the
        # other end of PTY is connected
        return ["-S", "-serial pty"]

    elif (mode == "TCP"):

        # QEMU will freeze on startup until it can connect to the server
        return ["-serial tcp:localhost:4444,server"]

    else:

        return ["-serial /dev/null"]


#-------------------------------------------------------------------------------
def get_qemu_cmd(
    platform,
    system_image,
    serial_qemu_connection,
    test_system_out_file
):

    qemu_mapping = {
        # <plat>: ["<qemu-binary-arch>", "<qemu-machine>"],

        "imx6":      ["arm",     "sabrelite"],
        "migv":      ["riscv64", "virt"],
        "rpi3":      ["aarch64", "raspi3"],
        "spike":     ["riscv64", "spike_v1.10"],
        "zynq7000":  ["arm",     "xilinx-zynq-a9"],
    }.get(platform, None)
    assert(qemu_mapping is not None)

    return [ "qemu-system-" + qemu_mapping[0],
             "-machine " + qemu_mapping[1],
             "-m size=1024M",
             "-nographic",
           ] + get_qemu_serial_connection_params(serial_qemu_connection) + [
             "-serial file:" + test_system_out_file,
             "-kernel " + system_image,
           ]


#-------------------------------------------------------------------------------
def start_or_attach_to_qemu_and_proxy(
    request,
    system,
    test_system_out_file,
    qemu_stdin_file,
    qemu_stdout_file,
    qemu_stderr_file,
    qemu_pid_file,
    use_proxy = False,
    proxy_stdout_file = None,
    proxy_pid_file = None,
):
    qemu_already_running = os.path.isfile(qemu_pid_file)

    serial_qemu_connection = None
    proxy_app = None

    if use_proxy:
        proxy_cfg_str = request.config.option.proxy
        assert(proxy_cfg_str is not None)
        arr = proxy_cfg_str.split(",")
        proxy_app = arr[0]
        serial_qemu_connection = "TCP" if (1 == len(arr)) else arr[1]

    f_qemu_stdin = None

    print("")

    if qemu_already_running:
        qemu_pid = get_pid_from_pid_file(qemu_pid_file)
        print("QEMU already running (PID %u)"%(qemu_pid))

    else:
        print("  test system output: " + test_system_out_file)
        print("  QEMU stdin:         " + qemu_stdin_file)
        print("  QEMU stdout:        " + qemu_stdout_file)
        print("  QEMU stderr:        " + qemu_stderr_file)

        system_image = request.config.option.system_image
        assert(system_image is not None)
        print("launching QEMU with system image " + system_image)
        assert(os.path.isfile(system_image))

        qemu_cmd = " ".join(
                    get_qemu_cmd(
                        request.config.option.target,
                        system_image,
                        serial_qemu_connection,
                        test_system_out_file) +
                        [
                            "2>" + qemu_stderr_file,
                            ">" + qemu_stdout_file,
                            "<" + qemu_stdin_file
                        ])

        start_process_and_create_pid_file(qemu_cmd, qemu_pid_file)

        # seems QEMU tries to read from strdin, so we have to open the pipe now
        # to unblock it
        f_qemu_stdin = open(qemu_stdin_file, "w", buffering=1)

        qemu_pid = get_pid_from_pid_file(qemu_pid_file)
        print("QEMU starting (PID %u) ..."%(qemu_pid))
        # give QEMU some time to start
        time.sleep(1)

    f_qemu_stderr = logs.open_file_non_blocking(qemu_stderr_file, "r")
    f_qemu_stdout = logs.open_file_non_blocking(qemu_stdout_file, "r")

    if use_proxy:
        if os.path.isfile(proxy_pid_file):
            proxy_pid = get_pid_from_pid_file(proxy_pid_file)
            print("Proxy already running (PID %u)"%(proxy_pid))
        elif qemu_already_running:
            # Proxy can't be running when we've just started QEMU, as they can
            # only be started togehter
            print("ERROR: can't start proxy if QEMU is already running")
            assert False
        else:

            print("Start proxy: " + proxy_app)
            assert(os.path.isfile(proxy_app))
            print("  proxy stdout:       " + proxy_stdout_file)

            connection_mode = None

            if(serial_qemu_connection == "PTY"):
                # search for dev/ptsX info in QEMU stderr
                # in QEMU >= 4.2 we need to look in stdout
                (text, match) = logs.get_match_in_line(
                                    f_qemu_stderr,
                                    re.compile('(\/dev\/pts\/\d)'),
                                    10)
                # if there was no match in stderr we have to look in stdout
                if match is None:
                    (text, match) = logs.get_match_in_line(
                                        f_qemu_stdout,
                                        re.compile('(\/dev\/pts\/\d)'),
                                        10)
                assert(match)

                connection_mode = "PTY:" + match # PTY to connect to
            elif(serial_qemu_connection == "TCP"):
                connection_mode = "TCP:4444"
            else:
                print("ERROR: invalid Proxy/QEMU_connection %s", serial_qemu_connection)
                # ToDo: return an error or throw exception
                assert False

            # start the proxy
            proxy_cmd = (proxy_app + \
                        " -c " + connection_mode +
                        " -t 1" # enable TAP
                        " > " + proxy_stdout_file)

            start_process_and_create_pid_file(proxy_cmd, proxy_pid_file)

            proxy_pid = get_pid_from_pid_file(proxy_pid_file)
            print("Proxy starting (PID %u) ..."%(proxy_pid))

    if not qemu_already_running:
        if (serial_qemu_connection == "PTY"):
            assert(use_proxy)
            # QEMU starts up in halted mode, must send the "c" command to let it
            # boot the system
            attempts = 0
            while (True):
                attempts += 1
                if (attempts > 60):
                    print("can't connect to QEMU")
                    assert(False)
                try:
                    f_qemu_stdin.write("c\n")
                    break
                except IOError as e:
                    print("waiting for QEMU, communication failures: " + attempts)
                    time.sleep(1)

            print("QEMU machine released...")

        # give QEMU some time to run
        time.sleep(2)

        # check that CapDL Loader suspends itself after it has successfully set
        # the system setup
        (ret, text, expr_fail) = logs.check_log_match_sequence(
            logs.open_file_non_blocking(test_system_out_file, 'r'),
            ["Booting all finished, dropped to user space",
             "Done; suspending..."],
            15)

        if not ret:
            pytest.fail(" missing: %s"%(expr_fail))

        print("QEMU up and system running")

    f_test_output = logs.open_file_non_blocking(test_system_out_file, 'r')

    return (f_qemu_stdin, f_test_output, f_qemu_stderr)


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
def use_qemu_with_proxy(request, use_proxy=False):

    log_dir = get_log_dir(request)

    test_system_out_file  = os.path.join(log_dir, "guest_out.txt")

    qemu_stdin_file       = os.path.join(log_dir, "qemu_in.fifo")
    qemu_stdout_file      = os.path.join(log_dir, "qemu_out.txt")
    qemu_stderr_file      = os.path.join(log_dir, "qemu_err.txt")
    qemu_pid_file         = os.path.join(log_dir, "qemu.pid")

    proxy_stdout_file     = None if not use_proxy \
                            else os.path.join(log_dir, "proxy_out.txt")

    proxy_pid_file        = None if not use_proxy \
                            else os.path.join(log_dir, "proxy.pid")

    # create pipe for QEMU input
    os.mkfifo(qemu_stdin_file)


    # pytest will run this for each test case
    yield (lambda system:
            start_or_attach_to_qemu_and_proxy(
                request,
                system,
                test_system_out_file,
                qemu_stdin_file,
                qemu_stdout_file,
                qemu_stderr_file,
                qemu_pid_file,
                use_proxy,
                proxy_stdout_file,
                proxy_pid_file) )

    # tear-down phase

    print("\n")

    print("terminating QEMU...")
    terminate_process_by_pid_file(qemu_pid_file)

    # must unlink the pipe so the next test run can create it again
    os.unlink(qemu_stdin_file)

    if use_proxy:
        print("terminating Proxy...")
        terminate_process_by_pid_file(proxy_pid_file)


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
    yield from use_qemu_with_proxy(request)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(request):
    yield from use_qemu_with_proxy(request, True)


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

    parser.addoption(
        "--target",
        required=True,
        help="target platform")

    parser.addoption(
        "--log_dir",
        help="folder where to put the logs")
