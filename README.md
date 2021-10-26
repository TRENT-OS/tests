# seos_tests test automation scripts

Test Automation scripts for the seos_tests project.

## Cppcheck

The usage of the cppcheck/check_static_analyzer.sh script is described within
the script.

## Pytest

Each of the scripts in this repository is designed to parse the output of the
test systems for different TRENTOS-M components or libraries and determine the
result (success/failure). The scripts are to be used within the seos\_tests
project and run with the `test.sh` script as follows:

```bash
cd seos_tests

# Prepare the test tools, it's a lightweight SDK build. Needs to be done only
# once.
src/seos_sandbox/scripts/open_trentos_build_env.sh src/test.sh prepare

# Run the test in QEMU.
src/seos_sandbox/scripts/open_trentos_test_env.sh \
src/test.sh run test_demo_hello_world.py
```

### Dependencies

* python
* see requirements.txt
