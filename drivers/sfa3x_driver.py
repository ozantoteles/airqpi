# -*- coding: utf-8 -*-

import time
import smbus
import logging

# Sensor limits
data_upper_limit = 1000
data_lower_limit = 0

HCHO = 0x5D
HCHO_BUS = 1 #default

def calcHcho(hcho):
    # calculate temperature in degrees celcius, page: 14
    return (hcho/5.0)        

def calcTemp(temp):
    # calculate temperature in degrees celcius, page: 14
    return (temp/200.0)

def calcHum(hum):
    # calculate relative humidity, page: 14
    return (hum/100.0)

def sensor_reset(bus):   
    
    bus.write_byte_data(HCHO,0xD3, 0x04)
    time.sleep(0.5)
    logging.debug(f'Sensor reset performed')

def crc_value(data_tobe_sent):
    #calculate crc value for two bytes to be send, page 12
    crc=0x00
    crc= crc^0xFF
    for i in range (0,2):
        crc= crc^data_tobe_sent[i]
        for j in range (7,-1,-1):
            if ((crc & 0x80) == 0x80 ):
                crc = (crc <<1) ^ 0x31
            else:
                crc = (crc <<1)    
    return(crc & 0xFF)     

def get_sensor_device_marking(bus):  

    bus.write_byte_data(HCHO,0xD0,0x60)
    time.sleep(0.5)
    data=bus.read_i2c_block_data(HCHO,0x00,32)
    
    device_marking = ""
    
    for i in range(0, len(data), 3):
        if i+2 < len(data):  # Ensure there are enough elements to process
            byte1 = data[i]
            byte2 = data[i+1]
            checksum = data[i+2]
            
            # Verify checksum
            calculated_checksum = crc_value([byte1, byte2])
            
            if calculated_checksum == checksum and byte1 != 0 and byte2 != 0:
                device_marking += chr(byte1) + chr(byte2)
                
    logging.debug(f'SFA3x HCHO: {device_marking}')
    
    return(device_marking)

def measure_raw(bus):
   
    
    # Start continuous measurement
    bus.write_byte_data(HCHO,0x00,0x06)
    time.sleep(0.5)
    # Read measured values
    bus.write_byte_data(HCHO,0x03, 0x27)
    time.sleep(0.5)
    data=bus.read_i2c_block_data(HCHO,0x00,9)

    return data

def init(busNo):
    
    bus = smbus.SMBus(busNo)
    get_sensor_device_marking(bus)

    return bus

def read(bus):
    
    rawdata = measure_raw(bus)
    time.sleep(0.5)
    logging.debug(f'sfa3x Raw data {rawdata}')
    SFA30temp = calcTemp(256*rawdata[6]+rawdata[7])
    SFA30hum = calcHum(256*rawdata[3]+rawdata[4])
    SFA30hcho = calcHcho(256*rawdata[0]+rawdata[1])
    
    return SFA30temp, SFA30hum, SFA30hcho

def main():

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        bus = init(1)
        temp, hum, hcho = read(bus)
        
        # Log the temp, hum, hcho values, and device marking
        
        logging.info(f'SFA3x Temperature: {temp} C')
        logging.info(f'SFA3x Relative Humidity: {hum} %')
        logging.info(f'SFA3x HCHO: {hcho} ppb')
        
    
    except Exception as e:
        # Log any exceptions
        logging.error(f'An error occurred: {e}')

    return 0

if __name__ == '__main__':
    main()  

