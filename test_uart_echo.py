#
# Copyright (C) 2023-2024, HENSOLDT Cyber GmbH
# 
# SPDX-License-Identifier: GPL-2.0-or-later
#
# For commercial licensing, contact: info.cyber@hensoldt.net
#

import pytest
import time
import board_automation.tools
import random
import string
import time

def rand_letters(amount):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=amount))


#-------------------------------------------------------------------------------
def test_uart_echo(boot):
    """
    Test UART echo send data and receive back
    """

    test_runner = boot()

    # synchronize with test application, timeout is 10 secs based on empirical
    # evidence. System load can likely impact this timing.
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'initialize UART ok',
        ],
        10)

    if not ret:
        pytest.fail('could not detect test start')

    serial_socket = test_runner.get_serial_socket()

    serial_socket.settimeout(30)

    block_size = 512
    loops = 32

    recv_data = ""

    if isinstance(test_runner.board_runner, \
                  board_automation.automation_HW_CI.CIBoardRunner):
        print("Testing on hardware CI")
        serial_socket.recv(1) #flush buffer
    
    for i in range(loops):
        data = rand_letters(block_size)
        t1 = time.time()
        serial_socket.sendall(data.encode("utf-8"))

        while len(recv_data) < block_size:
            try:
                recv_data += serial_socket.recv(block_size).decode()
            except Exception as e:
                print(f"Exception: {e}")
                break
        
        if data != recv_data[:block_size]:
            print(f"Data: {data}\nRata: {recv_data}")
            pytest.fail('Received data does not match with sent data')

        print(f"Sent and received Packet {i+1} of {loops}, Duration: {'%.2f' % ((time.time() - t1)*1000)}ms")

        recv_data = recv_data[block_size:]
        time.sleep(0.5)

    serial_socket.close()
    print(f"Success: {block_size*loops} Bytes sent and received")
