from test_logserver_data.common import *
from enum import Enum
import time
import re
import os
import logs
import pytest

import sys
sys.path.append('../common')


class LogTargets(Enum):
    CONSOLE_ONLY       = 0
    CONSOLE_AND_FILE_1 = 1
    CONSOLE_AND_FILE_2 = 2


def test_smoke_test(boot_with_proxy):
    """ Generic smoke test of logging.

    Something is logged, system does not crash.
    """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    success_msg = LogClients.LOG_SERVER.value

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(success_msg),
        timeout)

    assert match == success_msg


def test_different_clients_logging(boot_with_proxy):
    """ Different clients can add new entries to the log. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    success_msg = LogClients.LVL_NONE.value \
                + LogMessagesPatterns.NONE_LVL_MSG.value

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(success_msg),
        timeout)

    assert match

    success_msg = LogClients.LVL_ASSERT.value \
                + LogMessagesPatterns.ASSERT_LVL_MSG.value

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(success_msg),
        timeout)

    assert match

    success_msg = LogClients.LVL_FATAL.value \
                + LogMessagesPatterns.FATAL_LVL_MSG.value

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(success_msg),
        timeout)

    assert match

    success_msg = LogClients.LVL_ERROR.value \
                + LogMessagesPatterns.ERROR_LVL_MSG.value

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(success_msg),
        timeout)

    assert match


def test_logging_to_console(boot_with_proxy):
    """ Logs are printed on the console (stdout). """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    success_msg = LogClients.LVL_WARNING.value \
                + LogMessagesPatterns.WARNING_LVL_MSG.value

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(success_msg),
        timeout)

    assert match


def test_logging_to_file(boot_with_proxy):
    """ Logs are printed to the file. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    log_file01_content = re.split(log_targets_marker, text)[1]
    assert re.search(LogClients.LVL_FATAL.value, log_file01_content)


def test_logging_client_filter_null(boot_with_proxy):
    """ Logging with filter set to null on the client side.

    In this case LVL_DEBUG has been chosen as the one that has a NULL filter on
    its side but any of the LVL_* clients could be chosen.

    """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_DEBUG.value, text, 10)


def test_logging_server_and_client_filter_null(boot_with_proxy):
    """ Logging with filter disabled. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    logs_from_file02_begin = log_file_02_begin_marker
    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(logs_from_file02_begin),
        timeout)

    assert match

    verifyLogLevels(LogClients.FILTER_NULL.value, text, 13)


def test_logging_filter_none(boot_with_proxy):
    """ Logging with filtering of level level NONE (all types of messages).

        It is expected in this case that there will be only one entry from the
        client LVL_NONE.

        This one entry is present by exploiting the log API and calling log
        function with the level Debug_LOG_LEVEL_NONE (i.e. calling
        Debug_LOG(Debug_LOG_LEVEL_NONE, "NONE", ...)).

        """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_NONE.value, text, 1)


def test_logging_filter_level_assert(boot_with_proxy):
    """ Logging with filtering of level ASSERT. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_ASSERT.value, text, 5)


def test_logging_filter_level_fatal(boot_with_proxy):
    """ Logging with filtering of level FATAL.

    Please note that LVL_FATAL is expected to log both to consol and file.
    """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_FATAL.value, text,
                    6, LogTargets.CONSOLE_AND_FILE_1)

def test_logging_filter_level_error(boot_with_proxy):
    """ Logging with filtering of level ERROR. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(end_of_demo_marker),
        timeout)

    assert match

    verifyLogLevels(
        LogClients.LVL_ERROR.value,
        text,
        7,
        LogTargets.CONSOLE_ONLY)


def test_logging_filter_level_warning(boot_with_proxy):
    """ Logging with filtering of level WARNING. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_WARNING.value, text, 8)


def test_logging_filter_level_info(boot_with_proxy):
    """ Logging with filtering of level INFO. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_INFO.value, text, 9)


def test_logging_filter_level_debug(boot_with_proxy):
    """ Logging with filtering of level DEBUG. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_DEBUG.value, text, 10)


def test_logging_filter_level_trace(boot_with_proxy):
    """ Logging with filtering of level TRACE. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_TRACE.value, text, 11)


def test_logging_filter_level_custom(boot_with_proxy):
    """ Logging with filtering of level CUSTOM. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_CUSTOM.value, text, 12)

def test_logging_filter_level_max(boot_with_proxy):
    """ Logging with filtering of level MAX. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.LVL_MAX.value, text, 13)

def test_filter_on_client_side_none(boot_with_proxy):
    """ Logging with client's filtering of level level NONE (all types of
        messages).

        It is expected in this case that there will be only one entry from the
        client CL_FILTER_NONE both on the console and in the log file.

        This one entry is present by exploiting the log API and calling log
        function with the level Debug_LOG_LEVEL_NONE (i.e. calling
        Debug_LOG(Debug_LOG_LEVEL_NONE, "NONE", ...)).

        """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_NONE.value, text, 1)


def test_filter_on_client_side_level_assert(boot_with_proxy):
    """ Logging with client's filtering of level ASSERT. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_ASSERT.value, text, 5)


def test_filter_on_client_side_level_fatal(boot_with_proxy):
    """ Logging with client's filtering of level FATAL. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_FATAL.value, text, 6)


def test_filter_on_client_side_level_error(boot_with_proxy):
    """ Logging with client's filtering of level ERROR. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(end_of_demo_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_ERROR.value, text, 7)


def test_filter_on_client_side_level_warning(boot_with_proxy):
    """ Logging with client's filtering of level WARNING. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_WARNIN.value, text, 8)


def test_filter_on_client_side_level_info(boot_with_proxy):
    """ Logging with client's filtering of level INFO. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_INFO.value, text, 9)


def test_filter_on_client_side_level_debug(boot_with_proxy):
    """ Logging with client's filtering of level DEBUG. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_DEBUG.value, text, 10)


def test_filter_on_client_side_level_trace(boot_with_proxy):
    """ Logging with client's filtering of level TRACE. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_TRACE.value, text, 11)


def test_filter_on_client_side_level_custom(boot_with_proxy):
    """ Logging with client's filtering of level CUSTOM. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match

    verifyLogLevels(LogClients.CL_FILTER_CUSTOM.value, text, 12)


def test_log_empty_entry(boot_with_proxy):
    """ Logging empty entry. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(LogMessagesPatterns.EMPTY_MSG.value),
        timeout)

    assert match


def test_log_entry_page_size(boot_with_proxy):
    """ Logging very large entry. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(LogMessagesPatterns.LOREM_IPSUM.value),
        timeout)

    assert match


def test_get_sender_id(boot_with_proxy):
    """ Testing sender id feature

    Every client has its own uniq sender id based on which it can be identify
    even if client has no name assigned.
    """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(
              LogClients.LVL_ASSERT.value
            + LogMessagesPatterns.ASSERT_LVL_MSG.value),
        timeout)

    assert match


def test_logging_via_printf(boot_with_proxy):
    """ Logging via printf function call.

    The client APP_FS uses printf(...) instead of the logging functions.
    """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(
              LogClients.APP_FS.value
            + LogMessagesPatterns.PARTITION_0_CREATED.value),
        timeout)

    assert match


def test_logger_logging(boot_with_proxy):
    """ Logs from the logger itself. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(
              LogClients.LOG_SERVER.value
            + LogMessagesPatterns.LOG_SERVER_INIT_SUCCESS.value),
        timeout)

    assert match


def test_log_format(boot_with_proxy):
    """ Custom log format used. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    expected_pattern = LogClients.LOG_SERVER.value \
                     + r".*CUSTOM_FORMAT" \
                     + LogMessagesPatterns.LOG_SERVER_INIT_SUCCESS.value

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(expected_pattern),
        timeout)

    assert match


def test_different_backends(boot_with_proxy):
    """ Logs are pushed to different logging backends. """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(end_of_demo_marker),
        timeout)

    assert match
    assert re.search(log_file_01_begin_marker, text)

    console_only_entry_pattern = LogClients.LVL_NONE.value
    assert re.search(console_only_entry_pattern, text)


def test_client_logging_to_different_backends(boot_with_proxy):
    """ Test client logging to different backends.

    One client can log to different backends at the same time.
    """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(log_file_02_begin_marker),
        timeout)

    assert match
    assert (2 == len(
        re.findall(
            LogClients.LVL_FATAL.value + LogMessagesPatterns.NONE_LVL_MSG.value,
            text)))

def test_client_sending_ill_formatted_string(boot_with_proxy):
    """ This is a regression test related to SEOS-985

    If a client sends ill formatted string, e.g. 'Debug_LOG_DEBUG("%2F %2F %2Fl
    %3D");' (notice missing arguments), the fault handler shall be trigger
    due to client accessing restricted memory region.

    This test reproduces above case.
    """

    test_run = boot_with_proxy(log_server_demo_name)
    f_out = test_run[1]

    expected_error = "FAULT HANDLER: data fault from sendsIllFormattedString" \
                   + ".sendsIllFormattedString_ready_0000"

    (text, match) = logs.get_match_in_line(
        f_out,
        re.compile(expected_error),
        timeout)

    assert match == expected_error

def verifyLogLevels(
        client,
        logs_dump,
        expected_entries_count,
        targets = LogTargets.CONSOLE_ONLY):

    all_logs = re.split(log_targets_marker, logs_dump)

    log_console_content = all_logs[0]
    verifyLogLevelsForGivenLog(
        log_console_content,
        client,
        expected_entries_count)

    if LogTargets.CONSOLE_ONLY != targets:
        log_console_content = all_logs[targets.value]

        verifyLogLevelsForGivenLog(
            log_console_content,
            client,
            expected_entries_count)


def verifyLogLevelsForGivenLog(log, client, expected_entries_count):

    assert expected_entries_count == log.count(client)

    log_message_patterns = list(LogMessagesPatterns)

    for i in range(expected_entries_count):
        assert re.search(
            ('%s%s' % (client, log_message_patterns[i].value)),
            log)
