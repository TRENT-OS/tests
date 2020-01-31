from enum import Enum

timeout     = 90
empty_entry = 1

log_server_demo_name     = "test_logserver"

log_file_01_begin_marker = "log file 01 content:"
log_file_02_begin_marker = "log file 02 content:"
end_of_demo_marker       = "demo finished successfully"
log_targets_marker       = "content:"

class LogClients(Enum):
    LOG_SERVER      = "LOG-SERVER"

    LVL_NONE        = "LVL_NONE"
    LVL_ASSERT      = "000200"
    LVL_FATAL       = "LVL_FATAL"
    LVL_ERROR       = "LVL_ERROR"
    LVL_WARNING     = "LVL_WARNING"
    LVL_INFO        = "LVL_INFO"
    LVL_DEBUG       = "LVL_DEBUG"
    LVL_TRACE       = "LVL_TRACE"
    LVL_CUSTOM      = "LVL_CUSTOM"

    FILTER_NULL     = "FILTER_NULL"

    CL_FILTER_NONE   = "CL_FILTER_NONE"
    CL_FILTER_ASSERT = "CL_FILTER_ASSERT"
    CL_FILTER_FATAL  = "CL_FILTER_FATAL"
    CL_FILTER_ERROR  = "CL_FILTER_ERROR"
    CL_FILTER_WARNIN = "CL_FILTER_WARNIN"
    CL_FILTER_INFO   = "CL_FILTER_INFO"
    CL_FILTER_DEBUG  = "CL_FILTER_DEBUG"
    CL_FILTER_TRACE  = "CL_FILTER_TRACE"
    CL_FILTER_CUSTOM = "CL_FILTER_CUSTOM"

    APP0x           = "APP0x"
    APP_FS          = "APP_FS"

class LogMessagesPatterns(Enum):
    NONE_LVL_MSG    = r".*Debug_LOG_NONE\n"

    EMPTY_MSG   = r".*:\s\n"
    LOREM_IPSUM = r".*Lorem ipsum dol.*rturient purus, nisl viverra pra\.\n"

    ASSERT_LVL_MSG  = r".*Debug_LOG_ASSERT\n"
    FATAL_LVL_MSG   = r".*Debug_LOG_FATAL\n"
    ERROR_LVL_MSG   = r".*Debug_LOG_ERROR\n"
    WARNING_LVL_MSG = r".*Debug_LOG_WARNING\n"
    INFO_LVL_MSG    = r".*Debug_LOG_INFO\n"
    DEBUG_LVL_MSG   = r".*Debug_LOG_DEBUG\n"
    TRACE_LVL_MSG   = r".*Debug_LOG_TRACE\n"
    CUSTOM_LVL_MSG  = r".*Debug_LOG_CUSTOM\n"

    LOG_SERVER_INIT_SUCCESS = r".*=> SUCCESS!\n"
    PARTITION_0_CREATED     = r".*Partition 0 successfully created!"
