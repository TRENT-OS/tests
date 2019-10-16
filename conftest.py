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

        image_path = os.path.join(workspace_path, image_subpath)

        print('guest output file is ' + out_file)
        print('host input file is ' + in_file)
        print('host output file is ' + hout_file)
        print('host err file is ' + herr_file)

        if not os.path.isfile(qemu_pid_file_name):
            print("launching qemu on " + image_path)
            os.system("qemu-system-arm -machine xilinx-zynq-a9  -nographic -s -S -serial pty -serial file:" + out_file +" -m size=1024M  -kernel " + image_path + " 2>" + herr_file + " >" + hout_file + " <" + in_file + "& echo $! > "+qemu_pid_file_name+" &")
            print("process detached")

            time.sleep(1)

        f_err   = logs.open_file_non_blocking(herr_file, "r")
        f_in    = open(in_file, "w", buffering=1)
        f_out   = None

        (text, match) = logs.get_match_in_line(f_err, re.compile('(\/dev\/pts\/\d)'), 10)
        assert(match)

        cont = True
        attempts = 0
        while cont:
            connected = False
            attempts += 1
            try:
                f_in.write("c\n")
                connected = True
            except IOError as e:
                time.sleep(1)
            cont = not connected and attempts < 60

        time.sleep(2)
        f_out = logs.open_file_non_blocking(out_file, 'r', '\r')

        return (f_in, f_out, f_err)

    yield boot_image_path

    print("\n")
    print("terminating qemu...")
    os.system("kill `cat "+qemu_pid_file_name+"`")


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
        image_path = os.path.join(workspace_path, image_subpath)

        print('guest output file is ' + out_file)
        print('host input file is ' + in_file)
        print('host output file is ' + hout_file)
        print('host err file is ' + herr_file)
        print('proxy out file is ' + pout_file)


        if not os.path.isfile(qemu_pid_file_name):
            print("launching qemu on " + image_path)
            os.system("qemu-system-arm -machine xilinx-zynq-a9  -nographic -s -S -serial pty -serial file:" + out_file +" -m size=1024M  -kernel " + image_path + " 2>" + herr_file + " >" + hout_file + " <" + in_file + "& echo $! > "+qemu_pid_file_name+" &")
            print("process detached")

            time.sleep(1)

        f_err   = logs.open_file_non_blocking(herr_file, "r")
        f_in    = open(in_file, "w", buffering=1)
        f_out   = None

        (text, match) = logs.get_match_in_line(f_err, re.compile('(\/dev\/pts\/\d)'), 10)
        assert(match)

        if not os.path.isfile(proxy_pid_file_name):
            print("Start proxy...")
            os.system(proxy_path+" "+match+" > "+pout_file+" & echo $! > "+proxy_pid_file_name+" &")
            print("Detached proxy app process")

        cont = True
        attempts = 0
        while cont:
            connected = False
            attempts += 1
            try:
                f_in.write("c\n")
                connected = True
            except IOError as e:
                time.sleep(1)
            cont = not connected and attempts < 60

        time.sleep(2)
        f_out = logs.open_file_non_blocking(out_file, 'r', '\r')

        return (f_in, f_out, f_err)

    yield boot_image_path

    print("\n")
    print("terminating qemu...")
    os.system("kill `cat "+qemu_pid_file_name+"`")
    print("terminating proxy...")
    os.system("kill `cat "+proxy_pid_file_name+"`")


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
