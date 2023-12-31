# -*- coding: utf-8 -*-

import time
import smbus
import logging

#for reference to Wuhan Cubic CM1107 sensor look at https://en.gassensor.com.cn/Product_files/Specifications/CM1107N%20Dual%20Beam%20NDIR%20CO2%20Sensor%20Module%20Specification.pdf

CM1107 = 0x31 # The slave address is 0x31

# Sensor limits
data_upper_limit = 5000
data_lower_limit = 1 # read function returns 0 in case of a problem

# Commands, Datasheet 2.1 Statement of Measuring Command
read_cmd = 0x01 # Read measured result of CO2, Datasheet 2.2 Measuring Result
azs_cmd = 0x10  # Open/ Close ABC and set ABC parameter, Datasheet 2.3 Auto Zero Specification Setting 
clb_cmd = 0x03  # Calibrate concentration value of CO2, Datasheet 2.4 Calibration
swv_cmd = 0x1E  # Read software version, Datasheet 2.5 Read the Serial Number of the Sensor
sn_cmd = 0x1F   # Read the serial number of the sensor, Datasheet 2.6 Read Software Version

def init(busNo):
    """
    Initialize an SMBus object with the specified bus number, get sensor ID, and return the bus.

    Parameters:
    busNo (int): The bus number to initialize the SMBus object with.

    Returns:
    bus (smbus.SMBus): The initialized SMBus object.

    """
    bus = smbus.SMBus(busNo)
    get_serial_number(bus)
    # get_software_version(bus)
    return bus

def read(bus):
    """
    This function takes an smbus.SMBus object as its argument and uses it to 
    communicate with the sensor. It sends the command to measure the result, 
    waits for the sensor to finish measuring, reads the data from the sensor, 
    extracts the CO2 measuring result and status byte from the data, 
    calculates the checksum, and returns the CO2 measuring result and status 
    byte as a tuple. If there is a checksum error, 
    the function raises a ValueError.
    
    Datasheet:
    The master device should send command of measuring result. 
    Send: 0x01
    Response: [0x01][DF0][DF1][DF2][CS]  
    Note: 
    1. Sensor starts measuring result status once receiving the command 0x01. 
    After this, all the data which I2C read will be such status format data, 
    until the sensor receives new command or re-powering on. 
    2. Data format, master device receives DF0 first, 
    and then receives CS at last.

    Remark: CO2 measuring result 
    Status Byte: [DF0] [DF1]
    Decimal Effective Value Range: 0 ~ 5,000 ppm
    Relative Value: 0 ~ 5,000 ppm

    CO2 measuring result: DF0*256+DF1, Fixed output is 550ppm during preheating period.

    Status Byte
    Bit7: Reserved
    Bit6:   1: Drift 
            0: Normal
    Bit5:   1: Light Aging
            0 Normal
    Bit4:   1: Non- calibrated
            0: Calibrated
    Bit3:   1: Less than Measurement Range
            0: Normal 
    Bit2:   1: Over Measurement Range
            0: Normal 
    Bit1:   1: Sensor Error
            0: Operating Normal
    Bit0:   1: Preheating
            0: Preheat complete

    Example: The master device reads some data: Read 3 bit. 
    0x01 0x03 0x20 0x00 0xDC
    CO2 measuring result = (0x03 0x20) hexadecimal = (800) decimal = 800 ppm
    Status bit: 0x00 means working normally
    [CS]= -(0x01+0x03+0x20+0x00)   Only keep the lowest bite.
    """
    
    """ bus.write_byte(CM1107,read_cmd) 
    time.sleep(0.5)
    data=bus.read_i2c_block_data(CM1107,read_cmd,4)
    bus.close()

    #print(data)

    CM1107data = 256*data[2]+data[3]
    #print(CM1107data)

    return CM1107data """

    # Send command to measure result
    bus.write_byte(CM1107,read_cmd)
    
    # Wait for the sensor to finish measuring
    time.sleep(0.5)
    
    # Read data from the sensor
    data = bus.read_i2c_block_data(CM1107, read_cmd, 5)
    
    logging.debug(f'cm1104 read data: {data}')

    # print("data: ", data)

    # print("data[0]: ", data[0],
    #       "data[1]: ", data[1],
    #       "data[2]: ", data[2],
    #       "data[3]: ", data[3],
    #       "data[4]: ", data[4],)
    
    
    # Extract status byte from data
    status_byte = data[3]
    bit7 = (status_byte & 0b10000000) >> 7
    bit6 = (status_byte & 0b01000000) >> 6
    bit5 = (status_byte & 0b00100000) >> 5
    bit4 = (status_byte & 0b00010000) >> 4
    bit3 = (status_byte & 0b00001000) >> 3
    bit2 = (status_byte & 0b00000100) >> 2
    bit1 = (status_byte & 0b00000010) >> 1
    bit0 = status_byte & 0b00000001

    # Extract CO2 measuring result from data
    if bit1 == 1:
        logging.error("Error: Sensor error detected")
        return None
    elif bit2 == 1:
        logging.error("Error: Measurement range over range")
        return data_upper_limit
    elif bit3 == 1:
        logging.error("Error: Measurement range less than range")
        return data_lower_limit
    else:
        co2 = (data[1] << 8) + data[2]
        logging.debug(f'co2:  {co2}')
        return co2 

    # Print the status bits (optional)
    # print("Status Byte: {}".format(status_byte))
    # print("Bit 7: Reserved: {}".format(bit7))
    # print("Bit 6: Drift: {}".format('Detected' if bit6 == 1 else 'Not detected'))
    # print("Bit 5: Light Aging: {}".format('Detected' if bit5 == 1 else 'Not detected'))
    # print("Bit 4: Calibration: {}".format('Not calibrated' if bit4 == 1 else 'Calibrated'))
    # print("Bit 3: Measurement Range: {}".format('Less than range' if bit3 == 1 else 'Normal'))
    # print("Bit 2: Measurement Range: {}".format('Over range' if bit2 == 1 else 'Normal'))
    # print("Bit 1: Sensor Error: {}".format('Error' if bit1 == 1 else 'Normal'))
    # print("Bit 0: Preheating: {}".format('In progress' if bit0 == 1 else 'Complete'))

    # Sensor checksum is not valid for current hw/sw version, 
    # checksum control would be implemented later
    
    # Calculate checksum
    # cs = -(sum(data) & 0xFF)
    
    # Check if checksum is correct
    # if cs != data[4]:
    #     print("cs: ", cs)
    #     print("data[3]: ", data[4])
    #     raise ValueError("Checksum error")

    # return co2, status_byte # status byte handling is done inside the function for now

def get_serial_number(bus):
    """
    Sends the command 0x1F to the CM1107 sensor to get the serial number.

    Args:
        bus (smbus.SMBus): The I2C bus object to communicate with the sensor.

    Returns:
        str: The 20-digit serial number of the sensor.

    Datasheet:
    Send: 0x1F 
    Response: [0x1F] [DF0] [DF1] [DF2] [DF3] [DF4] [DF5] [DF6] [DF7] [DF8] [DF9] [CS] 
    Note: 
    1. Sensor starts device code output status once receiving the command 0x1F. 
    After this, all the data which I²C read will be such status format data, 
    until the sensor receives new command or re-powering on. 
    2. Data format, the master device receives [DF0] first, and then receives [CS] at last. 
    High bit in front. 
    [DF0][DF1]: Integer type 1 (0-9999)
    [DF2][DF3]: Integer type 2 (0-9999)
    [DF4][DF5]: Integer type 3 (0-9999)
    [DF6][DF7]: Integer type 4 (0-9999)
    [DF8][DF9]: Integer type 5 (0-9999)
    3. The five-integer types constitute serial number of 20 digits. 
    """

    # Send the command 0x1F to the sensor
    bus.write_byte(CM1107, sn_cmd)

    # Read the response data
    data = bus.read_i2c_block_data(CM1107, sn_cmd)

    # Extract the 5 integers from the response data
    int1 = (data[1] << 8) | data[2]
    int2 = (data[3] << 8) | data[4]
    int3 = (data[5] << 8) | data[6]
    int4 = (data[7] << 8) | data[8]
    int5 = (data[9] << 8) | data[10]

    # Combine the 5 integers to form the serial number
    serial_number = '{:04d}{:04d}{:04d}{:04d}{:04d}'.format(int1, int2, int3, int4, int5)
    # print("CM1107 Serial Number: ", serial_number)

    return serial_number

def get_software_version(bus):
    """
    Datasheet:
    Send: 0x1E Response: [0x1E] [DF0] [DF1] [DF2] [DF3] [DF4] [DF5] [DF6] [DF7] [DF8] [DF9] [CS] 
    Note:  
    1. Sensor starts software version output status once receiving the command 0x1E. 
    After this, all the data which I2C read will be such status format data, 
    until the sensor receives new command or re-powering on. 
    2. Data format, the master device receives DF0 first, and then receives CS at last. 
    [DF0] …… [DF9] is ASCII. 
    """

    # Send the command 0x1F to the sensor
    bus.write_byte(CM1107, swv_cmd)

    # Read the response data
    data = bus.read_i2c_block_data(CM1107, swv_cmd, 11)
    # print("data: ", data)

    # convert the ASCII data to a string
    software_version = ''.join([chr(d) for d in data[1:-1]])
    # print("CM1107 Software Verson: ", software_version)

    return software_version

def main():

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        bus = init(1)
        co2 = read(bus)
        serial_number = get_serial_number(bus)
        software_version = get_software_version(bus)
        
        # Log the CO2 value, serial number and sensor software version
        logging.info(f'CO2 measurement: {co2} ppm')
        logging.info(f'Serial Number: {serial_number}')
        logging.info(f'Software Version: {software_version}')
    
    except Exception as e:
        # Log any exceptions
        logging.error(f'An error occurred: {e}')

    return 0

if __name__ == '__main__':
    main()
        
