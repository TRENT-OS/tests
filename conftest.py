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
    print("Log files:")
    print("  test system output: " + test_system_out_file)
    print("  QEMU stdin:         " + qemu_stdin_file)
    print("  QEMU stdout:        " + qemu_stdout_file)
    print("  QEMU stderr:        " + qemu_stderr_file)

    if proxy_stdout_file is not None:
        print("  proxy stdout:       " + proxy_stdout_file)

    qemu_already_running = os.path.isfile(qemu_pid_file)

    proxy_already_running = False if proxy_pid_file is None \
                            else os.path.isfile(proxy_pid_file)


    if qemu_already_running:
        print("QEMU already running")
    else:
        test_image = os.path.join(
                        test_image_descriptor[0],
                        "build-zynq7000-Debug-"+test_image_descriptor[1],
                        "images",
                        "capdl-loader-image-arm-zynq7000")
        print("launching QEMU with " + test_image)

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
        print("process detached")

    # seems QEMU tried to read from strdin, so we have to open the pipe now
    # to unblock it
    f_qemu_stdin = open(qemu_stdin_file, "w", buffering=1)

    # give QEMU some time to start
    time.sleep(1)

    f_qemu_stderr = logs.open_file_non_blocking(qemu_stderr_file, "r")

    if proxy_app is not None:
        if proxy_already_running:
            print("Proxy already running")
        elif qemu_already_running:
            # Proxy can't be running when we've just started QEMU, as they can
            # only be started togehter
            print("ERROR: can't start proxy if QEMU is already running")
            assert False
        else:
            print("Start proxy: " + proxy_app)
            # search for dev/ptsX info in QEMU stderr
            (text, match) = logs.get_match_in_line(
                                f_qemu_stderr,
                                re.compile('(\/dev\/pts\/\d)'),
                                10)
            assert(match)

            tap_params = (match +
                 # legacy parameters for the HAR demo application, it is necessary to put them here for a trivial parameter count that should be solved with a 'param_name=value' approach"
                " 7999 HAR-test-HUB.azure-devices.net 8883 " +
                # 0 means disable picotcp on proxy, 1 means enable tap on proxy
                " 0 1")
            start_process_and_create_pid_file(
                proxy_app + " " + tap_params +" > " + proxy_stdout_file,
                proxy_pid_file)
            print("Detached proxy app process")

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

        # give QEMU some time to run
        time.sleep(2)

    print("QEMU up and system running")
    f_test_output = logs.open_file_non_blocking(test_system_out_file, 'r')

    return (f_qemu_stdin, f_test_output, f_qemu_stderr)


#-------------------------------------------------------------------------------
def use_qemu_with_proxy(request, workspace_path, proxy_app=None):

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
                [workspace_path, system],
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
def boot(request, workspace_path):
    yield from use_qemu_with_proxy(request, workspace_path)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(request, workspace_path, proxy_path):
    # proxy_path holds binary with full path
    yield from use_qemu_with_proxy(request, workspace_path, proxy_path)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_logging_for_qemu_and_proxy(request, workspace_path):

    timestamp_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # ToDo: find a better way where to store this.
    pytest.qemu_log_dir = os.path.join(workspace_path,
                                       "test-logs-"+timestamp_str)


#-------------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption("--workspace_path",
                     action="append",
                     default=[],
                     help="Path to the application image")

    parser.addoption("--proxy_path",
                     action="append",
                     default=[],
                     help="Path to the proxy application")


#-------------------------------------------------------------------------------
def pytest_generate_tests(metafunc):
    if 'workspace_path' in metafunc.fixturenames:
        metafunc.parametrize("workspace_path",
                             metafunc.config.getoption('workspace_path'),
                             scope="session")
    if 'proxy_path' in metafunc.fixturenames:
        metafunc.parametrize("proxy_path",
                             metafunc.config.getoption('proxy_path'),
                             scope="session")
