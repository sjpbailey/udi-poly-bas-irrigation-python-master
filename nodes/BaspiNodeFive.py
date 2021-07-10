
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import urllib3
from bascontrolns import Device, Platform

LOGGER = polyinterface.LOGGER
class BaspiNodeFive(polyinterface.Node):
    def __init__(self, controller, primary, address, name, ipaddress, bc5):
        super(BaspiNodeFive, self).__init__(controller, primary, address, name)
        self.lpfx = '%s:%s' % (address,name)
        self.ipaddress = (str(ipaddress).upper()) #Device(str(ipaddress).upper())
        self.bc5 = bc5

    def start(self):
        if self.ipaddress is not None:
            self.bc5 = Device(self.ipaddress)

        ### Do we have a BASpi or an Edge Device ###
        if self.bc5.ePlatform == Platform.BASC_PI or self.bc5.ePlatform == Platform.BASC_PO: ### if a BASpi-6u6r Device is found
            LOGGER.info('connected to BASpi-6U6R')
        elif self.bc5.ePlatform == Platform.BASC_ED: ### if a BASpi-Edge Device is found
            LOGGER.info('connected to BASpi-Edge')
            self.setDriver('ST', 1)    
        elif self.bc5.ePlatform == Platform.BASC_NONE: ### if there is NO Device found
            LOGGER.info('Unable to connect to Device')
            LOGGER.info('ipaddress')
        else:
            pass
        
        # How many nodes or points does the device have
        LOGGER.info('\t' + str(self.bc5.uiQty) + ' Universal inputs in this Device')
        LOGGER.info('\t' + str(self.bc5.boQty) + ' Binary outputs in this Device')
        LOGGER.info('\t' + str(self.bc5.vtQty) + ' Virtual points In This Device')        
        
        # Input/Output Status
        LOGGER.info('Inputs')
        for i in range(1,7):
            LOGGER.info(str(self.bc5.universalInput(i)))
        LOGGER.info('Outputs')
        for i in range(1,7):
            LOGGER.info(str(self.bc5.binaryOutput(i)))
        
        ### Universal Inputs ###
        self.setInputDriver('GV0', 1)
        self.setInputDriver('GV1', 2)
        self.setInputDriver('GV2', 3)
        self.setInputDriver('GV3', 4)
        self.setInputDriver('GV4', 5)

        # Binary/Digital Outputs
        self.setOutputDriver('GV6', 1)
        self.setOutputDriver('GV7', 2)
        self.setOutputDriver('GV8', 3)
        self.setOutputDriver('GV9', 4)
        self.setOutputDriver('GV10', 5)
        self.setOutputDriver('GV11', 6)
        
        # Input 6 Conversion
        input_six = self.bc5.universalInput(6)
        if input_six is not None:
            sumss_count = int(float(input_six))
            self.setDriver('GV5', int(sumss_count), force=True)
        if input_six is not None:
            sumss_count = int(float(self.bc5.universalInput(6))) 
        else:
            return

    ### Universal Input Conversion ###
    def setInputDriver(self, driver, input):
        input_val = self.bc5.universalInput(input)
        count = 0
        if input_val is not None:
            count = int(float(input_val))
            self.setDriver(driver, count, force=True)
        else:
            return

    ### Binary Output Conversion ###    
    def setOutputDriver(self, driver, input):
        output_val = self.bc5.binaryOutput(input)
        count = 0
        if output_val is not None:
            count = (output_val)
            self.setDriver(driver, count, force=True)
        else:
            return       
        pass

        # Dict for 6 output ON OFF function     
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
        
    # ON OFF Control Commands
    # All Zones
    def cmdOn(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc5.binaryOutput(index) != 1:
            self.bc5.binaryOutput(index, 1)
            self.setDriver(output, 1) 
            LOGGER.info('Zone {} On'.format(index))

    def cmdOff(self, command):
        output = self.mapping[command['cmd']]['output']
        index = self.mapping[command['cmd']]['index']
        if self.bc5.binaryOutput(index) != 0:
            self.bc5.binaryOutput(index, 0)
            self.setDriver(output, 0)
            LOGGER.info('Zone {} Off'.format(index))

    def query(self,command=None):
        self.reportDrivers()
    
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 17},
        {'driver': 'GV1', 'value': 1, 'uom': 56},
        {'driver': 'GV2', 'value': 1, 'uom': 56},
        {'driver': 'GV3', 'value': 1, 'uom': 56},
        {'driver': 'GV4', 'value': 1, 'uom': 56},
        {'driver': 'GV5', 'value': 1, 'uom': 25},
        #{'driver': 'GV6', 'value': 1, 'uom': 80},
        #{'driver': 'GV7', 'value': 1, 'uom': 80},
        #{'driver': 'GV8', 'value': 1, 'uom': 80},
        #{'driver': 'GV9', 'value': 1, 'uom': 80},
        #{'driver': 'GV10', 'value': 1, 'uom': 80},
        #{'driver': 'GV11', 'value': 1, 'uom': 80},
        ]
    
    id = 'baspi5_id'
    """
    id of the node from the nodedefs.xml that is in the profile.zip. This tells
    the ISY what fields and commands this node has.
    """
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
    