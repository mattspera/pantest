# pantest

A Palo Alto Networks test-suite Python library.

## Version Info

- Palo Alto: Tested on PAN-OS 8.0.x, 8.1.x
- Python: Python 3 required

## Python Library Dependencies

- pandevice
- netmiko
- xmltodict

## Overview

This Python library in development facilitates the automation of technical verification testing of Palo Alto Networks devices. The library contains a series of Python methods that each test a component of device configuration or state. Each test method takes a baseline value as an argument and compares this value to the current configuration or state value on the device. Each method will return a test result, including any differences found in the comparative values.

## How to Use

### 1. Compile and install pantest via pip

```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install dist/pantest-0.0.1-py3-none-any.whl
```

### 2. Import pantest into script and call available methods

**Sample script:**

```python
import argparse
import logging
import json
from datetime import datetime
from getpass import getpass

from pantest.testcases import FirewallTestCases

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', help='hostname or ip of Palo Alto device', required=True)
    parser.add_argument('--user', help='username for auth to Palo Alto device', required=True)
    args = parser.parse_args()

    # Lowering paramiko logging level to prevent unnecessary logging in main log file
    logging.getLogger('paramiko').setLevel(logging.WARNING)

    dt = datetime.now().strftime(r'%y%m%d_%H%M')
    logging.basicConfig(filename='{}_{}_tvt.log'.format(args.device, dt), level=logging.INFO)

    device_info = {
        'ip' : args.device,
        'username' : args.user,
        'password' : getpass()
    }

    fw_tester = FirewallTestCases(device_info)

    test_outputs = []

    # Test data

    bl_interfaces_up = ['ethernet1/1', 'ethernet1/2'] # 'ethernet1/1 and 'ethernet1/2' were interfaces up in baseline tvt

    bl_connectivity = {
        "10.0.3.15": "100%",
        "10.0.3.2": "100%",
        "192.168.56.10": "0%"
    }

    test_outputs.append(fw_tester.t_interfaces_up(bl_interfaces_up))
    test_outputs.append(fw_tester.t_connectivity(bl_connectivity))

    for test_res in test_outputs:
        print(json.dumps(test_res, indent=4, default=set_default)) # test_res is a dictionary containing test results

if __name__ == '__main__':
    main()
```

**Sample Script Output:**

```
{
    "name": "t_interfaces_up",
    "result": true
}
{
    "name": "t_connectivity",
    "result": false,
    "info": {
        "added": [],
        "removed": [],
        "changed [baseline, tvt]": {
            "10.0.3.15": [
                "100%",
                "0%"
            ]
        }
    }
}
```
