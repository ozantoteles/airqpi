# -*- coding: utf-8 -*-

import time
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_sht.sht4x.device import Sht4xI2cDevice
import logging

temp_data_upper_limit = 125
temp_data_lower_limit = -40
hum_data_upper_limit = 100
hum_data_lower_limit = 0

SHT40 = 0x45
SHT40_BUS = '/dev/i2c-1'

#private functions

def configure_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

logger = configure_logger()

def init(busNo):
    
    i2c_transceiver = LinuxI2cTransceiver(busNo)
    sht40 = Sht4xI2cDevice(I2cConnection(i2c_transceiver), slave_address=SHT40)
    sht40.read_serial_number()

    return sht40

def read(sensor):
    
    temperature, humidity = sensor.single_shot_measurement()
    logger.debug(f'Temperature: {temperature}, humidity: {humidity}')
    
    logger.debug(f'SHT40 Temperature ticks: {temperature.ticks}')
    logger.debug(f'SHT40 Temperature celcius: {temperature.degrees_celsius}')
    logger.debug(f'SHT40 Temperature fahrenheit: {temperature.degrees_fahrenheit}')
    logger.debug(f'SHT40 Relative Humidity ticks: {humidity.ticks}')
    logger.debug(f'SHT40 Relative Humidity %RH: {humidity.percent_rh}')
    
    sht4x_data = {}
    sht4x_data["SHT40_TEMP"] = temperature.degrees_celsius
    sht4x_data["SHT40_HUM"] = humidity.percent_rh
    
    return sht4x_data 

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logging.getLogger().setLevel(logging.DEBUG)

    try:
        sht40 = init(SHT40_BUS)
        sht40_data = read(sht40)
        
        # Log the temp, hum, hcho values, and device marking
        
        logger.info(f'SHT40 Temperature: {sht40_data["SHT40_TEMP"]}')
        logger.info(f'SHT40 Relative Humidity: {sht40_data["SHT40_HUM"]}')
        
    
    except Exception as e:
        # Log any exceptions
        logger.error(f'An error occurred: {e}')

    return 0

if __name__ == '__main__':
    main() 
    