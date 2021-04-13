
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import urllib3
from bascontrolns import Device, Platform

LOGGER = polyinterface.LOGGER

class BaspiNodeFour(polyinterface.Node):
    def __init__(self, controller, primary, address4, name, ipaddress4, bc4):
        super(BaspiNodeFour, self).__init__(controller, primary, address4, name)
        self.lpfx = '%s:%s' % (address4,name)
        self.ipaddress = (str(ipaddress4).upper()) #Device(str(ipaddress).upper())
        self.bc4 = bc4
        
    def start(self):
        if self.ipaddress is not None:
            self.bc4 = Device(self.ipaddress)
                        
        ### BASpi Four ###
        if self.bc4.ePlatform == Platform.BASC_NONE:
            LOGGER.info('Unable to connect')
            LOGGER.info('ipaddress4')
        if self.bc4.ePlatform == Platform.BASC_PI:
            LOGGER.info('Connected to BASpi6U6R Module Four')
        if self.bc4.ePlatform == Platform.BASC_PO:
            LOGGER.info('Connected to BASpi6U6R Module Four')    
        if self.bc4.ePlatform == Platform.BASC_ED:
            LOGGER.info('Connected to BASpi-Edge Module Four')    
            self.setDriver('ST', 1)    

        if self.bc4.ePlatform == Platform.BASC_ED:
                LOGGER.info('Universal inputs in this BASpi-EDGE1' + '\t' + str(self.bc4.uiQty))
                LOGGER.info('Binary outputs in this BASpi-EDGE1' + '\t' + str(self.bc4.boQty))
        if self.bc4.ePlatform == Platform.BASC_PI:
                LOGGER.info('Universal inputs in this BASpi-6U6R' + '\t' + str(self.bc4.uiQty))
                LOGGER.info('Binary outputs in this BASpi-6U6R' + '\t' + str(self.bc4.boQty))
        if self.bc4.ePlatform == Platform.BASC_PO:
                LOGGER.info('Universal inputs in this BASpi-6U6R' + '\t' + str(self.bc4.uiQty))
                LOGGER.info('Binary outputs in this BASpi-6U6R' + '\t' + str(self.bc4.boQty))        
                        
        # Input/Output Status
        LOGGER.info('UI 1' + '\t' + str(self.bc4.universalInput(1)))
        LOGGER.info('UI 2' + '\t' + str(self.bc4.universalInput(2)))
        LOGGER.info('UI 3' + '\t' + str(self.bc4.universalInput(3)))
        LOGGER.info('UI 4' + '\t' + str(self.bc4.universalInput(4)))
        LOGGER.info('UI 5' + '\t' + str(self.bc4.universalInput(5)))
        LOGGER.info('UI 6' + '\t' + str(self.bc4.universalInput(6)))
        LOGGER.info('BO 1' + '\t' + str(self.bc4.binaryOutput(1)))
        LOGGER.info('BO 2' + '\t' + str(self.bc4.binaryOutput(2)))
        LOGGER.info('BO 3' + '\t' + str(self.bc4.binaryOutput(3)))
        LOGGER.info('BO 4' + '\t' + str(self.bc4.binaryOutput(4)))
        LOGGER.info('BO 5' + '\t' + str(self.bc4.binaryOutput(5)))
        LOGGER.info('BO 6' + '\t' + str(self.bc4.binaryOutput(6)))
        
        ### Universal Inputs ###
        input_one = self.bc4.universalInput(1)
        input_two = self.bc4.universalInput(2)
        input_thr = self.bc4.universalInput(3)
        input_for = self.bc4.universalInput(4)
        input_fiv = self.bc4.universalInput(5)
        input_six = self.bc4.universalInput(6)

        ### Universal Inputs ###            
        self.setDriver('GV0', input_one, force=True)
        self.setDriver('GV1', input_two, force=True)
        self.setDriver('GV2', input_thr, force=True)
        self.setDriver('GV3', input_for, force=True)
        self.setDriver('GV4', input_fiv, force=True)
        
        # Binary/Digital Outputs
        output_one = (self.bc4.binaryOutput(1))
        output_two = (self.bc4.binaryOutput(2))
        output_tre = (self.bc4.binaryOutput(3))
        output_for = (self.bc4.binaryOutput(4))
        output_fiv = (self.bc4.binaryOutput(5))
        output_six = (self.bc4.binaryOutput(6))
           
        # Binary/Digital Outputs
        self.setDriver('GV6', output_one, force=True)
        self.setDriver('GV7', output_two, force=True)
        self.setDriver('GV8', output_tre, force=True)
        self.setDriver('GV9', output_for, force=True)
        self.setDriver('GV10', output_fiv, force=True)
        self.setDriver('GV11', output_six, force=True)
           
        # Input 6 Conversion
        if input_six is not None:
            sumss_count = int(float(input_six))
            self.setDriver('GV5', int(sumss_count), force=True)
        if input_six is not None:
            sumss_count = int(float(self.bc4.universalInput(6)))
    
    
    # OOP Control Commands
    # Zone 1
    def cmdOn1(self, command):
        if self.bc4.binaryOutput(1) != 1:
            self.bc4.binaryOutput(1, 1)
            self.setDriver("GV6", 1) 
            LOGGER.info('Zone 1 On')

    def cmdOff1(self, command):
        if self.bc4.binaryOutput(1) != 0:
            self.bc4.binaryOutput(1, 0)
            self.setDriver("GV6", 0) 
            LOGGER.info('Zone 1 Off')

    # Zone 2
    def cmdOn2(self, command):
        if self.bc4.binaryOutput(2) != 1:
            self.bc4.binaryOutput(2, 1)
            self.setDriver("GV7", 1) 
            LOGGER.info('Zone 2 On')
            
    def cmdOff2(self, command):
        if self.bc4.binaryOutput(2) != 0:
            self.bc4.binaryOutput(2, 0)
            self.setDriver("GV7", 0) 
            LOGGER.info('Zone 2 Off')
   
    # Zone 3
    def cmdOn3(self, command):
        if self.bc4.binaryOutput(3) != 1:
            self.bc4.binaryOutput(3, 1)
            self.setDriver("GV8", 1) 
            LOGGER.info('Zone 3 On')

    def cmdOff3(self, command):
        if self.bc4.binaryOutput(3) != 0:
            self.bc4.binaryOutput(3, 0)
            self.setDriver("GV8", 0) 
            LOGGER.info('Zone 3 Off')

    # Zone 4
    def cmdOn4(self, command):
        if self.bc4.binaryOutput(4) != 1:
            self.bc4.binaryOutput(4, 1)
            self.setDriver("GV9", 1)
            LOGGER.info('Zone 4 On')
           
    def cmdOff4(self, command):
        if self.bc4.binaryOutput(4) != 0:
            self.bc4.binaryOutput(4, 0)
            self.setDriver("GV9", 0) 
            LOGGER.info('Zone 4 Off')
   
    # Zone 5
    def cmdOn5(self, command):
        if self.bc4.binaryOutput(5) != 1:
            self.bc4.binaryOutput(5, 1)
            self.setDriver("GV10", 1) 
            LOGGER.info('Zone 5 On')
            
    def cmdOff5(self, command):
        if self.bc4.binaryOutput(5) != 0:
            self.bc4.binaryOutput(5, 0)
            self.setDriver("GV10", 0) 
            LOGGER.info('Zone 5 Off')
    
    # Zone 6
    def cmdOn6(self, command):
        if self.bc4.binaryOutput(6) != 1:
            self.bc4.binaryOutput(6, 1)
            self.setDriver("GV11", 1) 
            LOGGER.info('Zone 6 On')
            
    def cmdOff6(self, command):
        if self.bc4.binaryOutput(6) != 0:
            self.bc4.binaryOutput(6, 0)
            self.setDriver("GV11", 0) 
            LOGGER.info('Zone 6 Off')

    def shortPoll(self):
        LOGGER.debug('shortPoll')
        
    def longPoll(self):
        LOGGER.debug('longPoll')

    def cmd_ping(self,command):
        LOGGER.debug("cmd_ping:")
        r = self.http.request('GET',"google.com")
        LOGGER.debug("cmd_ping: r={}".format(r))

    def query(self,command=None):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 17},
        {'driver': 'GV1', 'value': 1, 'uom': 56},
        {'driver': 'GV2', 'value': 1, 'uom': 56},
        {'driver': 'GV3', 'value': 1, 'uom': 56},
        {'driver': 'GV4', 'value': 1, 'uom': 56},
        {'driver': 'GV5', 'value': 1, 'uom': 25},
        {'driver': 'GV6', 'value': 1, 'uom': 80},
        {'driver': 'GV7', 'value': 1, 'uom': 80},
        {'driver': 'GV8', 'value': 1, 'uom': 80},
        {'driver': 'GV9', 'value': 1, 'uom': 80},
        {'driver': 'GV10', 'value': 1, 'uom': 80},
        {'driver': 'GV11', 'value': 1, 'uom': 80},
        ]
    
    id = 'baspi4_id'
    """
    id of the node from the nodedefs.xml that is in the profile.zip. This tells
    the ISY what fields and commands this node has.
    """
    commands = {
                    'BON1': cmdOn1,
                    'BOF1': cmdOff1,
                    'BON2': cmdOn2,
                    'BOF2': cmdOff2,
                    'BON3': cmdOn3,
                    'BOF3': cmdOff3,
                    'BON4': cmdOn4,
                    'BOF4': cmdOff4,
                    'BON5': cmdOn5,
                    'BOF5': cmdOff5,
                    'BON6': cmdOn6,
                    'BOF6': cmdOff6,
                    'QUERY': query,
                }
    