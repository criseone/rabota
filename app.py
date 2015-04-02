import sys
import threading
import itertools
import numpy
import time
import pypot.dynamixel
import OSC
import simpleOSC

# Settings
motorSpeed = 1023
receiveAddress = "0.0.0.0"
receivePort = 8000

# Global variables
global dxlIO, foundIds, wheelSpeed, wheelOffset, dremelJointAngle, dremelJointSpeed

def wheelSpeedHandler(addr, tags, data, source):
    # if midi.isController():
    global dxlIO, foundIds
    if data == 0:
        data = 1; # Fix problem with non-symmetrical values
    pos = (data - 64)/64 * 150
    dxlIO.set_goal_position(dict(zip(foundIds, itertools.repeat(pos))))
    
def app():
    # Init Dynamixel connection
    global dxlIO, foundIds
    ports = pypot.dynamixel.get_available_ports()
    print 'available ports:', ports
    if not ports:
        raise IOError('No port available.')
    port = ports[0]
    print 'Using the first on the list', port
    dxlIO = pypot.dynamixel.DxlIO(port)
    print 'Connected!'
    foundIds = dxlIO.scan()
    print 'Found ids:', foundIds
    # Setup motors
    dxlIO.enable_torque(foundIds)
    dxlIO.set_moving_speed(dict(zip(foundIds, itertools.repeat(motorSpeed))))
    # Init OSC server
    simpleOSC.initOSCServer(receiveAddress, receivePort)
    simpleOSC.setOSCHandler('/wheelspeed', wheelSpeedHandler)
    simpleOSC.startOSCServer()
        # Enter infinite loop to be able to catch KeyboardInterrupt
    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
        simpleOSC.closeOSC()

# Launch the app
if __name__ == '__main__': app()