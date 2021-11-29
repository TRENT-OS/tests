import pytest
import logs # logs module from the common directory in TA

def test_run_native_sel4test(boot_sel4_native):
    """
    run native sel4bench
    """

    test_runner = boot_sel4_native()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'Serserv Server: main: Bound to the serial driver.' ], 1 ),
        # ToDo: add strings here
        ( ["here be dragons"], 180)

    ])

    if not ret:
        pytest.fail('sel4test string #{}.{} not found'.format(idx, idx2))
