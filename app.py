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
    global dxlIO, wheelSpeedMax, wheelSpeed
    cc = data[0] + 0.0
    if cc == 0:
        cc = 1; # Fix problem with non-symmetrical values
    wheelSpeed = (cc - 64)/64 * wheelSpeedMax
    updateWheelSpeeds()

def wheelSlowdownHandler(addr, tags, data, source):
    global dxlIO, wheelSlowdownMax, leftWheelSlowdown, rightWheelSlowdown
    cc = data[0] + 0.0
    if cc == 0:
        cc = 1; # Fix problem with non-symmetrical values
    slowdown = (cc - 64)/64 * wheelSlowdownMax
    if slowdown > 0:
        leftWheelSlowdown = slowdown
        rightWheelSlowdown = 0
    else:
        leftWheelSlowdown = 0
        rightWheelSlowdown = -slowdown
    updateWheelSpeeds()

def dremelJointPosHandler(addr, tags, data, source):
    global dxlIO, dremelJointPosMin, dremelJointPosMax, dremelMotorId
    cc = data[0] + 0.0
    pos = cc/127 * (dremelJointPosMax - dremelJointPosMin) + dremelJointPosMin
    dxlIO.set_goal_position({dremelMotorId: -pos})

def dremelJointSpeedHandler(addr, tags, data, source):
    global dxlIO, dremelJointSpeedMin, dremelJointSpeedMax, dremelMotorId
    cc = data[0] + 0.0
    speed = cc/127 * (dremelJointSpeedMax - dremelJointSpeedMin) + dremelJointSpeedMin
    dxlIO.set_moving_speed({dremelMotorId: speed})

def updateWheelSpeeds():
    global wheelSpeed, leftWheelSlowdown, rightWheelSlowdown, leftWheelMotorId, rightWheelMotorId
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
    print 'Connected'
    # Setup motors
    dxlIO.enable_torque([leftWheelMotorId, rightWheelMotorId, dremelMotorId])
    dxlIO.set_moving_speed({dremelMotorId: dremelJointSpeedMin})
    # Init OSC server
    simpleOSC.initOSCServer(receiveAddress, receivePort)
    simpleOSC.setOSCHandler('/wheelspeed', wheelSpeedHandler)
    simpleOSC.setOSCHandler('/wheelslowdown', wheelSlowdownHandler)
    simpleOSC.setOSCHandler('/dremeljointpos', dremelJointPosHandler)
    simpleOSC.setOSCHandler('/dremeljointspeed', dremelJointSpeedHandler)
    simpleOSC.startOSCServer()
    # Enter infinite loop to be able to catch KeyboardInterrupt
    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
        simpleOSC.closeOSC()

# Launch the app
if __name__ == '__main__': app()