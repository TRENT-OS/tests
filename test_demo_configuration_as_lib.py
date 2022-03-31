import pytest
import re

import logs # logs module from the common directory in TA

def test_run_demo(boot_with_proxy):
    test_runner = boot_with_proxy("demo_configuration_as_lib")

    success_msg = "# end #"
    timeout = 15
    (text, match) = logs.get_match_in_line(
                        test_runner.get_system_log(),
                        re.compile(success_msg),
                        timeout)
    assert match == success_msg
