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
def start_qemu_and_proxy(
    image_path,
    out_file,
    in_file,
    hout_file,
    herr_file,
    qemu_pid_file_name,
    proxy_path = None,
    pout_file = None,
    proxy_pid_file_name = None
):
    print('guest output file is ' + out_file)
    print('host input file is ' + in_file)
    print('host output file is ' + hout_file)
    print('host err file is ' + herr_file)
    if pout_file is not None:
        print('proxy out file is ' + pout_file)

    if not os.path.isfile(qemu_pid_file_name):
        print("launching qemu on " + image_path)
        start_process_and_create_pid_file(
            "qemu-system-arm" +
                " -machine xilinx-zynq-a9" +
                " -nographic" +
                " -s" +
                " -S" +
                " -serial pty" +
                " -serial file:" + out_file +
                " -m size=1024M" +
                " -kernel " + image_path +
                " 2>" + herr_file +
                " >" + hout_file +
                " <" + in_file,
            qemu_pid_file_name)
        print("process detached")

        time.sleep(1)

    f_err   = logs.open_file_non_blocking(herr_file, "r")
    f_in    = open(in_file, "w", buffering=1)
    f_out   = None

    if proxy_path is not None:
        (text, match) = logs.get_match_in_line(f_err, re.compile('(\/dev\/pts\/\d)'), 10)
        assert(match)

        if not os.path.isfile(proxy_pid_file_name):
            print("Start proxy...")
            start_process_and_create_pid_file(
                proxy_path + " " + match + " > " + pout_file,
                proxy_pid_file_name)
            print("Detached proxy app process")

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
    f_out = logs.open_file_non_blocking(out_file, 'r', '\r')

    return (f_in, f_out, f_err)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot(workspace_path):
    d = tempfile.mkdtemp()

    in_file     = os.path.join(d, "qemu_in.fifo")
    out_file    = os.path.join(d, "guest_out.txt")
    hout_file   = os.path.join(d, "qemu_out.txt")
    herr_file   = os.path.join(d, "qemu_err.txt")

    qemu_pid_file_name  = os.path.join(d, "qemu.pid")

    os.mkfifo(in_file)

    def boot_image_path(image_subpath):
        return start_qemu_and_proxy(
                    os.path.join(workspace_path, image_subpath),
                    out_file,
                    in_file,
                    hout_file,
                    herr_file,
                    qemu_pid_file_name)

    yield boot_image_path

    print("\n")
    print("terminating qemu...")
    terminate_process_by_pid_file(qemu_pid_file_name)


#-------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def boot_with_proxy(workspace_path, proxy_path):
    d = tempfile.mkdtemp()

    in_file     = os.path.join(d, "qemu_in.fifo")
    out_file    = os.path.join(d, "guest_out.txt")
    hout_file   = os.path.join(d, "qemu_out.txt")
    herr_file   = os.path.join(d, "qemu_err.txt")
    pout_file   = os.path.join(d, "proxy_out.txt")

    qemu_pid_file_name  = os.path.join(d, "qemu.pid")
    proxy_pid_file_name = os.path.join(d, "proxy.pid")

    os.mkfifo(in_file)

    def boot_image_path(image_subpath):
        return start_qemu_and_proxy(
                    os.path.join(workspace_path, image_subpath),
                    out_file,
                    in_file,
                    hout_file,
                    herr_file,
                    qemu_pid_file_name,
                    proxy_path,
                    pout_file,
                    proxy_pid_file_name)

    yield boot_image_path

    print("\n")
    print("terminating qemu...")
    terminate_process_by_pid_file(qemu_pid_file_name)
    print("terminating proxy...")
    terminate_process_by_pid_file(proxy_pid_file_name)


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
