import logging
import pypot.dynamixel

logging.basicConfig(level=logging.DEBUG)

def debug_motor():
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        raise IOError('No port available.')

    print(f"Available ports: {ports}")

    with pypot.dynamixel.DxlIO(ports[0], baudrate=57600) as dxl_io:
        print("Scanning for motors...")
        ids = dxl_io.scan(range(1, 253))
        print(f"Detected motor IDs: {ids}")

        if not ids:
            print("No motors detected. Check connections and power supply.")
        else:
            print("Motor detection successful.")

if __name__ == '__main__':
    try:
        debug_motor()
    except Exception as e:
        print(f"Error: {e}")