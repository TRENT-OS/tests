#
# Copyright (C) 2019-2023, HENSOLDT Cyber GmbH
#

import os
import re
import pytest
import logs # logs module from the common directory in TA


#-------------------------------------------------------------------------------
def test_run_demo(boot_with_proxy):
    """ This demo utilizes both the partition manager and the filesystem as a
    component and makes use of all relevant TRENTOS Filesystem API functions. """

    proxy_memory_file = "nvm_06"
    if os.path.isfile(proxy_memory_file):
        os.remove(proxy_memory_file)
    with  open(proxy_memory_file,"wb") as f:
        # create 36 MiB NVM file. The size comes from the partition sizes that
        # are defined in the define TRENTOS system config file. One day we
        # should extend things, so the TRENTOS system can request the proxy to
        # create a NVM of a given size and that is can quesry the currenty NVM
        # size and fail if this is too small. For now, we have to sync the value
        # here with the TRENTOS system manually.
        f.seek( (36*1024*1024) -1 )
        f.write(b"\0")

    test_runner = boot_with_proxy('demo_fs_as_components')

    (text, match) = logs.get_match_in_line(
                        test_runner.get_system_log(),
                        re.compile('# end #'),
                        30)
    assert match == success_msg
