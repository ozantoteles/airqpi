# -*- coding: utf-8 -*-

import time
import os, csv
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection
from sensirion_i2c_sgp4x import Sgp40I2cDevice
from sensirion_gas_index_algorithm.voc_algorithm import VocAlgorithm
import logging

data_upper_limit = 500
data_lower_limit = 0

SGP4X = 0x59
SGP4X_BUS = '/dev/i2c-1'

#private functions

def configure_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

logger = configure_logger()

def init(busNo, bufferFolder='buffer'):
    
    i2c_transceiver = LinuxI2cTransceiver(busNo)
    sgp40 = Sgp40I2cDevice(I2cConnection(i2c_transceiver), slave_address=SGP4X)
    sgp40.get_serial_number()
    
    if not os.path.exists(bufferFolder):
        os.makedirs(bufferFolder)

    return sgp40

def read(sensor, temperature=25.0, humidity=50.0, bufferFolder='buffer/', bufferSize=5000, bufferFile='vochistory.csv'):
    
    logger.debug(f'temperature: {temperature}')
    logger.debug(f'humidity: {humidity}')
    
    sraw_voc = sensor.measure_raw(temperature, humidity)
    logger.debug(f'sraw_voc: {sraw_voc}')
    logger.debug(f'sraw_voc ticks: {sraw_voc.ticks}')
    
    sgp4x_data = {}
    sgp4x_data["SGP40_SRAW_VOC"] = sraw_voc.ticks
    
    file_path = os.path.join(bufferFolder, bufferFile)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # Create an empty file
    
    with open(file_path, 'r') as f:
        lenofraw = len(f.readlines())
    
    if lenofraw < bufferSize:
        with open(file_path, 'a') as fin:
            fin.write(str(sraw_voc.ticks) + "\n")
    else:
        with open(file_path, 'r') as fd:
            data = fd.readlines()[1:]
        with open(file_path, 'w') as fout:
            fout.writelines(data)
        with open(file_path, 'a') as fin:
            fin.write(str(sraw_voc.ticks) + "\n")
    
    with open(file_path, 'r') as fin:
        rawarray = fin.read().splitlines()
        
    voc_algorithm = VocAlgorithm()
    for rawdata in rawarray:
        voc_index = voc_algorithm.process(int(rawdata))
        
    sgp4x_data["SGP40_VOC_INDEX"] = voc_index
    
    return sgp4x_data 

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logging.getLogger().setLevel(logging.DEBUG)

    try:
        sgp40 = init(SGP4X_BUS)
        sgp40_data = read(sgp40)
        
        # Log the temp, hum, hcho values, and device marking
        
        logger.info(f'SHT40 SRAW VOC: {sgp40_data["SGP40_SRAW_VOC"]}')
        logger.info(f'SGP40 VOC INDEX: {sgp40_data["SGP40_VOC_INDEX"]}')
        
    
    except Exception as e:
        # Log any exceptions
        logger.error(f'An error occurred: {e}')

    return 0

if __name__ == '__main__':
    main() 



# # Connect to the I²C 1 port /dev/i2c-1
# with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:
    # # Create SGP40 device
    # sgp40 = Sgp40I2cDevice(I2cConnection(i2c_transceiver))

    # print("SGP40 Serial Number: {}".format(sgp40.get_serial_number()))

    # # Measure every second for one minute
    # for _ in range(60):
        # time.sleep(1)
        # sraw_voc = sgp40.measure_raw()
        # # use default formatting for printing output:
        # print("SRAW VOC: {}".format(sraw_voc))