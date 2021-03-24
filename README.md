# seos_tests test automation scripts

Test Automation scripts for the seos_tests project.

## Cppcheck

The usage of the cppcheck/check_static_analyzer.sh script is described within the script.

## Pytest

The usage of python virtual environments is suggested to avoid collisions when installing the requirements.

* pip install -r requirements.txt
* pytest -v -s --workspace_path="absolute_path_to_seos_tests" --proxy_path="absolute_path_to_proxy_app"

The proxy_app is the proxy application that communicates (via QEMU UART) with the test applications provided by seos_tests. The proxy application runs on Linux and certain provides facilities (e.g.: inter-networking).

### Dependencies

* python
* see requirements.txt
