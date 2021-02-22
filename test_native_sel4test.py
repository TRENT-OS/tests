import pytest
import logs # logs module from the common directory in TA

def test_run_native_sel4test(boot_sel4_native):
    """
    run native sel4test
    """

    test_runner = boot_sel4_native()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        # the sel4test system prints the untypeds when it starts
        ( [ 'List of untypeds' ], 1 ),
        # the sel4test application starts
        ( [ 'seL4 Test' ], 1),
        # and it will start running tests
        ( [ 'Starting test suite sel4test' ], 2),
        # first test case
        ( [ 'Starting test 1: SYSCALL0000' ], 2),
        # and eventually, all test have passed
        ( ["All is well in the universe"], 180)

    ])

    if not ret:
        pytest.fail('sel4test string #{}.{} not found'.format(idx, idx2))
