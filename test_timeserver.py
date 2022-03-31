import pytest


#-------------------------------------------------------------------------------
def test_timer(boot):
    """
    Test timer
    """

    test_runner = boot()[0]

    # synchronize with test application
    (ret, idx) = test_runner.system_log_match_sequence(
        [
            '[ticker] run',
        ],
        5)

    if not ret:
        pytest.fail('could not detect test start')

    # If the timer works, there is one message per second, but it seems on some
    # system the timer setup is broken:
    # * zynq7000/QEMU: the "subjective second" takes 95 seconds in the real
    #                  world.

    (ret, idx) = test_runner.system_log_match_sequence(
        [
            '1 sec tick, delta',
        ],
        100)

    if not ret:
        pytest.fail('timer test failed')
