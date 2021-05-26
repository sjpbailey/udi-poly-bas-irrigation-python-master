#!/usr/bin/pyenv python
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from enum import Enum
import ipaddress
import bascontrolns
from bascontrolns import Device, Platform

LOGGER = polyinterface.LOGGER

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'BAS Irrigation'
        self.ipaddress = None
        self.ipaddress2 = None
        self.debug_enable = 'False'
        self.poly.onConfig(self.process_config)
        
    def start(self):
        serverdata = self.poly.get_server_data()
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']
        if self.check_params():
            self.ipaddress =  self.bc('sIpAddress')
                     
        LOGGER.info('Starting BASpi6U6R Network')
        # Remove all existing notices
        self.removeNoticesAll()
        self.check_params()
        
        
    def shortPoll(self):
        self.discover()
              

    def longPoll(self):
        self.discover()

    def query(self,command=None):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()
    class bc:
        def __init__(self):  #sIpAddress
            self.bc = Device()
                
    def get_request(self, url):
        try:
            r = requests.get(url, auth=HTTPBasicAuth('http://' + self.ipaddress, self.ipaddress2 + '/cgi-bin/xml-cgi')) #
            if r.status_code == requests.codes.ok:
                if self.debug_enable == 'True' or self.debug_enable == 'true':
                    print(r.content)

                return r.content
            else:
                LOGGER.error("BASpi6u6r.get_request:  " + r.content)
                return None

        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))        

    def discover(self, *args, **kwargs):
        ### BASpi One ###
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
            self.addNode(Baspi_one(self, self.address, 'baspi1_id', 'Zone 1 Control', self.ipaddress, self.bc))
            self.setDriver('GV19', 1)    
        

        ### BASpi Two ###
        if self.ipaddress2 is not None:
            self.bc2 = Device(self.ipaddress2)
            self.addNode(Baspi_two(self, self.address, 'baspi2_id', 'Zone 2 Control', self.ipaddress2, self.bc2))
            self.setDriver('GV20', 1)
        

    def delete(self):
        LOGGER.info('Removing BASpi6U6R Network')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config));
        LOGGER.info("process_config: Exit");

    def check_params(self):
        st = True
        self.removeNoticesAll()
        default_irrigation1_ip = None
        default_irrigation2_ip = None
        st1 = None

        if 'irrigation1_ip' and 'irrigation2_ip' in self.polyConfig['customParams']:
            self.ipaddress = self.polyConfig['customParams']['irrigation1_ip']
            self.ipaddress2 = self.polyConfig['customParams']['irrigation2_ip']
        else:
            self.ipaddress = default_irrigation1_ip
            self.ipaddress2 = default_irrigation2_ip
            LOGGER.error(
                'check_params: BASpi6u6r IP not defined in customParams, please add it.  Using {}'.format(self.ipaddress))
            st = False        
                
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']

        # Make sure they are in the params 'password': self.password, 'user': self.user,
        self.addCustomParam({'irrigation1_ip': self.ipaddress, 'debug_enable': self.debug_enable})
        self.addCustomParam({'irrigation2_ip': self.ipaddress2, 'debug_enable': self.debug_enable})

        # Add a notice if they need to change the user/password from the defaultself.user == default_user or self.password == default_password or .
        if self.ipaddress == default_irrigation1_ip:
 
            self.addNotice('Please set proper, IP for your Zone Controllers as key = irrigation1_ip and the BASpi IP Address for Value '
                           'in configuration page, and restart this nodeserver')
            st = False
        
        if self.ipaddress2 == default_irrigation2_ip:
            #self.addNotice('Please set proper, IP for Zone Control 2 as key = irrigation2_ip and the BASpi IP Address for Value '
                           #'in configuration page, and restart this nodeserver')

            st1 = False               
            
        if st1 == True:
            return True
        else:
            return False

    
    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st
    
    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV19', 'value': 0, 'uom': 2},
        {'driver': 'GV20', 'value': 0, 'uom': 2},
    ]



class Baspi_one(polyinterface.Node):
    def __init__(self, controller, primary, address, name, ipaddress, bc):
        super(Baspi_one, self).__init__(controller, primary, address, name)
        self.ipaddress = (str(ipaddress).upper()) #Device(str(ipaddress).upper())
        self.bc = bc
        
    def start(self):
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
                        
        ## Do we have a BASpi or an Edge Device ###
        if self.bc.ePlatform == Platform.BASC_PI: ### if a BASpi-6u6r Device is found
            LOGGER.info('connected to BASpi-6U6R Irrigation')
        elif self.bc.ePlatform == Platform.BASC_ED: ### if a BASpi-Edge Device is found
            LOGGER.info('connected to BASpi-Edge Irrigation')
            self.setDriver('ST', 1)    
        elif self.bc.ePlatform == Platform.BASC_NONE: ### if there is NO Device found
            LOGGER.info('Unable to connect to Irrigation Device')
            LOGGER.info('ipaddress')
        else:
            pass
        
        # How many nodes or points does the device have
        LOGGER.info('\t' + str(self.bc.uiQty) + ' Universal inputs in this Doors 1-6')
        LOGGER.info('\t' + str(self.bc.boQty) + ' Binary outputs in this Doors 1-6')
        LOGGER.info('\t' + str(self.bc.vtQty) + ' Virtual points In This Doors 1-6')
        
        # Input/Output Status   
        LOGGER.info('Inputs')
        for i in range(1,7):
            LOGGER.info(str(self.bc.universalInput(i)))
        LOGGER.info('Outputs')
        for i in range(1,7):
               LOGGER.info(str(self.bc.binaryOutput(i)))

        ### Universal Inputs ###
        self.setInputDriver('GV0', 1)
        self.setInputDriver('GV1', 2)
        self.setInputDriver('GV2', 3)
        self.setInputDriver('GV3', 4)
        self.setInputDriver('GV4', 5)
        self.setInputDriver('GV5', 6)

    def setInputDriver(self, driver, input):
        input_val = self.bc.universalInput(input)
       

        # Binary/Digital Outputs
        self.setOutputDriver('GV6', 1)
        self.setOutputDriver('GV7', 2)
        self.setOutputDriver('GV8', 3)
        self.setOutputDriver('GV9', 4)
        self.setOutputDriver('GV10', 5)
        self.setOutputDriver('GV11', 6)
        
    def setOutputDriver(self, driver, input):
        input_val = self.bc.binaryOutput(input)
        
        
        self.mapping = {
            'BON1' : {'output':'GV6', 'index': (1)}, 
            'BOF1' : {'output':'GV6', 'index': (1)}, 
            'BON2' : {'output':'GV7', 'index': (2)}, 
            'BOF2' : {'output':'GV7', 'index': (2)}, 
            'BON3' : {'output':'GV8', 'index': (3)}, 
            'BOF3' : {'output':'GV8', 'index': (3)},
            'BON4' : {'output':'GV9', 'index': (4)}, 
            'BOF4' : {'output':'GV9', 'index': (4)}, 
            'BON5' : {'output':'GV10', 'index': (5)}, 
            'BOF5' : {'output':'GV10', 'index': (5)}, 
            'BON6' : {'output':'GV11', 'index': (6)}, 
            'BOF6' : {'output':'GV11', 'index': (6)},
                } 
    
    
    # OOP Control Commands
    def cmdOn(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc.binaryOutput(index) != 1:
            self.bc.binaryOutput(index, 1)
            self.setDriver(output, 1) 
            LOGGER.info('Zone {} On'.format(index))
            

    def cmdOff(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc.binaryOutput(index) != 0:
            self.bc.binaryOutput(index, 0)
            self.setDriver(output, 0) 
            LOGGER.info('Zone {} Off'.format(index))

   
    def query(self,command=None):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    id = 'baspi1_id'
    commands = {
                    'BON1': cmdOn,
                    'BOF1': cmdOff,
                    'BON2': cmdOn,
                    'BOF2': cmdOff,
                    'BON3': cmdOn,
                    'BOF3': cmdOff,
                    'BON4': cmdOn,
                    'BOF4': cmdOff,
                    'BON5': cmdOn,
                    'BOF5': cmdOff,
                    'BON6': cmdOn,
                    'BOF6': cmdOff,
                    'QUERY': query,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 17},
        {'driver': 'GV1', 'value': 1, 'uom': 56},
        {'driver': 'GV2', 'value': 1, 'uom': 56},
        {'driver': 'GV3', 'value': 1, 'uom': 56},
        {'driver': 'GV4', 'value': 1, 'uom': 56},
        {'driver': 'GV5', 'value': 1, 'uom': 56},
        {'driver': 'GV6', 'value': 1, 'uom': 80},
        {'driver': 'GV7', 'value': 1, 'uom': 80},
        {'driver': 'GV8', 'value': 1, 'uom': 80},
        {'driver': 'GV9', 'value': 1, 'uom': 80},
        {'driver': 'GV10', 'value': 1, 'uom': 80},
        {'driver': 'GV11', 'value': 1, 'uom': 80},
        {'driver': 'GV21', 'value': 1, 'uom': 56},
        {'driver': 'GV22', 'value': 1, 'uom': 56},
        {'driver': 'GV23', 'value': 1, 'uom': 56},
        {'driver': 'GV24', 'value': 1, 'uom': 56},
        {'driver': 'GV25', 'value': 1, 'uom': 56},
        {'driver': 'GV26', 'value': 1, 'uom': 56},
    ]
    
   
    

class Baspi_two(polyinterface.Node):
    def __init__(self, controller, primary, address2, name, ipaddress2, bc2):
        super(Baspi_two, self).__init__(controller, primary, address2, name)
        self.ipaddress2 = (str(ipaddress2).upper()) #Device(str(ipaddress).upper())
        self.bc2 = bc2
        

    def start(self):
        if self.ipaddress2 is not None:
            self.bc2 = Device(self.ipaddress2)
                        
            ## Do we have a BASpi or an Edge Device ###
        if self.bc2.ePlatform == Platform.BASC_PI: ### if a BASpi-6u6r Device is found
            LOGGER.info('connected to BASpi-6U6R Irrigation')
        elif self.bc2.ePlatform == Platform.BASC_ED: ### if a BASpi-Edge Device is found
            LOGGER.info('connected to BASpi-Edge Irrigation')
            self.setDriver('ST', 1)    
        elif self.bc2.ePlatform == Platform.BASC_NONE: ### if there is NO Device found
            LOGGER.info('Unable to connect to Irrigation Device')
            LOGGER.info('ipaddress')
        else:
            pass
            

            LOGGER.info('\t' + str(self.bc2.uiQty) + ' Universal inputs in this BASpi2')
            LOGGER.info('\t' + str(self.bc2.boQty) + ' Binary outputs in this BASpi2')
            LOGGER.info('\t' + str(self.bc2.biQty) + ' Binary inputs in This BASpi2')
            LOGGER.info('\t' + str(self.bc2.aoQty) + ' Analog outputs In This BASpi2')
            
        ### Universal Inputs ###
        input_one = self.bc2.universalInput(1)
        input_two = self.bc2.universalInput(2)
        input_thr = self.bc2.universalInput(3)
        input_for = self.bc2.universalInput(4)
        input_fiv = self.bc2.universalInput(5)
        input_six = self.bc2.universalInput(6)

        # Binary/Digital Outputs
        output_one = (self.bc2.binaryOutput(1))
        output_two = (self.bc2.binaryOutput(2))
        output_tre = (self.bc2.binaryOutput(3))
        output_for = (self.bc2.binaryOutput(4))
        output_fiv = (self.bc2.binaryOutput(5))
        output_six = (self.bc2.binaryOutput(6))
            
        ### Universal Inputs ###            
        self.setDriver('GV0', input_one, force=True)
        self.setDriver('GV1', input_two, force=True)
        self.setDriver('GV2', input_thr, force=True)
        self.setDriver('GV3', input_for, force=True)
        self.setDriver('GV4', input_fiv, force=True)
        self.setDriver('GV5', input_six, force=True)

        # Binary/Digital Outputs
        self.setDriver('GV6', output_one, force=True)
        self.setDriver('GV7', output_two, force=True)
        self.setDriver('GV8', output_tre, force=True)
        self.setDriver('GV9', output_for, force=True)
        self.setDriver('GV10', output_fiv, force=True)
        self.setDriver('GV11', output_six, force=True)
           
        # Input/Output Status   
        LOGGER.info('Inputs')
        for i in range(1,7):
            LOGGER.info(str(self.bc2.universalInput(i)))
        LOGGER.info('Outputs')
        for i in range(1,7):
               LOGGER.info(str(self.bc2.binaryOutput(i)))
        
    
        self.mapping = {
            'BON1' : {'output':'GV6', 'index': (1)}, 
            'BOF1' : {'output':'GV6', 'index': (1)}, 
            'BON2' : {'output':'GV7', 'index': (2)}, 
            'BOF2' : {'output':'GV7', 'index': (2)}, 
            'BON3' : {'output':'GV8', 'index': (3)}, 
            'BOF3' : {'output':'GV8', 'index': (3)},
            'BON4' : {'output':'GV9', 'index': (4)}, 
            'BOF4' : {'output':'GV9', 'index': (4)}, 
            'BON5' : {'output':'GV10', 'index': (5)}, 
            'BOF5' : {'output':'GV10', 'index': (5)}, 
            'BON6' : {'output':'GV11', 'index': (6)}, 
            'BOF6' : {'output':'GV11', 'index': (6)},
                }
    
    def cmdOn(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc2.binaryOutput(index) != 1:
            self.bc2.binaryOutput(index, 1)
            self.setDriver(output, 1) 
            LOGGER.info('Zone {} On'.format(index))
    
    def cmdOff(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc2.binaryOutput(index) != 0:
            self.bc2.binaryOutput(index, 0)
            self.setDriver(output, 0) 
            LOGGER.info('Zone {} Off'.format(index))
    
    
    def query(self,command=None):
        self.reportDrivers()

    
    id = "baspi2_id"
    commands = {
                    'BON1': cmdOn,
                    'BOF1': cmdOff,
                    'BON2': cmdOn,
                    'BOF2': cmdOff,
                    'BON3': cmdOn,
                    'BOF3': cmdOff,
                    'BON4': cmdOn,
                    'BOF4': cmdOff,
                    'BON5': cmdOn,
                    'BOF5': cmdOff,
                    'BON6': cmdOn,
                    'BOF6': cmdOff,
                    'QUERY': query,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 17},
        {'driver': 'GV1', 'value': 1, 'uom': 56},
        {'driver': 'GV2', 'value': 1, 'uom': 56},
        {'driver': 'GV3', 'value': 1, 'uom': 56},
        {'driver': 'GV4', 'value': 1, 'uom': 56},
        {'driver': 'GV5', 'value': 1, 'uom': 56},
        {'driver': 'GV6', 'value': 1, 'uom': 80},
        {'driver': 'GV7', 'value': 1, 'uom': 80},
        {'driver': 'GV8', 'value': 1, 'uom': 80},
        {'driver': 'GV9', 'value': 1, 'uom': 80},
        {'driver': 'GV10', 'value': 1, 'uom': 80},
        {'driver': 'GV11', 'value': 1, 'uom': 80},
        {'driver': 'GV21', 'value': 1, 'uom': 56},
        {'driver': 'GV22', 'value': 1, 'uom': 56},
        {'driver': 'GV23', 'value': 1, 'uom': 56},
        {'driver': 'GV24', 'value': 1, 'uom': 56},
        {'driver': 'GV25', 'value': 1, 'uom': 56},
        {'driver': 'GV26', 'value': 1, 'uom': 56},
    ]

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('BASIRRIGATION')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)

# Union Made by Humans on Earth: sjb / gtb rights reserved