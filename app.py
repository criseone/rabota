import numpy
import time
import pypot.dynamixel
import OSC
import simpleOSC

# Settings
receiveAddress = "0.0.0.0"
receivePort = 8000
dremelJointSpeedMin = 100
dremelJointSpeedMax = 1024
dremelJointPosMin = 40
dremelJointPosMax = 53
wheelSpeedMax = 1024 # use symmetrically for min and max
wheelSlowdownMax = 1 # %, in range 0-1
leftWheelMotorId = 3
rightWheelMotorId = 2
dremelMotorId = 4

# Global variables
wheelSpeed = 0
leftWheelSlowdown = 0
rightWheelSlowdown = 0

def wheelSpeedHandler(addr, tags, data, source):
    global wheelSpeedMax, wheelSpeed
    value = data[0] + 0.0
    if value == 0:
        value = 1; # Fix problem with non-symmetrical values
    wheelSpeed = (value - 64)/63 * wheelSpeedMax
    updateWheelSpeeds()

def wheelSlowdownHandler(addr, tags, data, source):
    global wheelSlowdownMax, leftWheelSlowdown, rightWheelSlowdown
    value = data[0] + 0.0
    if value == 0:
        value = 1; # Fix problem with non-symmetrical values
    slowdown = (value - 64)/63 * wheelSlowdownMax
    if slowdown > 0:
        leftWheelSlowdown = slowdown
        rightWheelSlowdown = 0
    else:
        leftWheelSlowdown = 0
        rightWheelSlowdown = -slowdown
    updateWheelSpeeds()

def dremelJointPosHandler(addr, tags, data, source):
    global dxlIO, dremelJointPosMin, dremelJointPosMax, dremelMotorId
    value = data[0] + 0.0
    pos = value/127 * (dremelJointPosMax - dremelJointPosMin) + dremelJointPosMin
    dxlIO.set_goal_position({dremelMotorId: -pos})

def dremelJointSpeedHandler(addr, tags, data, source):
    global dxlIO, dremelJointSpeedMin, dremelJointSpeedMax, dremelMotorId
    value = data[0] + 0.0
    speed = value/127 * (dremelJointSpeedMax - dremelJointSpeedMin) + dremelJointSpeedMin
    dxlIO.set_moving_speed({dremelMotorId: speed})

def stopHandler(addr, tags, data, source):
    dxlIO.set_moving_speed({leftWheelMotorId: 0, rightWheelMotorId : 0})

def leftWheelSpeedHandler(addr, tags, data, source):
    dxlIO.set_moving_speed({leftWheelMotorId: data[0]})

def rightWheelSpeedHandler(addr, tags, data, source):
    dxlIO.set_moving_speed({rightWheelMotorId: data[0]})




def updateWheelSpeeds():
    global dxlIO, wheelSpeed, leftWheelSlowdown, rightWheelSlowdown, leftWheelMotorId, rightWheelMotorId
    leftWheelSpeed = wheelSpeed * (1 - leftWheelSlowdown)
    rightWheelSpeed = -wheelSpeed * (1 - rightWheelSlowdown)
    dxlIO.set_moving_speed({leftWheelMotorId: leftWheelSpeed, rightWheelMotorId: rightWheelSpeed})


def app():
    # Init Dynamixel connection
    global dxlIO, foundIds
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        raise IOError('No port available.')
    port = ports[0]
    dxlIO = pypot.dynamixel.DxlIO(port)
    print 'Connected DxLIO'
    # print 'Found Motors with IDs: ' 
    # print dxlIO.scan()
    # Setup motors
    # dxlIO.enable_torque([leftWheelMotorId, rightWheelMotorId]) #, dremelMotorId])
    dxlIO.enable_torque([leftWheelMotorId, rightWheelMotorId])
    # dxlIO.set_moving_speed({dremelMotorId: dremelJointSpeedMin})
    print 'Motors Set Up'

    # Init OSC server
    simpleOSC.initOSCServer(receiveAddress, receivePort)
    simpleOSC.setOSCHandler('/wheelspeed', wheelSpeedHandler)
    simpleOSC.setOSCHandler('/rightwheelspeed', rightWheelSpeedHandler)
    simpleOSC.setOSCHandler('/leftwheelspeed', leftWheelSpeedHandler)
    simpleOSC.setOSCHandler('/wheelslowdown', wheelSlowdownHandler)
    simpleOSC.setOSCHandler('/dremeljointpos', dremelJointPosHandler)
    simpleOSC.setOSCHandler('/dremeljointspeed', dremelJointSpeedHandler)
    simpleOSC.setOSCHandler('/stop', stopHandler)
    simpleOSC.startOSCServer()
    # Enter infinite loop to be able to catch KeyboardInterrupt
    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
        simpleOSC.closeOSC()

# Launch the app
if __name__ == '__main__': app()
