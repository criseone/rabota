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
    #     global dxlIO, foundIds
    #     value = midi.getControllerValue()
    #     print '%s: cc' % port, midi.getControllerNumber(), value
    #     pos = (value - 63.5)/63.5 * 150
    #     dxlIO.set_goal_position(dict(zip(foundIds, itertools.repeat(pos))))
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags :%s" % tags
    print "the actual data is : %s" % data

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

# Launch the app
if __name__ == '__main__': app()