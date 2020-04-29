import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time
import subprocess
import datetime
import multiprocessing, ssl, socket

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
def start_or_attach_to_qemu_and_proxy(
    test_image_descriptor,
    test_system_out_file,
    qemu_stdin_file,
    qemu_stdout_file,
    qemu_stderr_file,
    qemu_pid_file,
    proxy_app = None,
    proxy_stdout_file = None,
    proxy_pid_file = None,
    qemu_connection = None
):
    qemu_already_running = os.path.isfile(qemu_pid_file)

    proxy_already_running = False if proxy_pid_file is None \
                            else os.path.isfile(proxy_pid_file)

    f_qemu_stdin = None

    print("")

    if qemu_already_running:
        qemu_pid = get_pid_from_pid_file(qemu_pid_file)
        print("QEMU already running (PID %u)"%(qemu_pid))

    else:
        test_image = os.path.join(
                        test_image_descriptor[0],
                        "build-zynq7000-Debug-"+test_image_descriptor[1],
                        "images",
                        "capdl-loader-image-arm-zynq7000")

        print("launching QEMU with " + test_image)
        print("  test system output: " + test_system_out_file)
        print("  QEMU stdin:         " + qemu_stdin_file)
        print("  QEMU stdout:        " + qemu_stdout_file)
        print("  QEMU stderr:        " + qemu_stderr_file)

        assert(os.path.isfile(test_image))

        connection_string = " -serial /dev/null"

        if(qemu_connection == "PTY"):
            # must use "-S" to freeze the QEMU at startup,
            # unfreezing when the other end of PTY is
            # connected
            connection_string = " -S -serial pty"
        elif (qemu_connection == "TCP"):
            # QEMU will freeze on startup until it can
            # connect to the server
            connection_string = " -serial tcp:localhost:4444,server"
        
        qemu_cmd = ("qemu-system-arm" +
                " -machine xilinx-zynq-a9" +
                " -nographic" +
                connection_string + 
                " -serial file:" + test_system_out_file +
                " -m size=1024M" +
                " -kernel " + test_image +
                " 2>" + qemu_stderr_file +
                " >" + qemu_stdout_file +
                " <" + qemu_stdin_file)

        start_process_and_create_pid_file(qemu_cmd, qemu_pid_file)

        # seems QEMU tries to read from strdin, so we have to open the pipe now
        # to unblock it
        f_qemu_stdin = open(qemu_stdin_file, "w", buffering=1)

        qemu_pid = get_pid_from_pid_file(qemu_pid_file)
        print("QEMU starting (PID %u) ..."%(qemu_pid))
        # give QEMU some time to start
        time.sleep(1)


    f_qemu_stderr = logs.open_file_non_blocking(qemu_stderr_file, "r")

    if proxy_app is not None:
        if proxy_already_running:
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

            if(qemu_connection == "PTY"):
                # search for dev/ptsX info in QEMU stderr
                (text, match) = logs.get_match_in_line(
                                    f_qemu_stderr,
                                    re.compile('(\/dev\/pts\/\d)'),
                                    10)
                assert(match)

                connection_mode = "PTY:" + match # PTY to connect to
            elif(qemu_connection == "TCP"):
                connection_mode = "TCP:4444"
            else:
                print("ERROR: invalid qemu_connection %s", qemu_connection)
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
        if(qemu_connection == "PTY"):
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

        print("QEMU up and system running")

    f_test_output = logs.open_file_non_blocking(test_system_out_file, 'r')

    return (f_qemu_stdin, f_test_output, f_qemu_stderr)


#-------------------------------------------------------------------------------
def use_qemu_with_proxy(request, log_dir, proxy_app=None, qemu_connection=None):

    test_system_out_file  = os.path.join(log_dir, "guest_out.txt")

    qemu_stdin_file       = os.path.join(log_dir, "qemu_in.fifo")
    qemu_stdout_file      = os.path.join(log_dir, "qemu_out.txt")
    qemu_stderr_file      = os.path.join(log_dir, "qemu_err.txt")
    qemu_pid_file         = os.path.join(log_dir, "qemu.pid")

    proxy_stdout_file     = None if proxy_app is None \
                            else os.path.join(log_dir, "proxy_out.txt")

    proxy_pid_file        = None if proxy_app is None \
                            else os.path.join(log_dir, "proxy.pid")

    # create pipe for QEMU input
    os.mkfifo(qemu_stdin_file)

    # pytest will run this for each test case
    yield (lambda system:
            start_or_attach_to_qemu_and_proxy(
                [request.config.option.workspace_path, system],
                test_system_out_file,
                qemu_stdin_file,
                qemu_stdout_file,
                qemu_stderr_file,
                qemu_pid_file,
                proxy_app,
                proxy_stdout_file,
                proxy_pid_file,
                qemu_connection) )

    # tear-down phase

    print("\n")

    print("terminating QEMU...")
    terminate_process_by_pid_file(qemu_pid_file)

    # must unlink the pipe so the next test run can create it again
    os.unlink(qemu_stdin_file)

    if proxy_app is not None:
        print("terminating Proxy...")
        terminate_process_by_pid_file(proxy_pid_file)


#-------------------------------------------------------------------------------
def tls_server_proc(port = 8888, timeout = 180):
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(
            certfile="test_tls_api/cert.pem",
            keyfile="test_tls_api/key.pem"
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
def create_log_dir(request):
    test_module = os.path.splitext(request.node.name)[0]
    log_dir = os.path.join(request.config.option.workspace_path,
                           request.config.option.test_run_id,
                           test_module)

    if os.path.isdir(log_dir):
        pytest.fail("log dir already exists: %s"%(log_dir))

    os.makedirs(log_dir)
    return log_dir


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot(request):
    log_dir = create_log_dir(request)
    yield from use_qemu_with_proxy(request, log_dir)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(request):
    log_dir = create_log_dir(request)
    proxy_app = request.config.option.proxy_path
    qemu_connection = request.config.option.qemu_connection
    yield from use_qemu_with_proxy(request, log_dir, proxy_app, qemu_connection)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def tls_server():
    proc = multiprocessing.Process(target=tls_server_proc)
    proc.start()
    yield proc
    proc.terminate()


#-------------------------------------------------------------------------------
def pytest_addoption(parser):

    parser.addoption(
        "--workspace_path",
        required=True,
        help="location of the workspace that holds the test image")

    # proxy is an optional parameter, because some tests don't need it
    parser.addoption(
        "--proxy_path",
        help="location of the proxy application")

    parser.addoption(
        "--qemu_connection",
        help="QEMU connection mode (PTY or TCP)")

    parser.addoption(
        "--test_run_id",
        required=True,
        help="test run ID")
