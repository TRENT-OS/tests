import pytest
import test_parser as parser

test_system = "bmrbl"


#-------------------------------------------------------------------------------
def test_bmrbl_boot_menu(boot_bare_metal):
    """
    Run simple bmrbl test that checks if the bmrbl loads correctly and displays
    the boot menu.
    """

    test_runner = boot_bare_metal()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ 'reading boot configuration from ROM ...' ], 5 ),
        ( [ 'Choose mode:' ], 5 )

    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))
