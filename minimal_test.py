import pypot.dynamixel

try:
    with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:
        print("Scanning for motors...")
        ids = dxl_io.scan()
        print(f"Detected motor IDs: {ids}")
except Exception as e:
    print(f"Error: {e}")
