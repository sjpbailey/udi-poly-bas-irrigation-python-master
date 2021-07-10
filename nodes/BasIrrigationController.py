try:
    from polyinterface import Controller,LOG_HANDLER,LOGGER
except ImportError:
    from pgc_interface import Controller,LOGGER
import logging
import sys
import time
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from enum import Enum
import ipaddress
import bascontrolns
from bascontrolns import Device, Platform

# My Template Node
from nodes import BaspiNodeOne
from nodes import BaspiNodeTwo
from nodes import BaspiNodeThree
from nodes import BaspiNodeFour
from nodes import BaspiNodeFive
from nodes import BaspiNodeSix

# IF you want a different log format than the current default
LOG_HANDLER.set_log_format('%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')

class BasIrrigationController(Controller):
    def __init__(self, polyglot):
        super(BasIrrigationController, self).__init__(polyglot)
        self.name = 'Irrigation'
        self.hb = 0
        self.Device = Device
        # This can be used to call your function everytime the config changes
        # But currently it is called many times, so not using.
        #self.poly.onConfig(self.process_config)

    def start(self):
        # This grabs the server.json data and checks profile_version is up to
        # date based on the profile_version in server.json as compared to the
        # last time run which is stored in the DB.  When testing just keep
        # changing the profile_version to some fake string to reload on restart
        # Only works on local currently..
        serverdata = self.poly.get_server_data(check_profile=True)
        #serverdata['version'] = "testing"
        LOGGER.info('Started BAS Irrigation {}'.format(serverdata['version']))
        # Show values on startup if desired.
        LOGGER.debug('ST=%s',self.getDriver('ST'))
        self.setDriver('ST', 1)
        self.heartbeat(0)
        self.check_params()
        self.set_debug_level(self.getDriver('GV1'))
        self.discover()
        
    def shortPoll(self):
        self.discover()
        LOGGER.debug('shortPoll')
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def longPoll(self):
        self.heartbeat() 
        LOGGER.debug('longPoll')
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def query(self,command=None):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()
    class bc:
        def __init__(self, sIpAddress, ePlatform):
            self.bc = Device()
            self.ePlatform = ePlatform
                
    def get_request(self, url):
        try:
            r = requests.get(url, auth=HTTPBasicAuth('http://' + self.ipaddress1, 
            self.ipaddress2 + self.ipaddress3, + self.ipaddress4, self.ipaddress5, + self.ipaddress6 + '/cgi-bin/xml-cgi')) 
            if r.status_code == requests.codes.ok:
                if self.debug_enable == 'True' or self.debug_enable == 'true':
                    print(r.content)

                return r.content
            else:
                LOGGER.error("BASpi6u6r.get_request:  " + r.content)
                return None

        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))


    def delete(self):
        LOGGER.info('Removing BAS Irrigation')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config))
        LOGGER.info("process_config: Exit")

    def heartbeat(self,init=False):
        LOGGER.debug('heartbeat: init={}'.format(init))
        if init is not False:
            self.hb = init
        LOGGER.debug('heartbeat: hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def set_module_logs(self,level):
        logging.getLogger('urllib3').setLevel(level)

    def set_debug_level(self,level):
        LOGGER.debug('set_debug_level: {}'.format(level))
        if level is None:
            level = 30
        level = int(level)
        if level == 0:
            level = 30
        LOGGER.info('set_debug_level: Set GV1 to {}'.format(level))
        self.setDriver('GV1', level)
        # 0=All 10=Debug are the same because 0 (NOTSET) doesn't show everything.
        if level <= 10:
            LOGGER.setLevel(logging.DEBUG)
        elif level == 20:
            LOGGER.setLevel(logging.INFO)
        elif level == 30:
            LOGGER.setLevel(logging.WARNING)
        elif level == 40:
            LOGGER.setLevel(logging.ERROR)
        elif level == 50:
            LOGGER.setLevel(logging.CRITICAL)
        else:
            LOGGER.debug("set_debug_level: Unknown level {}".format(level))
        # this is the best way to control logging for modules, so you can
        # still see warnings and errors
        #if level < 10:
        #    self.set_module_logs(logging.DEBUG)
        #else:
        #    # Just warnigns for the modules unless in module debug mode
        #    self.set_module_logs(logging.WARNING)
        # Or you can do this and you will never see mention of module logging
        if level < 10:
            LOG_HANDLER.set_basic_config(True,logging.DEBUG)
        else:
            # This is the polyinterface default
            LOG_HANDLER.set_basic_config(True,logging.WARNING)
        
    def check_params(self):
        self.removeNoticesAll()
        default_irr1_ip = None
        default_irr2_ip = None
        default_irr3_ip = None
        default_irr4_ip = None
        default_irr5_ip = None
        default_irr6_ip = None

        if 'irr1_ip' and 'irr2_ip' and 'irr3_ip' and 'irr4_ip' and 'irr5_ip'  in self.polyConfig['customParams']:   #and 'irr6_ip'
            self.ipaddress = self.polyConfig['customParams']['irr1_ip']
            self.ipaddress2 = self.polyConfig['customParams']['irr2_ip']
            self.ipaddress3 = self.polyConfig['customParams']['irr3_ip']
            self.ipaddress4 = self.polyConfig['customParams']['irr4_ip']
            self.ipaddress5 = self.polyConfig['customParams']['irr5_ip']
            self.ipaddress6 = self.polyConfig['customParams']['irr6_ip']

        else:
            self.ipaddress = default_irr1_ip
            self.ipaddress2 = default_irr2_ip
            self.ipaddress3 = default_irr3_ip
            self.ipaddress4 = default_irr4_ip
            self.ipaddress5 = default_irr5_ip
            self.ipaddress6 = default_irr6_ip
            LOGGER.error(
                'check_params: The First BASpi6u6r IP is not defined in customParams, please add at least one.  Using {}'.format(self.ipaddress))

        self.addCustomParam({'irr1_ip': self.ipaddress})
        self.addCustomParam({'irr2_ip': self.ipaddress2})
        self.addCustomParam({'irr3_ip': self.ipaddress3})
        self.addCustomParam({'irr4_ip': self.ipaddress4})
        self.addCustomParam({'irr5_ip': self.ipaddress5})
        self.addCustomParam({'irr6_ip': self.ipaddress6})

        # Add a notice if they need to change the user/password from the defaultself.user == default_user or self.password == default_password or .
        if self.ipaddress == default_irr1_ip:
            self.setDriver('GV19', 0) 
            self.addNotice('Please set proper, IP for your Zone Controllers as key = irr1_ip and the BASpi IP Address for Value '
                            'in configuration page, and restart this nodeserver for additional controllers input irr2_ip, irr3_ip up to irr6')
            st = False
        
        if self.ipaddress2 == default_irr2_ip:
            st = False
            
        if self.ipaddress3 == default_irr3_ip:
            st = False

        if self.ipaddress4 == default_irr4_ip:
            st = False

        if self.ipaddress5 == default_irr5_ip:
            st = False

        if self.ipaddress6 == default_irr6_ip:
            st = False

        else:
            return True

    def discover(self, *args, **kwargs):
        ### BASpi One ###
        LOGGER.info(self.ipaddress)
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
            self.addNode(BaspiNodeOne(self, self.address, 'baspi1_id', 'Zone Control 1', self.ipaddress, self.bc))
        
        ### BASpi Two ###
        LOGGER.info(self.ipaddress2)
        if self.ipaddress2 is not None:
            self.bc2 = Device(self.ipaddress2)
            self.addNode(BaspiNodeTwo(self, self.address, 'baspi2_id', 'Zone Control 2', self.ipaddress2, self.bc2))
        
        ### BASpi Three ###
        LOGGER.info(self.ipaddress3)
        if self.ipaddress3 is not None:
            self.bc3 = Device(self.ipaddress3)
            self.addNode(BaspiNodeThree(self, self.address, 'baspi3_id', 'Zone Control 3', self.ipaddress3, self.bc3))

        ### BASpi Four ###
        LOGGER.info(self.ipaddress4)
        if self.ipaddress4 is not None:
            self.bc4 = Device(self.ipaddress4)
            self.addNode(BaspiNodeFour(self, self.address, 'baspi4_id', 'Zone Control 4', self.ipaddress4, self.bc4))

        ### BASpi Five ###
        LOGGER.info(self.ipaddress5)
        if self.ipaddress5 is not None:
            self.bc5 = Device(self.ipaddress5)
            self.addNode(BaspiNodeFive(self, self.address, 'baspi5_id', 'Zone Control 5', self.ipaddress5, self.bc5))
        
        ### BASpi Fsix ###
        LOGGER.info(self.ipaddress6)
        if self.ipaddress6 is not None:
            self.bc6 = Device(self.ipaddress6)
            self.addNode(BaspiNodeSix(self, self.address, 'baspi6_id', 'Zone Control 6', self.ipaddress6, self.bc6))
        
    def remove_notice_test(self,command):
        LOGGER.info('remove_notice_test: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNotice('test')

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def cmd_set_debug_mode(self,command):
        val = int(command.get('value'))
        LOGGER.debug("cmd_set_debug_mode: {}".format(val))
        self.set_debug_level(val)
    
    id = 'controller'

    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'REMOVE_NOTICE_TEST': remove_notice_test,
        'SET_DM': cmd_set_debug_mode,
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 10, 'uom': 25},
    ]
