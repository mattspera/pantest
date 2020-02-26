import re
import sys
import logging

import xmltodict
from pandevice.base import PanDevice
from pandevice.errors import PanDeviceError
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException

class PanApi(object):

    def __init__(self, device_info):
        try:
            device = PanDevice.create_from_device(
                device_info['ip'],
                device_info['username'],
                device_info['password']
            )
        except PanDeviceError as e:
            print(e.message)
            sys.exit()

        self.dev = device

    def get_system_info(self):
        req = 'show system info'
        logging.info(req)

        resp = self.dev.op(req, xml=True) # xml=True return the xml string rather than element tree
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_route_table(self):
        req = 'show routing route'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_route_interface(self):
        req = 'show routing interface'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_system_environmentals(self):
        req = 'show system environmentals'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_ntp(self):
        req = 'show ntp'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_panorama_status(self):
        req = 'show panorama status'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']   

    def get_ha_status(self):
        req = 'show high-availability all'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_device_groups(self):
        req = 'show devicegroups'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_templates(self):
        req = 'show templates'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_devices_connected(self):
        req = 'show devices connected'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_log_collectors_connected(self):
        req = "show log-collector connected"
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_wf_appliances_connected(self):
        req = "show wildfire-appliance connected"
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_interface_hardware(self):
        req = '<show><interface>hardware</interface></show>' # req in xml as required for this api call to work
        logging.info(req)

        resp = self.dev.op(req, xml=True, cmd_xml=False) # cmd_xml=False allows xml formatted req
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_running_security_policy(self, vsys):
        req = 'show running security-policy'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

    def get_running_nat_policy(self, vsys):
        req = 'show running nat-policy'
        logging.info(req)

        resp = self.dev.op(req, xml=True)
        logging.info(resp + b'\n')

        return xmltodict.parse(resp)['response']['result']

class PanCli(object):

    def __init__(self, device_info):
        device_info['device_type'] = 'paloalto_panos' 

        try:
            ssh_connection_handler = ConnectHandler(**device_info)
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            print(e)
            sys.exit()

        self.conn = ssh_connection_handler

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.disconnect()

    def run_cmd(self, cmd, expect_string=''):
        logging.info(cmd)

        res = self.conn.send_command(cmd, expect_string=expect_string)
        logging.info(res + '\n')

        return res

    def run_cmd_show(self, cmd):
        logging.info(cmd)

        res = self.conn.send_command_timing(cmd, delay_factor=10)
        logging.info(res + '\n')

        return res

    def enter_config_mode(self):
        self.conn.config_mode()

class PanHybrid(object):

    def __init__(self, device_info):
        self.api = PanApi(device_info)
        self.cli = PanCli(device_info)

    def get_connectivity(self):
        nexthops = []
        nexthop_interfaces = []

        for entry in self.api.get_route_table()['entry']:
            if (
                entry['nexthop'] != '0.0.0.0' and
                entry['nexthop'] != 'discard' and
                not entry['nexthop'] in nexthops
            ):
                nexthops.append(entry['nexthop'])
                nexthop_interfaces.append(entry['interface'])

        interface_ip_map_dict = {}

        for interface in self.api.get_route_interface()['interface']:
            if 'address' in interface:
                interface_ip_map_dict[interface['name']] = interface['address']
            else:
                interface_ip_map_dict[interface['name']] = ''

        nexthop_interface_ips = []

        for nexthop_interface in nexthop_interfaces:
            for int_name, int_ip in interface_ip_map_dict.items():
                if nexthop_interface == int_name:
                    nexthop_interface = int_ip
                    nexthop_interface_ips.append(nexthop_interface[:-3])
                    break

        packet_loss_dict = {}

        for nexthop, source in list(zip(nexthops, nexthop_interface_ips)):
            if source:
                cmd = 'ping source {} count 2 host {}'.format(source, nexthop)
                raw_text_ping = self.cli.run_cmd(cmd, expect_string=r'(unknown)|(syntax)|(bind)|(\d{1,3})%').strip('ping\n')
                re_packet_loss = re.search(r'(\d{1,3})%', raw_text_ping)

                if re_packet_loss:
                    packet_loss_dict[nexthop] = re_packet_loss.group(0)

        return packet_loss_dict