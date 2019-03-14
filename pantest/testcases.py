import logging
import ast
import time

from pantest.utils import *
from pantest.interface import PanApi, PanCli, PanHybrid

'''
Panorama-ONLY Tests
'''
class PanoramaTestCases(object):

    def __init__(self, pandevice_obj):
        self.api = PanApi(pandevice_obj)

    def t_shared_policy_sync(self, test):
        test_name = 't_shared_policy_sync'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        device_groups = self.api.get_device_groups()

        shared_policy_sync_dict = {}
        for dg in device_groups['entry']:
            if 'devices' in dg:
                shared_policy_sync_dict[dg['@name']] = {}
                if isinstance(dg['devices']['entry'], dict): # One device within device group - dict
                    shared_policy_sync_dict[dg['@name']].update(
                            {
                               dg['devices']['entry']['hostname'] : {
                                   dg['devices']['entry']['vsys']['entry']['@name'] : dg['devices']['entry']['vsys']['entry']['shared-policy-status']
                                }
                            }
                        )
                else: # many devices within device group - list
                    for dg_dev in dg['devices']['entry']:
                        if dg_dev['connected'] == 'yes':
                            shared_policy_sync_dict[dg['@name']].update(
                                {
                                    dg_dev['hostname'] : {
                                        dg_dev['vsys']['entry']['@name'] : dg_dev['vsys']['entry']['shared-policy-status']
                                    }
                                }
                            )

        # If test is a string (will be if input variable sourced from Ansible module), convert to a dict
        if isinstance(test, str):
            test = ast.literal_eval(test)

        output = compare_dict(test, shared_policy_sync_dict)

        if not output['added'] and not output['removed'] and not output['changed [baseline, tvt]']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'dg-shared-policy-sync-change' : output
            }
            return result

    def t_template_sync(self, test):
        test_name = 't_template_sync'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        templates = self.api.get_templates()

        template_sync_dict = {}
        for t in templates['entry']:
            if 'devices' in t:
                template_sync_dict[t['@name']] = {}
                if isinstance(t['devices']['entry'], dict): # one device within template - dict
                    template_sync_dict[t['@name']].update(
                        {
                            t['devices']['entry']['serial'] :t['devices']['entry']['template-status']
                        }
                    )
                else: # many devices within template - list
                    for t_dev in t['devices']['entry']:
                        template_sync_dict[t['@name']].update(
                            {
                                t_dev['serial'] : t_dev['template-status']
                            }
                        )

        # If test is a string (will be if input variable sourced from Ansible module), convert to a dict
        if isinstance(test, str):
            test = ast.literal_eval(test)

        output = compare_dict(test, template_sync_dict)

        if not output['added'] and not output['removed'] and not output['changed [baseline, tvt]']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'template-sync-change' : output
            }
            return result

    def t_devices_connected(self, test):
        test_name = 't_devices_connected'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        connected_devices = self.api.get_devices_connected()

        dev_conn_list = []
        if 'devices' in connected_devices: # connected devices found
            conn_devs = connected_devices['devices']['entry']
            if isinstance(conn_devs, dict): # one connected device found - dict
                dev_conn_list.append(conn_devs['hostname'])
            else: # many connected devices found - list
                for conn_dev in conn_devs:
                    dev_conn_list.append(conn_dev['hostname'])

        output = compare_list(test, dev_conn_list)

        if not output['added'] and not output['removed']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'devices-connected-change' : output
            }
            return result

    def t_log_collectors_connected(self, test):
        test_name = 't_log_collectors_connected'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        connected_log_collectors = self.api.get_log_collectors_connected()

        conn_lc_list = []
        if 'log-collector' in connected_log_collectors: # connected log collectors found
            conn_lcs = connected_log_collectors['log-collector']['entry']
            if isinstance(conn_lcs, dict): # one connected log collector found - dict
                conn_lc_list.append(conn_lcs['host-name'])
            else: # may connected log collectors found - list
                for conn_lc in conn_lcs:
                    conn_lc_list.append(conn_lc['host-name'])

        output = compare_list(test, conn_lc_list)

        if not output['added'] and not output['removed']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'log-collectors-connected-change' : output
            }
            return result

    def t_wf_appliances_connected(self, test):
        test_name = 't_wf_appliances_connected'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        connected_wf_appliances = self.api.get_wf_appliances_connected()

        conn_wf_list = []
        if 'wildfire-appliances' in connected_wf_appliances: # connected wf appliances found
            conn_wf_apps = connected_wf_appliances['wildfire-appliances']['entry']
            if isinstance(conn_wf_apps, dict): # one connected wf appliance found - dict
                conn_wf_list.append(conn_wf_apps['hostname'])
            else: # may connected wf appliance found - list
                for conn_wf_app in conn_wf_apps:
                    conn_wf_list.append(conn_wf_app['hostname'])

        output = compare_list(test, conn_wf_list)

        if not output['added'] and not output['removed']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'wildfire-appliances-connected-change' : output
            }
            return result

    def t_log_collector_config_sync(self, test):
        test_name = 't_log_collector_config_sync'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        connected_log_collectors = self.api.get_log_collectors_connected()

        lc_config_sync_dict = {}
        if 'log-collector' in connected_log_collectors: # connected log collectors found
            conn_lcs = connected_log_collectors['log-collector']['entry']
            if isinstance(conn_lcs, dict): # one connected log collector found - dict
                lc_config_sync_dict[conn_lcs['host-name']] = conn_lcs['config-status']
            else: # many connected log collectors found - list
                for conn_lc in conn_lcs:
                    lc_config_sync_dict[conn_lc['host-name']] = conn_lc['config-status']

        # If test is a string (will be if input variable sourced from Ansible module), convert to a dict
        if isinstance(test, str):
            test = ast.literal_eval(test)

        output = compare_dict(test, lc_config_sync_dict)

        if not output['added'] and not output['removed'] and not output['changed [baseline, tvt]']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'log-collector-config-sync-change' : output
            }
            return result

    def t_wf_appliance_config_sync(self, test):
        test_name = 't_wf_appliance_config_sync'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        connected_wf_appliances = self.api.get_wf_appliances_connected()

        wf_config_sync_dict = []
        if 'wildfire-appliances' in connected_wf_appliances: # connected wf appliances found
            conn_wf_apps = connected_wf_appliances['wildfire-appliances']['entry']
            if isinstance(conn_wf_apps, dict): # one connected wf appliance found - dict
                wf_config_sync_dict[conn_wf_apps['hostname']] = conn_wf_apps['config-state']
            else: # may connected wf appliance found - list
                for conn_wf_app in conn_wf_apps:
                    wf_config_sync_dict[conn_wf_app['hostname']] = conn_wf_app['config-state']

        # If test is a string (will be if input variable sourced from Ansible module), convert to a dict
        if isinstance(test, str):
            test = ast.literal_eval(test)

        output = compare_dict(test, wf_config_sync_dict)

        if not output['added'] and not output['removed'] and not output['changed [baseline, tvt]']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'wf-appliance-config-sync-change' : output
            }
            return result

    def t_ha_peer_up_pano(self, test):
        test_name = 't_ha_peer_up_pano'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ha_status()
        info = output['peer-info']

        if info['conn-status'] == test:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'ha-peer-status' : info['conn-status']
            }
            return result

    def t_ha_match_pano(self, test):
        test_name = 't_ha_peer_up_pano'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ha_status()
        info = output['local-info']
        compare_dict = {
            'app-version' : info['app-compat'],
            'av-version' : info['av-compat']
        }

        compat_fail_dict = {}
        for k, v in compare_dict.items():
            if v != test and test == 'Match':
                compat_fail_dict[k] = v

        if not compat_fail_dict:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'baseline' : test,
                'ha-version-match-changes' :  compat_fail_dict
            }
            return result

    def t_ha_config_synched_pano(self, test):
        test_name = 't_ha_config_synched_pano'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ha_status()

        if output['running-sync'] == test:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'ha-config-sync-status' : output['running-sync']
            }
            return result

    def t_system_env_alarms_pano(self, test):
        test_name = 't_system_env_alarms_pano'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_system_environmentals()

        envs = [
            output['thermal']['Slot0']['entry'],
            output['fan']['Slot0']['entry'],
            output['power']['Slot0']['entry'],
        ]

        env_alarm_fail_dict = {}
        for item in envs:
            for entry in item:
                if not entry['alarm'] == test:
                    env_alarm_fail_dict[entry['description']] = entry['alarm']

        if not env_alarm_fail_dict:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = env_alarm_fail_dict
            return result

'''
Firewall-ONly Tests
'''
class FirewallTestCases(object):

    def __init__(self, pandevice_obj, netmiko_obj):
        self.api = PanApi(pandevice_obj)
        self.cli = PanCli(netmiko_obj)
        self.api_cli = PanHybrid(pandevice_obj, netmiko_obj)

    def t_system_env_alarms_fw(self, test):
        test_name = 't_system_env_alarms_fw'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_system_environmentals()

        envs = [
            output['thermal']['Slot1']['entry'],
            output['fan']['Slot1']['entry'],
            output['power']['Slot1']['entry'],
            output['power-supply']['Slot1']['entry']
        ]

        env_alarm_fail_dict = {}
        for item in envs:
            for entry in item:
                if not entry['alarm'] == test:
                    env_alarm_fail_dict[entry['description']] = entry['alarm']

        if not env_alarm_fail_dict:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = env_alarm_fail_dict
            return result

    def t_connectivity(self, test):
        test_name = 't_connectivity'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        tvt_connectivity = self.api_cli.get_connectivity()

        # If test is a string (will be if input variable sourced from Ansible module), convert to a dict
        if isinstance(test, str):
            test = ast.literal_eval(test)

        output = compare_dict(test, tvt_connectivity)

        if not output['added'] and not output['removed'] and not output['changed [baseline, tvt]']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = output
            return result

    def t_panorama_connected(self, test):
        test_name = 't_panorama_connected'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_panorama_status()

        if 'Connected' in output and test in output:
            result['result'] = True
            return result
        else:
            result['result'] = False
            return result

    def t_ha_peer_up(self, test):
        test_name = 't_ha_peer_up'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ha_status()
        info = output['group']['peer-info']

        if info['conn-ha2']['conn-status'] == test and info['conn-ha1']['conn-status'] == test:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'ha2-link-status' : info['conn-ha2']['conn-status'],
                'ha1-link-status' : info['conn-ha1']['conn-status']
            }
            return result

    def t_ha_match(self, test):
        test_name = 't_ha_peer_up'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ha_status()
        info = output['group']['local-info']
        compare_dict = {
            'app-version' : info['app-compat'],
            'av-version' : info['av-compat'],
            'threat-version' : info['threat-compat'],
            'gpclient-compat' : info['gpclient-compat'],
            'panos-version' : info['build-compat']
        }

        compat_fail_dict = {}
        for k, v in compare_dict.items():
            if v != test and test == 'Match':
                compat_fail_dict[k] = v

        if not compat_fail_dict:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'baseline' : test,
                'ha-version-match-changes' :  compat_fail_dict
            }
            return result

    def t_ha_config_synched(self, test):
        test_name = 't_ha_config_synched'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ha_status()

        if output['group']['running-sync'] == test:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'ha-config-sync-status' : output['group']['running-sync']
            }
            return result

    def t_interfaces_up(self, test):
        test_name = 't_interfaces_up'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_interface_hardware()

        int_fail_list = []
        for int_test in test:
            for int_hw in output['hw']['entry']:
                if int_test == int_hw['name']:
                    if int_hw['state'] != 'up':
                        int_fail_list.append(int_test)
                    break

        if not int_fail_list:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'interfaces-down' : int_fail_list
            }
            return result

    def t_traffic_log_forward(self):
        test_name = 't_traffic_log_forward'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.cli.run_cmd('show logging-status')
        test = find_seq_number('traffic', output)

        # wait 15 seconda for traffic log to be forwarded
        time.sleep(15)

        output = self.cli.run_cmd('show logging-status')
        log_fwd_seq = find_seq_number('traffic', output)

        if int(log_fwd_seq) > int(test):
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'baseline-seq-no' : test,
                'tvt-seq-no' : log_fwd_seq
            }
            return result 

'''
General Tests - Panorama & Firewall
'''
class GeneralTestCases(object):

    def __init__(self, pandevice_obj, netmiko_obj):
        self.api = PanApi(pandevice_obj)
        self.cli = PanCli(netmiko_obj)                  

    def t_system_version(self, test):
        test_name = 't_system_version'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_system_info()

        if output['system']['sw-version'] == test:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'current-sw-version' : output['system']['sw-version'],
                'target-sw-version' : test
            }
            return result

    def t_config_diff(self, test):
        test_name = 't_config_diff'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        self.cli.run_cmd('set cli config-output-format set')
        self.cli.enter_config_mode()
        running_config_setcmds = self.cli.run_cmd_show('show')
        running_config_setcmds_list = running_config_setcmds.splitlines()

        output = compare_list(test, running_config_setcmds_list)

        if not output['added'] and not output['removed']:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'config-changes' : output
            }
            return result

    def t_ha_enabled(self, test):
        test_name = 't_ha_enabled'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ha_status()

        if output['enabled'] == test:
            result['result'] = True
            return result
        else:
            result['result'] = False
            return result

    def t_ntp_synched(self, test):
        test_name = 't_ntp_synched'
        logging.info('Test case: {}'.format(test_name))

        result = {}
        result['name'] = test_name

        output = self.api.get_ntp()

        ntp_status_1 = output['ntp-server-1']['status']
        ntp_status_2 = output['ntp-server-2']['status']

        if ntp_status_1 == test or ntp_status_2 == test:
            result['result'] = True
            return result
        else:
            result['result'] = False
            result['info'] = {
                'ntp-server-1-status' : ntp_status_1,
                'ntp-server-2-status' : ntp_status_2
            }
            return result