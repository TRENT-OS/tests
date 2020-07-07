import pytest
import sys
import os
import re
import logs # logs module from the common directory in TA

def test_run_demo(boot_with_proxy):
    """ This demo utilizes both the partition manager and the filesystem as component and makes use of all relevant SEOS Filesystem API functions. """
    proxy_memory_file = "nvm_06"
    if os.path.isfile(proxy_memory_file):
        os.remove(proxy_memory_file)
    with  open(proxy_memory_file,"wb") as f:
        # create 36 MiB NVM file. The size comes from the partition sizes that
        # are defined in the define SEOS system config file. One day we should
        # extend things, so the SEOS system can request the proxy to create a
        # NVM of a given size and that is can quesry the currenty NVM size and
        # fail if this is too small. For now, we have to sync the value here
        # with the SEOSM system manually.
        f.seek( (36*1024*1024) -1 )
        f.write(b"\0")

    test_run = boot_with_proxy("demo_fs_as_components")
    f_out = test_run[1]

    success_msg = "# end #"
    timeout = 30
    (text, match) = logs.get_match_in_line(f_out, re.compile(success_msg), timeout)
    assert match == success_msg
