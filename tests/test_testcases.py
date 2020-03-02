import os
import yaml
import unittest

from pantest.testcases import PanoramaTestCases, FirewallTestCases, GeneralTestCases

def setUpModule():
    working_dir = os.path.dirname(__file__)
    file_path = os.path.join(working_dir, 'etc/test_vars.yml')

    global test_vars
    with open(file_path) as file_obj:
        test_vars = yaml.safe_load(file_obj)

    global device_info
    device_info = {
        'ip' : os.environ.get('TEST_IP'),
        'username' : os.environ.get('TEST_USERNAME'),
        'password' : os.environ.get('TEST_PASSWORD')
    }

class TestPanoramaTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

class TestFirewallTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fw_tester = FirewallTestCases(device_info)

    def test_t_system_env_alarms_fw(self):
        pass

    def test_t_connectivity(self):
        output_1 = self.fw_tester.t_connectivity(test_vars['nexthop_pings'])
        output_2 = self.fw_tester.t_connectivity(test_vars['not_nexthop_pings'])
        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])
        self.assertEqual(test_vars['removed_nexthop'], next(iter(output_2['info']['removed'])))
        self.assertIn(test_vars['changed_nexthop'], output_2['info']['changed [baseline, tvt]'])
        self.assertEqual(test_vars['packet_loss'], output_2['info']['changed [baseline, tvt]'][test_vars['changed_nexthop']][1])
        self.assertEqual(test_vars['not_packet_loss'], output_2['info']['changed [baseline, tvt]'][test_vars['changed_nexthop']][0])

    def test_t_panorama_connected(self):
        pass

    def test_t_ha_peer_up(self):
        output_1 = self.fw_tester.t_ha_peer_up(test_vars['ha_peer_up_status'])
        output_2 = self.fw_tester.t_ha_peer_up(test_vars['not_ha_peer_up_status'])
        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])
        self.assertEqual(test_vars['ha1_status'], output_2['info']['ha1-link-status'])
        self.assertEqual(test_vars['ha2_status'], output_2['info']['ha2-link-status'])   

    def test_t_ha_match(self):
        pass

    def test_t_ha_config_synced(self):
        output_1 = self.fw_tester.t_ha_config_synced(test_vars['ha_config_sync_status'])
        output_2 = self.fw_tester.t_ha_config_synced(test_vars['not_ha_config_sync_status'])
        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])
        self.assertEqual(test_vars['ha_config_sync_status'], output_2['info']['ha-config-sync-status'])

    def test_t_interfaces_up(self):
        output_1 = self.fw_tester.t_interfaces_up(test_vars['interfaces_up'])
        output_2 = self.fw_tester.t_interfaces_up(test_vars['not_interfaces_up'])
        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])
        self.assertEqual(output_2['info']['interfaces-down'][0], test_vars['not_interfaces_up'][2])

    def test_t_traffic_log_forward(self):
        pass

class TestGeneralTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gen_tester = GeneralTestCases(device_info)

    def test_t_system_version(self):
        output_1 = self.gen_tester.t_system_version(test_vars['sys_version'])
        output_2 = self.gen_tester.t_system_version(test_vars['not_sys_version'])
        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])
        self.assertEqual(output_2['info']['current-sw-version'], test_vars['sys_version'])
        self.assertEqual(output_2['info']['target-sw-version'], test_vars['not_sys_version'])

    def test_t_config_diff(self):
        working_dir = os.path.dirname(__file__)

        file_path_1 = os.path.join(working_dir, test_vars['config_set'])

        with open(file_path_1, 'r') as file_obj:
            config_set_list = file_obj.read().splitlines()
            output_1 = self.gen_tester.t_config_diff(config_set_list)

        file_path_2 = os.path.join(working_dir, test_vars['not_config_set'])

        with open(file_path_2, 'r') as file_obj:
            config_set_list = file_obj.read().splitlines()
            output_2 = self.gen_tester.t_config_diff(config_set_list)

        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])
        self.assertListEqual(test_vars['removed_config'], output_2['info']['config-changes']['removed'])
        self.assertListEqual(test_vars['added_config'], output_2['info']['config-changes']['added'])          


    def test_t_ha_enabled(self):
        output_1 = self.gen_tester.t_ha_enabled(test_vars['ha_enabled_status'])
        output_2 = self.gen_tester.t_ha_enabled(test_vars['not_ha_enabled_status'])
        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])

    def test_t_ntp_synced(self):
        output_1 = self.gen_tester.t_ntp_synced(test_vars['ntp_status'])
        output_2 = self.gen_tester.t_ntp_synced(test_vars['not_ntp_status'])
        self.assertTrue(output_1['result'])
        self.assertFalse(output_2['result'])

if __name__ == "__main__":
    unittest.main()