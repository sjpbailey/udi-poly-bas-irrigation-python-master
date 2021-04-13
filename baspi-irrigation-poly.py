#!/usr/bin/env python
"""
This is a NodeServer is for Irrigation Control of 12 Zones using 2 
Contemporary Controls BASpi-6U6R DIY modules Written by Steve and Gerrod Bailey
sjpbailey1961@gmail.com
template for Polyglot v2 written in Python2/3
by Einstein.42 (James Milne) milne.james@gmail.com
"""
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
""" Grab My Controller Node """
from nodes import BasIrrigationController
from nodes import BaspiNodeOne
from nodes import BaspiNodeTwo
from nodes import BaspiNodeThree
from nodes import BaspiNodeFour
from nodes import BaspiNodeFive
from nodes import BaspiNodeSix

LOGGER = polyinterface.LOGGER

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('BASIRRIGATION')
        polyglot.start()
        control = BasIrrigationController(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """
        polyglot.stop()
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
    sys.exit(0)
