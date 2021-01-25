from scapy.all import *
import socket
import logs # logs module from the common directory in TA
import pytest
from http.server import BaseHTTPRequestHandler, HTTPServer
import shutil
import pathlib
import sys
import socketserver
import threading
import os
import tests

# This python file is imported by pydoc which sometimes throws an error about a
# missing IPv6 default route (if the machine building the documentation doesn't
# have it set). To remove this warning we disable IPv6 support in scapy, since
# we don't use it at this time.
from scapy.config import conf
conf.ipv6_enabled = False

test_system = None
TEST_TIMEOUT = 10

# This indicates the folder which consists of TUF metadata files created for a
# specific test case
current_test_files_dir = "test_folder"

def get_requested_filepath(path):
    foldername = pathlib.PurePath(__file__)

    # PurePath(path).name is used as path is of the format
    # "/<requested_file>.bin"
    filename = pathlib.PurePath(
                    foldername.parent,
                    (pathlib.Path(__file__)).stem,
                    current_test_files_dir,
                    pathlib.PurePath(path).name)

    return filename

class HandlerClass(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'bin')
        self.end_headers()

    def do_GET(self):
        self._set_response()

        try:
            file = open(get_requested_filepath(self.path),'rb')
            self.wfile.write(file.read())
        except:
            self.wfile.write('File missing :'.encode('utf-8'))
            self.wfile.write(self.path.encode('utf-8'))

def startServer(server_class=HTTPServer, handler_class=HandlerClass, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except:
        print("Exception occurred!!!")
    httpd.server_close()

@pytest.fixture(scope="module")
def startDaemon(request):
    #start the server in a seperate thread
    daemon = threading.Thread(name='daemon',target=startServer,daemon=True)
    daemon.start()
    def fin():
        print("teardown httpd")
        daemon.killed = True
    request.addfinalizer(fin)

def test_newRootFileMissing_pos(boot_with_proxy, startDaemon):
    """
    Checks if the device requests the next version of root metadata until it
    reads File missing from the server.
    """
    global current_test_files_dir
    current_test_files_dir = "newRootFileMissing"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                    ['Requested file is missing in the server',
                                    'OS_SecureUpdate_getFile with err -8',
                                    'New root file not present'],
                                    20)

def test_successfulUpdate_pos(boot_with_proxy):
    """
    Checks if the firmware update process is successful.
    """
    global current_test_files_dir
    current_test_files_dir = "successfulUpdate"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                      ['In function verifyImage',
                                      'Hash equal',
                                      'In function storeImage'],
                                      20)

def test_oldRootMetadata_neg(boot_with_proxy):
    """
    Checks if older versions of root metadata are rejected by the device.
    """
    global current_test_files_dir
    current_test_files_dir = "oldRootMetadata"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                        ['New root metadata version is old. Abort update!!',
                        'Invalid new root.bin!! Abort update!!',
                        'State SET_TRUSTED_ROOT_FILE failed with an error -5'],
                        20)

def test_rootSignatureFailure_neg(boot_with_proxy):
    """
    Checks if the device rejects root metadata with invalid signature.
    """
    global current_test_files_dir
    current_test_files_dir = "rootSignatureFailure"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['OS_CryptoSignature_verify() failed with -11',
                                'verifySignature() failed with -11',
                                'root checkSignature failed with -11',
                                'Invalid new root.bin!! Abort update!!'],
                                20)

def test_rootTypeMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects root metadata with invalid type.
    """
    global current_test_files_dir
    current_test_files_dir = "rootTypeMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                        ['root file type mismatch!!',
                        'Invalid new root.bin!! Abort update!!',
                        'State SET_TRUSTED_ROOT_FILE failed with an error -5'],
                        20)

def test_rootMetadataExpires_neg(boot_with_proxy):
    """
    Checks if the device rejects root metadata which is expired.
    """
    global current_test_files_dir
    current_test_files_dir = "rootMetadataExpires"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                        ['root file validity has expired!!',
                        'Invalid new root.bin!! Abort update!!',
                        'State SET_TRUSTED_ROOT_FILE failed with an error -4'],
                        20)

def test_unsupportedSignatureScheme_neg(boot_with_proxy):
    """
    Checks if the device rejects root metadata with unsupported signature
    scheme.
    """
    global current_test_files_dir
    current_test_files_dir = "unsupportedSignatureScheme"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                        ['Unsupported signature scheme. Abort update!!',
                        'Invalid new root.bin!! Abort update!!',
                        'State SET_TRUSTED_ROOT_FILE failed with an error -3'],
                        20)

def test_unsupportedKeyType_neg(boot_with_proxy):
    """
    Checks if the device rejects root metadata which is unsupported key type.
    """
    global current_test_files_dir
    current_test_files_dir = "unsupportedKeyType"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                        ['Unsupported key type. Abort update!!',
                        'Invalid new root.bin!! Abort update!!',
                        'State SET_TRUSTED_ROOT_FILE failed with an error -3'],
                        20)

def test_timestampSignatureFailure_neg(boot_with_proxy):
    """
    Checks if the device rejects timestamp metadata with invalid signature.
    """
    global current_test_files_dir
    current_test_files_dir = "timestampSignatureFailure"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['verifySignature() failed with -11',
                            'timestamp checkSignature failed with -11',
                            'State PROCESS_TIMESTAMP failed with an error -11'],
                            20)

def test_timestampMetadataExpired_neg(boot_with_proxy):
    """
    Checks if the device rejects timestamp metadata which is expired.
    """
    global current_test_files_dir
    current_test_files_dir = "timestampMetadataExpired"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['timestamp file validity has expired!!',
                            'State PROCESS_TIMESTAMP failed with an error -4'],
                            20)

def test_timestampTypeMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects timestamp metadata with invalid type.
    """
    global current_test_files_dir
    current_test_files_dir = "timestampTypeMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['timestamp file type mismatch!!',
                            'State PROCESS_TIMESTAMP failed with an error -5'],
                            20)

def test_snapshotVersionOutdatedinTimestamp_neg(boot_with_proxy):
    """
    Checks if the device rejects timestamp metadata with older snapshot version.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotVersionOutdatedinTimestamp"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['Snapshot version is old. Abort update!!',
                            'State PROCESS_TIMESTAMP failed with an error -5'],
                            20)

def test_timestampVersionOld_neg(boot_with_proxy):
    """
    Checks if the device rejects timestamp metadata which is expired.
    """
    global current_test_files_dir
    current_test_files_dir = "timestampVersionOld"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                        ['Timestamp metadata version is old. Abort update!!',
                        'State PROCESS_TIMESTAMP failed with an error -5'],
                        20)

def test_timestampSpecVersionMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects timestamp metadata with a different TUF
    version.
    """
    global current_test_files_dir
    current_test_files_dir = "timestampSpecVersionMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['timestamp TUF spec version mismatch!!',
                            'State PROCESS_TIMESTAMP failed with an error -5'],
                            20)

def test_snapshotVersionOld_neg(boot_with_proxy):
    """
    Checks if the device rejects snapshot metadata with older version.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotVersionOld"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['Received snapshot version is old',
                            'State PROCESS_SNAPSHOT failed with an error -5'],
                            20)

def test_snapshotFileTypeMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects snapshot metadata with invalid type.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotFileTypeMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['snapshot file type mismatch!!',
                            'State PROCESS_SNAPSHOT failed with an error -5'],
                            20)

def test_SnapshotHashMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects snapshot metadata with a hash different to what
    is indicated in the timestamp metadata.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotHashMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['Snapshot hash mismatch!!',
                            'State PROCESS_SNAPSHOT failed with an error -5'],
                            20)

def test_snapshotSignatureMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects snapshot metadata with invalid signature.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotSignatureMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['verifySignature() failed with -11',
                            'snapshot checkSignature failed with -11',
                            'State PROCESS_SNAPSHOT failed with an error -11'],
                            20)

def test_snapshotLenMismatch_neg(boot_with_proxy, startDaemon):
    """
    Checks if the device rejects snapshot metadata with length different to what
    is indicated in timestamp metadata.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotLenMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['Snapshot file size mismatch!!',
                            'State PROCESS_SNAPSHOT failed with an error -5'],
                            20)

def test_snapshotTUFSpecMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects snapshot metadata with a different TUF
    specification.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotTUFSpecMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['snapshot TUF spec version mismatch!!',
                            'State PROCESS_SNAPSHOT failed with an error -5'],
                            20)

def test_snapshotMetadatExpired_neg(boot_with_proxy):
    """
    Checks if the device rejects snapshot metadata which is expired.
    """
    global current_test_files_dir
    current_test_files_dir = "snapshotMetadatExpired"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['snapshot file validity has expired!!',
                            'State PROCESS_SNAPSHOT failed with an error -4'],
                            20)

def test_targetVersionInSnapshotOutdated_neg(boot_with_proxy):
    """
    Checks if the device rejects snapshot metadata with older target version.
    """
    global current_test_files_dir
    current_test_files_dir = "targetVersionInSnapshotOutdated"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['Target metadata version is outdated',
                            'State PROCESS_SNAPSHOT failed with an error -5'],
                            20)

def test_targetMetadataSignatureInvalid_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata with invalid signature.
    """
    global current_test_files_dir
    current_test_files_dir = "targetMetadataSignatureInvali"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                            ['targets checkSignature failed with -11',
                            'State PROCESS_TARGET failed with an error -11'],
                            20)

def test_firmwareRollback_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata with older firmware version.
    """
    global current_test_files_dir
    current_test_files_dir = "firmwareRollback"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['Firmware rollback!!',
                                'State PROCESS_TARGET failed with an error -5'],
                                20)

def test_targetMetadataExpired_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata which is expired.
    """
    global current_test_files_dir
    current_test_files_dir = "targetMetadataExpired"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['targets file validity has expired!!',
                                'State PROCESS_TARGET failed with an error -4'],
                                20)

def test_targetTypeMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata with invalid type.
    """
    global current_test_files_dir
    current_test_files_dir = "targetTypeMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['targets file type mismatch!!',
                                'State PROCESS_TARGET failed with an error -5'],
                                20)

def test_targetMetadataTUFSpecMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata with a different TUF
    specification.
    """
    global current_test_files_dir
    current_test_files_dir = "targetMetadataTUFSpecMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['targets TUF spec version mismatch!!',
                                'State PROCESS_TARGET failed with an error -5'],
                                20)

def test_firmwareVendorMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata with a different firmware
    vendor.
    """
    global current_test_files_dir
    current_test_files_dir = "firmwareVendorMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['Firmware vendor mismatch!!',
                                'State PROCESS_TARGET failed with an error -5'],
                                20)

def test_firmwareDeviceClassMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata with a different device class.
    """
    global current_test_files_dir
    current_test_files_dir = "firmwareDeviceClassMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['Firmware device class mismatch!!',
                                'State PROCESS_TARGET failed with an error -5'],
                                20)

def test_targetMetadataOlder_neg(boot_with_proxy):
    """
    Checks if the device rejects target metadata with older version.
    """
    global current_test_files_dir
    current_test_files_dir = "targetMetadataOlder"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['Received target metadata is older!!',
                                'State PROCESS_TARGET failed with an error -5'],
                                20)

def test_imageLengthMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects image whose length is different to what is
    indicated in the target metadata.
    """
    global current_test_files_dir
    current_test_files_dir = "imageLengthMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['Image length mismatch',
                                'State VERIFY_IMAGE failed with an error -5'],
                                20)

def test_imageHashMismatch_neg(boot_with_proxy):
    """
    Checks if the device rejects image whose hash is different to what is
    indicated in the target metadata.
    """
    global current_test_files_dir
    current_test_files_dir = "imageHashMismatch"
    tests.run_test_log_match_sequence(boot_with_proxy,test_system,
                                ['In function verifyImage',
                                'Hash not equal',
                                'State VERIFY_IMAGE failed with an error -5'],
                                20)
