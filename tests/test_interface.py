import os
import yaml
import unittest

from pantest.interface import PanApi, PanCli, PanHybrid

def setUpModule():
    working_dir = os.path.dirname(__file__)
    file_path = os.path.join(working_dir, 'etc/responses.yml')

    global expected_responses
    with open(file_path) as file_obj:
        expected_responses = yaml.safe_load(file_obj)

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
        self.assertEqual(expected_responses['hostname'], output['system']['hostname'])

    def test_get_route_table(self):
        output = self.api.get_route_table()
        self.assertTrue(next((entry for entry in output['entry'] if entry['destination'] == expected_responses['test_route_dest'])), None)

    def test_get_route_interface(self):
        output = self.api.get_route_interface()
        self.assertTrue(next((i for i in output['interface'] if i['name'] == expected_responses['host_only_route_int'])), None)

    def test_get_system_environmentals(self):
        pass

    def test_get_ntp(self):
        output = self.api.get_ntp()
        self.assertEqual(expected_responses['ntp_status'], output['synched'])

    def test_get_panorama_status(self):
        pass

    def test_get_interface_hardware(self):
        output = self.api.get_interface_hardware()
        self.assertTrue(next((i for i in output['hw']['entry'] if i['mac'] == expected_responses['interface_mac'])), None)

class TestPanCli(unittest.TestCase):

    def setUp(self):
        self.cli = PanCli(device_info)

    def test_run_cmd(self):
        output = self.cli.run_cmd('show admins')
        self.assertIn('Session-start', output)

    def test_enter_config_mode(self):
        output = self.cli.enter_config_mode()
        self.assertIn(expected_responses['config_mode_prompt'], output)

    def tearDown(self):
        del self.cli

class TestPanHybrid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_cli = PanHybrid(device_info)

    def test_get_connectivity(self):
        output = self.api_cli.get_connectivity()
        self.assertEqual(expected_responses['packet_loss'], output['192.168.56.2'])

if __name__ == "__main__":
    unittest.main()
