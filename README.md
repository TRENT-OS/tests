# seos\_tests test automation scripts

Pytest Test Automation scripts for the seos\_tests project

## Getting Started

The usage of python virtual environments is suggest to avoid collision when installing the requirements

* pip install -r requirements.txt
* pytest -v -s --workspace\_path="absolute\_path\_to\_seos\_tests" --proxy\_path="absolute\_path\_to\_seos\_proxy\_app"

The seos\_proxy\_app is the proxy application that communicates (via qemu UART) with the SeOS test applications provided by seos\_tests. The proxy application runs on Linux and provide facilities to SeOS (e.g.: internetworking)

### Dependencies

* python
* see requirements.txt


