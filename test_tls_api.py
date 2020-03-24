import pytest, sys
sys.path.append('../common')
import test_parser as parser

TEST_NAME = 'test_tls_api'

# AUTOGENERATED TEST FUNCTIONS BELOW -------------------------------------------

def test_OS_Tls_init_pos_0(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_init(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 30, 'test_OS_Tls_init_pos')

def test_OS_Tls_init_neg_0(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_init(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_init_neg')

def test_OS_Tls_free_pos_0(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_free(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_free_pos')

def test_OS_Tls_free_neg_0(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_free(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_free_neg')

def test_OS_Tls_handshake_pos_0(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_handshake(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 30, 'test_OS_Tls_handshake_pos', 'mode=1')

def test_OS_Tls_handshake_neg_0(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_handshake(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_handshake_neg', 'mode=1')

def test_OS_Tls_write_neg_0(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_write(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_write_neg', 'mode=1')

def test_OS_Tls_write_pos_0(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_write(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_write_pos', 'mode=1')

def test_OS_Tls_read_neg_0(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_read(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_read_neg', 'mode=1')

def test_OS_Tls_read_pos_0(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_read(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 2, 'test_OS_Tls_read_pos', 'mode=1')

def test_OS_Tls_reset_neg_0(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_reset(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_reset_neg', 'mode=1')

def test_OS_Tls_reset_pos_0(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_reset(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 30, 'test_OS_Tls_reset_pos', 'mode=1')

def test_OS_Tls_handshake_pos_1(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_handshake(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 30, 'test_OS_Tls_handshake_pos', 'mode=3')

def test_OS_Tls_handshake_neg_1(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_handshake(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_handshake_neg', 'mode=3')

def test_OS_Tls_write_neg_1(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_write(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_write_neg', 'mode=3')

def test_OS_Tls_write_pos_1(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_write(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_write_pos', 'mode=3')

def test_OS_Tls_read_neg_1(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_read(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_read_neg', 'mode=3')

def test_OS_Tls_read_pos_1(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_read(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 2, 'test_OS_Tls_read_pos', 'mode=3')

def test_OS_Tls_reset_neg_1(boot_with_proxy, tls_server):
    """
    Negative tests for OS_Tls_reset(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 1, 'test_OS_Tls_reset_neg', 'mode=3')

def test_OS_Tls_reset_pos_1(boot_with_proxy, tls_server):
    """
    Positive tests for OS_Tls_reset(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot_with_proxy(TEST_NAME), 30, 'test_OS_Tls_reset_pos', 'mode=3')

