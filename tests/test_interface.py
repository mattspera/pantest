import os
import sys
import yaml
import unittest

from pantest.interface import PanApi, PanCli, PanHybrid

def setUpModule():
    working_dir = os.path.dirname(__file__)
    file_path = os.path.join(working_dir, 'etc/test_vars.yml')

    global test_vars
    with open(file_path) as file_obj:
        test_vars = yaml.safe_load(file_obj)

    try:
        assert all(os.environ[env] for env in ['TEST_USERNAME', 'TEST_PASSWORD', 'TEST_IP'])
    except KeyError as exc:
        sys.exit(f"ERROR: Missing env variable: {exc}")

    global device_info
    device_info = {
        'ip' : os.environ.get('TEST_IP'),
        'username' : os.environ.get('TEST_USERNAME'),
        'password' : os.environ.get('TEST_PASSWORD')
    }

class TestPanApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = PanApi(device_info)

    def test_get_system_info(self):
        output = self.api.get_system_info()
        self.assertEqual(test_vars['hostname'], output['system']['hostname'])

    def test_get_route_table(self):
        output = self.api.get_route_table()
        self.assertTrue(next((entry for entry in output['entry'] if entry['destination'] == test_vars['test_route_dest'])), None)

    def test_get_route_interface(self):
        output = self.api.get_route_interface()
        self.assertTrue(next((i for i in output['interface'] if i['name'] == test_vars['host_only_route_int'])), None)

    def test_get_system_environmentals(self):
        pass

    def test_get_ntp(self):
        output = self.api.get_ntp()
        self.assertEqual(test_vars['ntp_status'], output['synched'])

    def test_get_panorama_status(self):
        pass

    def test_get_ha_status(self):
        output = self.api.get_ha_status()
        self.assertEqual(test_vars['ha_enabled_status'], output['enabled'])

    def test_get_interface_hardware(self):
        output = self.api.get_interface_hardware()
        self.assertTrue(next((i for i in output['hw']['entry'] if i['mac'] == test_vars['interface_mac'])), None)

class TestPanCli(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cli = PanCli(device_info)

    def test_run_cmd(self):
        output = self.cli.run_cmd('show admins')
        self.assertIn('Session-start', output)

    def test_enter_config_mode(self):
        output = self.cli.enter_config_mode()
        self.cli.exit_config_mode()
        self.assertIn(test_vars['config_mode_prompt'], output)

    def test_exit_config_mode(self):
        self.cli.enter_config_mode()
        output = self.cli.exit_config_mode()
        self.assertIn(test_vars['op_mode_prompt'], output)

class TestPanHybrid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_cli = PanHybrid(device_info)

    def test_get_connectivity(self):
        output = self.api_cli.get_connectivity()
        self.assertEqual(test_vars['packet_loss'], output[test_vars['changed_nexthop']])

if __name__ == "__main__":
    unittest.main()
