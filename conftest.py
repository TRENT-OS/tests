import pytest

import sys
sys.path.append('../common')

import logs
import tempfile
import os
import re
import time
import subprocess


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
    test_image,
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
    if not qemu_already_running:
        print("launching qemu on " + test_image)
        start_process_and_create_pid_file(
            "qemu-system-arm" +
                " -machine xilinx-zynq-a9" +
                " -nographic" +
                " -s" +
                " -S" +
                " -serial pty" +
                " -serial file:" + test_system_out_file +
                " -m size=1024M" +
                " -kernel " + test_image +
                " 2>" + qemu_stderr_file +
                " >" + qemu_stdout_file +
                " <" + qemu_stdin_file,
            qemu_pid_file)
        print("process detached")

        time.sleep(1)

    f_err   = logs.open_file_non_blocking(qemu_stderr_file, "r")
    f_in    = open(qemu_stdin_file, "w", buffering=1)
    f_out   = None

    if proxy_app is not None:
        # search for dev/ptsX info in QEMU stderr
        (text, match) = logs.get_match_in_line(f_err, re.compile('(\/dev\/pts\/\d)'), 10)
        assert(match)

        if not os.path.isfile(proxy_pid_file):
            print("Start proxy...")
            start_process_and_create_pid_file(
                proxy_app + " " + match + " > " + proxy_stdout_file,
                proxy_pid_file)
            print("Detached proxy app process")

    if not qemu_already_running:
        attempts = 0
        while (True):
            attempts += 1
            if (attempts > 60):
                print("can't connect to QEMU")
                assert(False)
            try:
                f_in.write("c\n")
                break
            except IOError as e:
                print("waiting for QEMU, communication failures: " + attempts)
                time.sleep(1)

        time.sleep(2)

    f_out = logs.open_file_non_blocking(test_system_out_file, 'r', '\r')

    return (f_in, f_out, f_err)


#-------------------------------------------------------------------------------
def use_qemu_with_proxy(workspace_path, proxy_app=None):
    tmp_dir = tempfile.mkdtemp()

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

    # pytest wil run this for each test case
    yield (lambda image_subpath:
            start_or_attach_to_qemu_and_proxy(
                os.path.join(workspace_path, image_subpath),
                test_system_out_file,
                qemu_stdin_file,
                qemu_stdout_file,
                qemu_stderr_file,
                qemu_pid_file,
                proxy_app,
                proxy_stdout_file,
                proxy_pid_file) )

    print("\n")

    print("terminating QEMU...")
    terminate_process_by_pid_file(qemu_pid_file)

    if proxy_app is not None:
        print("terminating Proxy...")
        terminate_process_by_pid_file(proxy_pid_file)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot(workspace_path):
    yield from use_qemu_with_proxy(workspace_path)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(workspace_path, proxy_path):
    # proxy_path holds binary with full path
    yield from use_qemu_with_proxy(workspace_path, proxy_path)


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
