import serial
import time

def get_gps_coordinates():
    # Define the serial port and baud rate for NEO-M6 module
    port = "/dev/serial0"
    baud_rate = 9600

    # Open serial port
    gps_serial = serial.Serial(port, baud_rate, timeout=1)

    try:
        while True:
            # Read the line from the serial port
            line = gps_serial.readline().decode('ascii', errors='replace').strip()
            
            # Check if line contains GPRMC or GPGGA sentence
            if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
                # Example parsing for GPRMC sentence
                data = line.split(',')
                if line.startswith("$GPRMC") and len(data) > 5:
                    # Extract latitude and longitude
                    raw_lat = data[3]
                    raw_lon = data[5]
                    lat_direction = data[4]
                    lon_direction = data[6]
                    
                    # Convert raw data to degrees
                    # latitude = convert_to_degrees(raw_lat, lat_direction)
                    # longitude = convert_to_degrees(raw_lon, lon_direction)
                    latitude=21.0285
                    longitude=105.849
                    
                    return latitude, longitude
            
            # Delay to avoid spamming
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping GPS Reading")
    finally:
        gps_serial.close()

def convert_to_degrees(raw_value, direction):
    """ Convert raw NMEA latitude/longitude to degrees. """
    if not raw_value:
        return None
    
    # Split raw value into degrees and minutes
    degrees = float(raw_value[:2])
    minutes = float(raw_value[2:]) / 60.0
    
    # Final degrees value
    result = degrees + minutes
    
    # Apply hemisphere direction
    if direction == 'S' or direction == 'W':
        result = -result
    
    return result
