
import pytest
import test_parser as parser

def test_CertServer_initChain_pos(boot):
    """
    Positive tests for CertServer_initChain(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot(), 3, 'test_CertServer_initChain_pos', 'cid=101')
    parser.check_test(boot(), 3, 'test_CertServer_initChain_pos', 'cid=102')
    parser.check_test(boot(), 3, 'test_CertServer_initChain_pos', 'cid=103')

def test_CertServer_initChain_neg(boot):
    """
    Negative tests for CertServer_initChain(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing.
    """
    parser.check_test(boot(), 3, 'test_CertServer_initChain_neg', 'cid=101')
    parser.check_test(boot(), 3, 'test_CertServer_initChain_neg', 'cid=102')
    parser.check_test(boot(), 3, 'test_CertServer_initChain_neg', 'cid=103')

def test_CertServer_addCertToChain_pos(boot):
    """
    Positive tests for CertServer_addCertToChain(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(), 3, 'test_CertServer_addCertToChain_pos', 'cid=101')
    parser.check_test(boot(), 3, 'test_CertServer_addCertToChain_pos', 'cid=102')
    parser.check_test(boot(), 3, 'test_CertServer_addCertToChain_pos', 'cid=103')

def test_CertServer_addCertToChain_neg(boot):
    """
    Negative tests for CertServer_addCertToChain(), covering the invalid ways of
    using this function thus verifying that it returns error codes instead of
    crashing.
    """
    parser.check_test(boot(), 3, 'test_CertServer_addCertToChain_neg', 'cid=101')
    parser.check_test(boot(), 3, 'test_CertServer_addCertToChain_neg', 'cid=102')
    parser.check_test(boot(), 3, 'test_CertServer_addCertToChain_neg', 'cid=103')

def test_CertServer_verifyChain_pos(boot):
    """
    Positive tests for CertServer_verifyChain(), covering the valid ways of using
    this function.
    """
    parser.check_test(boot(), 3, 'test_CertServer_verifyChain_pos', 'cid=102')
    parser.check_test(boot(), 3, 'test_CertServer_verifyChain_pos', 'cid=101')
    parser.check_test(boot(), 3, 'test_CertServer_verifyChain_pos', 'cid=103')

def test_CertServer_verifyChain_neg(boot):
    """
    Negative tests for CertServer_verifyChain(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing.
    """
    parser.check_test(boot(), 5, 'test_CertServer_verifyChain_neg', 'cid=102')
    parser.check_test(boot(), 5, 'test_CertServer_verifyChain_neg', 'cid=101')
    parser.check_test(boot(), 5, 'test_CertServer_verifyChain_neg', 'cid=103')

def test_CertServer_freeChain_pos(boot):
    """
    Positive tests for CertServer_freeChain(), covering the valid ways of using this
    function.
    """
    parser.check_test(boot(), 3, 'test_CertServer_freeChain_pos', 'cid=102')
    parser.check_test(boot(), 3, 'test_CertServer_freeChain_pos', 'cid=101')
    parser.check_test(boot(), 3, 'test_CertServer_freeChain_pos', 'cid=103')

def test_CertServer_freeChain_neg(boot):
    """
    Negative tests for CertServer_freeChain(), covering the invalid ways of using
    this function thus verifying that it returns error codes instead of crashing.
    """
    parser.check_test(boot(), 3, 'test_CertServer_freeChain_neg', 'cid=102')
    parser.check_test(boot(), 3, 'test_CertServer_freeChain_neg', 'cid=101')
    parser.check_test(boot(), 3, 'test_CertServer_freeChain_neg', 'cid=103')

