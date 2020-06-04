
import pytest, sys
sys.path.append('../common')
import test_parser as parser

TEST_NAME = 'test_cert_lib'

# AUTOGENERATED TEST FUNCTIONS BELOW -------------------------------------------

def test_CertParser_init_pos_0(boot):
    """
    Positive tests for CertParser_init(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot(TEST_NAME), 2, 'test_CertParser_init_pos')

def test_CertParser_init_neg_0(boot):
    """
    Negative tests for CertParser_init(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_init_neg')

def test_CertParser_free_pos_0(boot):
    """
    Positive tests for CertParser_free(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_free_pos')

def test_CertParser_free_neg_0(boot):
    """
    Negative tests for CertParser_free(), covering the invalid ways of using this
    function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_free_neg')

def test_CertParser_Cert_init_pos_0(boot):
    """
    Positive tests for CertParser_Cert_init(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Cert_init_pos')

def test_CertParser_Cert_init_neg_0(boot):
    """
    Negative tests for CertParser_Cert_init(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Cert_init_neg')

def test_CertParser_Cert_free_pos_0(boot):
    """
    Positive tests for CertParser_Cert_free(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Cert_free_pos')

def test_CertParser_Cert_free_neg_0(boot):
    """
    Negative tests for CertParser_Cert_free(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Cert_free_neg')

def test_CertParser_Cert_getAttrib_pos_0(boot):
    """
    Positive tests for CertParser_Cert_getAttrib(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Cert_getAttrib_pos')

def test_CertParser_Cert_getAttrib_neg_0(boot):
    """
    Negative tests for CertParser_Cert_getAttrib(), covering the invalid ways of
    using this function thus verifying that it returns error codes instead of
    crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Cert_getAttrib_neg')

def test_CertParser_Chain_init_pos_0(boot):
    """
    Positive tests for CertParser_Chain_init(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_init_pos')

def test_CertParser_Chain_init_neg_0(boot):
    """
    Negative tests for CertParser_Chain_init(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_init_neg')

def test_CertParser_Chain_free_pos_0(boot):
    """
    Positive tests for CertParser_Chain_free(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_free_pos')

def test_CertParser_Chain_free_neg_0(boot):
    """
    Negative tests for CertParser_Chain_free(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_free_neg')

def test_CertParser_Chain_addCert_pos_0(boot):
    """
    Positive tests for CertParser_Chain_addCert(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_addCert_pos')

def test_CertParser_Chain_addCert_neg_0(boot):
    """
    Negative tests for CertParser_Chain_addCert(), covering the invalid ways of
    using this function thus verifying that it returns error codes instead of
    crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_addCert_neg')

def test_CertParser_Chain_getCert_pos_0(boot):
    """
    Positive tests for CertParser_Chain_getCert(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_getCert_pos')

def test_CertParser_Chain_getCert_neg_0(boot):
    """
    Negative tests for CertParser_Chain_getCert(), covering the invalid ways of
    using this function thus verifying that it returns error codes instead of
    crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_getCert_neg')

def test_CertParser_Chain_getLength_pos_0(boot):
    """
    Positive tests for CertParser_Chain_getLength(), covering the valid ways of
    using this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_getLength_pos')

def test_CertParser_Chain_getLength_neg_0(boot):
    """
    Negative tests for CertParser_Chain_getLength(), covering the invalid ways of
    using this function thus verifying that it returns error codes instead of
    crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_Chain_getLength_neg')

def test_CertParser_addTrustedChain_pos_0(boot):
    """
    Positive tests for CertParser_addTrustedChain(), covering the valid ways of
    using this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_addTrustedChain_pos')

def test_CertParser_addTrustedChain_neg_0(boot):
    """
    Negative tests for CertParser_addTrustedChain(), covering the invalid ways of
    using this function thus verifying that it returns error codes instead of
    crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_addTrustedChain_neg')

def test_CertParser_verifyChain_pos_0(boot):
    """
    Positive tests for CertParser_verifyChain(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_verifyChain_pos')

def test_CertParser_verifyChain_neg_0(boot):
    """
    Negative tests for CertParser_verifyChain(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing
    """
    parser.check_test(boot(TEST_NAME), 1, 'test_CertParser_verifyChain_neg')