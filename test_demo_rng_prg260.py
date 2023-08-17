import pytest
import socket
import board_automation.tools
import serial
import multiprocessing

################################################################################
#                                Attention!                                    #
#                                                                              #
#   This test requires a special setup and launch in order to be able to       #
#   connect to the rng hardware from within qemu and docker.                   #
#   Please consult the README at /src/src/tests/test_rng_prg260/README.md      #
#   for instructions.                                                          #
#                                                                              #
################################################################################

TTYUSB_DEVICE = "/dev/ttyUSB1" # Change the path according to your setup

#-------------------------------------------------------------------------------

def qemu_listening_thrd(qemu_sock, rng_uart):
    while(1):
        rng_uart.write(qemu_sock.recv(1))

def uart_listening_thrd(qemu_sock, rng_uart):
    while(1):
        qemu_sock.sendall(rng_uart.read(1))


class SerialProxy:
    def __init__(self):
        self.__get_qemu_sock()
        self.__get_rng_tty()
        self.thrd_fn = [qemu_listening_thrd, uart_listening_thrd]
        self.__launch()

    def __get_qemu_sock(self):
        self.qemu_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.qemu_sock.connect(("localhost", 7000))

    def __get_rng_tty(self):
        self.rng_uart = serial.Serial(TTYUSB_DEVICE, 115200)

    def __launch(self):
        self.thrd_pool = [ multiprocessing.Process(target=fn, args=(self.qemu_sock, self.rng_uart)) for fn in self.thrd_fn ]
        print("SerialProxy: Starting threads...")
        [ thrd.start() for thrd in self.thrd_pool ]

    def __del__(self):
        [ thrd.terminate() for thrd in self.thrd_pool ]

#-------------------------------------------------------------------------------
def test_rng(boot):
    """
    Test UART echo send data and receive back
    """

    serialProxy = SerialProxy()
    test_runner = boot()
    print("After booot")
    

    # synchronize with test application, timeout is 10 secs based on empirical
    # evidence. System load can likely impact this timing.
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'initialize UART ok',
            "Success Test passed!"
        ],
        30)

    if not ret:
        pytest.fail('could not detect test start')
