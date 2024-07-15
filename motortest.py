import time
import pypot.dynamixel

# Motor IDs (replace with your actual motor IDs)
leftWheelMotorId = 3
rightWheelMotorId = 2
dremelMotorId = 4

# Function to initialize and test the motors
def test_motors():
    # Get available ports
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        raise IOError('No port available.')

    # Initialize the first available port
    with pypot.dynamixel.DxlIO(ports[0]) as dxl_io:
        # Scan for connected motors
        ids = dxl_io.scan([leftWheelMotorId, rightWheelMotorId, dremelMotorId])
        if len(ids) < 3:
            raise IOError('Not all motors are connected.')

        print(f"Connected motors: {ids}")

        # Set the speed for each motor
        dxl_io.set_moving_speed({leftWheelMotorId: 100, rightWheelMotorId: 100, dremelMotorId: 100})

        # Set the goal position for each motor
        print("Moving motors to initial positions...")
        dxl_io.set_goal_position({leftWheelMotorId: 45, rightWheelMotorId: 45, dremelMotorId: 45})
        time.sleep(2)

        # Test left wheel motor
        print("Testing left wheel motor...")
        dxl_io.set_goal_position({leftWheelMotorId: 90})
        time.sleep(1)
        dxl_io.set_goal_position({leftWheelMotorId: 0})
        time.sleep(1)

        # Test right wheel motor
        print("Testing right wheel motor...")
        dxl_io.set_goal_position({rightWheelMotorId: 90})
        time.sleep(1)
        dxl_io.set_goal_position({rightWheelMotorId: 0})
        time.sleep(1)

        # Test dremel motor
        print("Testing dremel motor...")
        dxl_io.set_goal_position({dremelMotorId: 90})
        time.sleep(1)
        dxl_io.set_goal_position({dremelMotorId: 0})
        time.sleep(1)

        # Stop all motors
        dxl_io.set_moving_speed({leftWheelMotorId: 0, rightWheelMotorId: 0, dremelMotorId: 0})
        print("Motor test completed.")

if __name__ == '__main__':
    test_motors()
