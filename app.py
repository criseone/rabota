import numpy
import time
import pypot.dynamixel
from pythonosc import dispatcher, osc_server, udp_client

# Settings
receiveAddress = "0.0.0.0"
receivePort = 8000
dremelJointSpeedMin = 100
dremelJointSpeedMax = 1024
dremelJointPosMin = 40
dremelJointPosMax = 53
wheelSpeedMax = 1024  # use symmetrically for min and max
wheelSlowdownMax = 1  # %, in range 0-1
leftWheelMotorId = 3
rightWheelMotorId = 2
dremelMotorId = 4

# Global variables
wheelSpeed = 0
leftWheelSlowdown = 0
rightWheelSlowdown = 0

def handle_sleep_data(address, *args):
    # Process sleep data and control robot accordingly
    print(f"Received sleep data: {args}")
    # Implement your logic based on the sleep data

def wheel_speed_handler(address, *args):
    global wheelSpeedMax, wheelSpeed
    value = args[0] + 0.0
    if value == 0:
        value = 1  # Fix problem with non-symmetrical values
    wheelSpeed = (value - 64) / 63 * wheelSpeedMax
    update_wheel_speeds()

def wheel_slowdown_handler(address, *args):
    global wheelSlowdownMax, leftWheelSlowdown, rightWheelSlowdown
    value = args[0] + 0.0
    if value == 0:
        value = 1  # Fix problem with non-symmetrical values
    slowdown = (value - 64) / 63 * wheelSlowdownMax
    if slowdown > 0:
        leftWheelSlowdown = slowdown
        rightWheelSlowdown = 0
    else:
        leftWheelSlowdown = 0
        rightWheelSlowdown = -slowdown
    update_wheel_speeds()

def dremel_joint_pos_handler(address, *args):
    global dxlIO, dremelJointPosMin, dremelJointPosMax, dremelMotorId
    value = args[0] + 0.0
    pos = value / 127 * (dremelJointPosMax - dremelJointPosMin) + dremelJointPosMin
    dxlIO.set_goal_position({dremelMotorId: -pos})

def dremel_joint_speed_handler(address, *args):
    global dxlIO, dremelJointSpeedMin, dremelJointSpeedMax, dremelMotorId
    value = args[0] + 0.0
    speed = value / 127 * (dremelJointSpeedMax - dremelJointSpeedMin) + dremelJointSpeedMin
    dxlIO.set_moving_speed({dremelMotorId: speed})

def stop_handler(address, *args):
    dxlIO.set_moving_speed({leftWheelMotorId: 0, rightWheelMotorId: 0})

def left_wheel_speed_handler(address, *args):
    dxlIO.set_moving_speed({leftWheelMotorId: args[0]})

def right_wheel_speed_handler(address, *args):
    dxlIO.set_moving_speed({rightWheelMotorId: args[0]})

def update_wheel_speeds():
    leftSpeed = wheelSpeed * (1 - leftWheelSlowdown)
    rightSpeed = wheelSpeed * (1 - rightWheelSlowdown)
    dxlIO.set_moving_speed({leftWheelMotorId: leftSpeed, rightWheelMotorId: rightSpeed})

def app():
    global dxlIO
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        raise IOError('No port available.')

    dxlIO = pypot.dynamixel.DxlIO(ports[0])
    ids = dxlIO.scan([leftWheelMotorId, rightWheelMotorId, dremelMotorId])
    if len(ids) < 3:
        raise IOError('Not all motors are connected.')

    dispatch = dispatcher.Dispatcher()
    dispatch.map("/wheelspeed", wheel_speed_handler)
    dispatch.map("/wheelslowdown", wheel_slowdown_handler)
    dispatch.map("/dremelpos", dremel_joint_pos_handler)
    dispatch.map("/dremelspeed", dremel_joint_speed_handler)
    dispatch.map("/stop", stop_handler)
    dispatch.map("/leftwheelspeed", left_wheel_speed_handler)
    dispatch.map("/rightwheelspeed", right_wheel_speed_handler)
    dispatch.map("/sleepdata", handle_sleep_data)

    server = osc_server.ThreadingOSCUDPServer((receiveAddress, receivePort), dispatch)
    print(f"Serving on {server.server_address}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == '__main__':
    app()