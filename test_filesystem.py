import pytest, sys
import test_parser as parser

#-------------------------------------------------------------------------------
def test_filesystem_generic(boot):

    test_run = boot('')
    f_out = test_run[1]

    (ret, text, expr_fail) = logs.check_log_match_sequence(
    f_out,
    [
        "test_OS_FileSystem_little_fs() SUCCESS",
        "test_OS_FileSystem_spiffs() SUCCESS",
        "test_OS_FileSystem_fat() SUCCESS",
        "All tests successfully completed"
    ],
    20)

    if not ret:
        pytest.fail(" missing: %s"%(expr_fail))
