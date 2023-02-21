import pytest
import time
import socket
import board_automation.tools


#-------------------------------------------------------------------------------
def throughput_str(cnt, delta):
    t = cnt / delta
    p = ''

    if (t > 1024):
        t = t / 1024
        p = 'K'

    if (t > 1024):
        t = t / 1024
        p = 'M'

    if (t > 1024):
        t = t / 1024
        p = 'G'

    if (t > 1024):
        t = t / 1024
        p = 'T'

    return '{:.2f} {}iB/s'.format(t, p)


#-------------------------------------------------------------------------------
def test_uart(boot):
    """
    Test UART data stream handling and throughput
    """

    test_runner = boot()

    # synchronize with test application, timeout is 10 secs based on empirical
    # evidence. System load can likely impact this timing.
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'initialize UART ok',
            'UART tester loop running',
        ],
        10)

    if not ret:
        pytest.fail('could not detect test start')

    serial_socket = test_runner.get_serial_socket()

    def generator_inc_byte_stream(start=0):
        # generate an endless byte stream: 00 01 02 ... FE FF 00 01 ...
        data_byte = start
        while True:
            yield data_byte
            data_byte = (data_byte + 1) & 0xFF

    g = generator_inc_byte_stream()

    # When the serial port is configured at 115200 baud 8N1, we have 10 bits per
    # byte (start bit, 8 bit data, stop bit) and the throughput is roughly
    # 11.52 KiByte/s (= 115200/10). However, if we run over a network socket,
    # internal data buffering can happen and what we send is neither what is
    # actually sent nor what the other side receives. Linux seems to have a
    # 2.5 MiByte TCP socket buffer for sending, so any amount of data below that
    # could could see a raw send throughput rates of over 800 MiB/s. Just when
    # all buffers are full and flow control kicks in, the actual network speed
    # is the limitation. However, even this is usually still way above the UART
    # baudrates we are expecting. Thus, if no physical UART is involved that
    # really limits the speed or the QEMU UART simulation does no simulate
    # baudrates, things tend to run as fast as the UART driver will see and read
    # the incoming data. This messes badly with the assumption that a UART at
    # 115200 baud is so slow, that things can be handled easily without flow
    # control.
    # To support throttling on the sender side already, we feed the socket with
    # blocks and apply a delay after each write. The throughput is
    # then (1 / t_throttle) * block_size, e.g. for 512 byte data blocks we get:
    #   10 ms -> 50 KiByte/s
    #   20 ms -> 25 KiByte/s
    #   25 ms -> 20 KiByte/s
    #   40 ms -> 12.5 KiByte/s (close to real 115200 baudrate)
    #   50 ms -> 10 KiByte/s

    block_size = 512
    loops = 4096 # send 2 MiByte data in 4096 block of 512 byte each

    t1 = None # set when sender thread starts
    t2 = None # set when sender thread ends
    t_throttle = 0.04 if isinstance(
                            test_runner,
                            board_automation.automation_QEMU.QemuProxyRunner) \
                 else None

    if t_throttle:
        serial_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    # run the actual sending of data in a thread, so we can apply throttling
    # easily by sleeping.
    def send_data(thread):
        nonlocal t1, t2  # modification applies to variable of outer scope
        print('UART host sender thread running')
        t1 = time.time()
        for _ in range(loops):
            arr = bytearray([ next(g) for _ in range(block_size) ])
            t_block_start = time.time()
            serial_socket.sendall(arr)
            if t_throttle:
                t_sleep = t_throttle - (time.time() - t_block_start)
                if t_sleep > 0:
                    time.sleep(t_sleep)
        t2 = time.time()

        print('Throughput host send: ' +
              throughput_str(block_size * loops, t2 - t1) )

    sender_thread = board_automation.tools.run_in_thread(send_data)

    # check if the test started. The 64 KiByte must go trough in a bit over
    # 5.5 secs, so giving 10 secs will allow some startup delays.
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'bytes processed: 0x10000', # 64 KiByte
        ],
        10)

    if not ret:
        pytest.fail('throughput start failed')

    # If we are here, 64 KiB are already through. There are 1984 KiByte left,
    # which take a bit over 172 secs. Giving 200 secs secs will do well.
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            'bytes processed: 0x100000', # 1 MiByte
            'bytes processed: 0x200000', # 2 MiByte
        ],
        200)

    if not ret:
        pytest.fail('throughput test failed')

    t3 = time.time()
    delta = t3 - t1 # thread has updated t1
    print('Throughput serial: {} (took {:.2f} secs)'.format(
            throughput_str(block_size * loops, delta),
            delta) )

    # Sanity check, the sender thread must have terminated. Since it prints
    # something at the end, we give it one second here to finish this.
    sender_thread.join(timeout=1);
    if sender_thread.is_alive():
        pytest.fail('sender thread did not terminate')
