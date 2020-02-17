import pytest

import sys
sys.path.append('../common')

import logs
import os
import re
import time
import subprocess
import datetime

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
    proxy_pid_file = None
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

        start_process_and_create_pid_file(
            "qemu-system-arm" +
                " -machine xilinx-zynq-a9" +
                " -nographic" +
                #" -s" +  # shortcut for -gdb tcp::1234
                " -S" +  # freeze the CPU at startup
                #" -serial tcp:localhost:4444,server" +
                " -serial pty" +
                " -serial file:" + test_system_out_file +
                " -m size=1024M" +
                " -kernel " + test_image +
                " 2>" + qemu_stderr_file +
                " >" + qemu_stdout_file +
                " <" + qemu_stdin_file,
            qemu_pid_file)

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
            print("  proxy stdout:       " + proxy_stdout_file)
            # search for dev/ptsX info in QEMU stderr
            (text, match) = logs.get_match_in_line(
                                f_qemu_stderr,
                                re.compile('(\/dev\/pts\/\d)'),
                                10)
            assert(match)

            start_process_and_create_pid_file(
                proxy_app + \
                    " -c PTY:" + match + # PTY to connect to
                    " -t 1" # enable TAP
                    " > " + proxy_stdout_file,
                proxy_pid_file)

            proxy_pid = get_pid_from_pid_file(proxy_pid_file)
            print("Proxy starting (PID %u) ..."%(proxy_pid))

    if not qemu_already_running:
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
def use_qemu_with_proxy(request, proxy_app=None):

    test_module = os.path.splitext(request.node.name)[0]
    tmp_dir = os.path.join(pytest.qemu_log_dir, test_module)

    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)

    test_system_out_file  = os.path.join(tmp_dir, "guest_out.txt")

    qemu_stdin_file       = os.path.join(tmp_dir, "qemu_in.fifo")
    qemu_stdout_file      = os.path.join(tmp_dir, "qemu_out.txt")
    qemu_stderr_file      = os.path.join(tmp_dir, "qemu_err.txt")
    qemu_pid_file         = os.path.join(tmp_dir, "qemu.pid")

    proxy_stdout_file     = None if proxy_app is None \
                            else os.path.join(tmp_dir, "proxy_out.txt")

    proxy_pid_file        = None if proxy_app is None \
                            else os.path.join(tmp_dir, "proxy.pid")

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
                proxy_pid_file) )

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
@pytest.fixture(scope="module")
def boot(request):
    yield from use_qemu_with_proxy(request)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(request):
    proxy_app = request.config.option.proxy_path
    yield from use_qemu_with_proxy(request, proxy_app)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_logging_for_qemu_and_proxy(request):

    # print("request.config.option", request.config.option)
    # print("  workspace_path: ", request.config.option.workspace_path)
    # print("  proxy_path: ", request.config.option.proxy_path)

    timestamp_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # ToDo: find a better way where to store this.
    pytest.qemu_log_dir = os.path.join(request.config.option.workspace_path,
                                       "test-logs-"+timestamp_str)



#-------------------------------------------------------------------------------
def pytest_addoption(parser):

    parser.addoption(
        "--workspace_path",
        help="location of the workspace that holds the test image")

    parser.addoption(
        "--proxy_path",
        help="location of the proxy application")
