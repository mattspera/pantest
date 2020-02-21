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

Todo...

## How to Use

1. **Compile and install pantest via pip**

```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install dist/pantest-0.0.1-py3-none-any.whl
```

2. **Import pantest into script and call available methods**

Sample script:

```python
from getpass import getpass

from pandevice.base import PanDevice
from pandevice.errors import PanDeviceError
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException

from pantest.testcases import GeneralTestCases
from pantest.testcases import FirewallTestCases
from pantest.testcases import PanoramaTestCases

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', help='hostname or ip of Palo Alto device', required=True)
    parser.add_argument('--user', help='username for auth to Palo Alto device', required=True)
    args = parser.parse_args()

    password = getpass()

    try:
        device = PanDevice.create_from_device(args.device, args.user, password)
    except PanDeviceError as e:
        print(e.message)

    auth = {
        'device_type' : 'paloalto_panos',
        'ip' : args.device,
        'username' : args.user,
        'password' : password
    }

    try:
        conn = ConnectHandler(**auth)
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(e.message)

    fw_tester = FirewallTestCases(device, conn)

    test_output = fw_tester.t_panorama_connected('yes')

    print(test_output) # test_output is a dictionary

if __name__ == '__main__':
    main()
```
