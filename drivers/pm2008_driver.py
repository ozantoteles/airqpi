# -*- coding: utf-8 -*-

import smbus
import logging

#for reference to Wuhan Cubic PM2008 sensor look at https://en.gassensor.com.cn/Product_files/Specifications/PM2008M-M%20Laser%20Particle%20Sensor%20Module%20Specification.pdf

# I2C address
PM2008 = (0x50 >>1)

# Sensor limits
data_upper_limit = 300
data_lower_limit = 0

# Prepare Open single measurement command and check sum bytes
# Datasheet 3.1 Send Command Data page:17
# Send by main controlled board:
# START+WRITE+ACK+P1+ACK+P2+ACK…… +P7+ACK+STOP
p1=0x16 # Frame header
p2=7    # Number of byte, not including length of device address (From P1 to P7, 7 bytes in total)
p3=2    # Data 1
p4=0xFF # Data 2, high byte
p5=0xFF # Data 2, low byte
p6=0xFF # Data 3
p7=p1^p2^p3^p4^p5^p6    # Data check code

def delay_sec(count):
    while(count>1):
        count=count-1

def init(busNo):
    
    bus = smbus.SMBus(busNo)
    return bus

def read(bus):
    """
    Datasheet 3.2 Read Data Command
    Send by main controlled board:
    START+READ+ACK+P1+ACK+P2+ACK+……+P32+NACK+STOP

    "Data"	"Byte Content"	"Description"
    "Device address"	"Sensor address and read/write command"	"This byte is 0x51 when read data"
    P1	0x16	Frame header
    P2	Frame length	Number of bytes, not including length of device address (from P1 to P32, 32 bytes in total)
    P3	Sensor status	Close: 1; Alarm: 7; Measuring: 2; Data stable: 0x80 (only for dynamic or timing measuring mode). Other data is invalid.(Check 3.3 detailed introduction for every kinds of measurement mode)
    P4	Data 1, high byte	The measuring mode of sensor as: Single measuring mode: 2; Continuous measuring mode: 3 Dynamic measuring mode: 5; Timing measuring mode: >= 60 (means measuring period)
    P5	Data 1, low byte	
    P6	Data 2, high byte	Calibration coefficient: (Range: 70~150, Corresponding: 0.7~1.5）
    P7	Data 2, low byte	
    P8	Data 3, high byte	PM1.0 concentration, unit: μg/m³, GRIMM
    P9	Data 3, low byte	
    P10	Data 4, high byte	PM2.5 concentration, unit: μg/m³, GRIMM
    P11	Data 4, low byte
    P12	Data 5, high byte	PM10 concentration, unit: μg/m³, GRIMM
    P13	Data 5, low byte	
    P14	Data 6, high byte	PM1.0 concentration, unit: μg/m³, TSI
    P15	Data 6, low byte	
    P16	Data 7, high byte	PM2.5 concentration, unit: μg/m³, TSI
    P17	Data 7, low byte	
    P18	Data 8, high byte	PM10 concentration, unit: μg/m³ , TSI
    P19	Data 8, low byte	
    P20	Data 9, high byte	Number of PM0.3, unit: pcs/0.1L
    P21	Data 9, low byte	
    P22	Data 10, high byte	Number of PM0.5, unit: pcs/0.1L
    P23	Data 10, low byte	
    P24	Data 11, high byte	Number of PM1.0, unit: pcs/0.1L
    P25	Data 11, low byte	
    P26	Data 12, high byte	Number of PM2.5, unit: pcs/0.1L
    P27	Data 12, low byte	
    P28	Data 13, high byte	Number of PM5.0, unit: pcs/0.1L
    P29	Data 13, low byte	
    P30	Data 14, high byte	Number of PM10, unit: pcs/0.1L
    P31	Data 14, low byte	P32	Data check code Check code = (P1^P2^……^P31)
    """  
    #send measure command, page:17
    bus.write_i2c_block_data(PM2008,p1,[p2,p3,p4,p5,p6,p7])
    delay_sec(0xFFFF)
    #read sensor values, page:18
    data=bus.read_i2c_block_data(PM2008,0x00,32)
    bus.close()
    #print(data)
    #print("PM2008 Status Byte: ",data[2])
    #print("PM1.0 GRIMM:",256*data[7]+data[8])
    #print("PM2.5 GRIMM:",256*data[9]+data[10])
    #print("PM 10 GRIMM:",256*data[11]+data[12])
    #print("PM1.0 TSI  :",256*data[13]+data[14])
    #print("PM2.5 TSI  :",256*data[15]+data[16])
    #print("PM 10 TSI  :",256*data[17]+data[18])
    #print("PM0.3 L    :",256*data[19]+data[20])
    #print("PM0.5 L    :",256*data[21]+data[22])
    #print("PM1.0 L    :",256*data[23]+data[24])
    #print("PM2.5 L    :",256*data[25]+data[26])
    #print("PM  5 L    :",256*data[27]+data[28])
    #print("PM 10 L    :",256*data[29]+data[30])
    #print()

    # Check status byte and return -999 if not measuring
    if data[2] != 2:
        pm2008SensorVals = {
            "PM2008_1_0_GRIMM_LEVEL": -999,
            "PM2008_2_5_GRIMM_LEVEL": -999,
            "PM2008_10_GRIMM_LEVEL": -999,
            "PM2008_1_0_TSI_LEVEL": -999,
            "PM2008_2_5_TSI_LEVEL": -999,
            "PM2008_10_TSI_LEVEL": -999,
            "PM2008_0_3_L_LEVEL": -999,
            "PM2008_0_5_L_LEVEL": -999,
            "PM2008_1_0_L_LEVEL": -999,
            "PM2008_2_5_L_LEVEL": -999,
            "PM2008_5_L_LEVEL": -999,
            "PM2008_10_L_LEVEL": -999
        }
    else:
        pm2008SensorVals = {}
        pm2008SensorVals["PM2008_1_0_GRIMM_LEVEL"] = 256*data[7]+data[8]
        pm2008SensorVals["PM2008_2_5_GRIMM_LEVEL"] = 256*data[9]+data[10]
        pm2008SensorVals["PM2008_10_GRIMM_LEVEL"] = 256*data[11]+data[12]
        pm2008SensorVals["PM2008_1_0_TSI_LEVEL"] = 256*data[13]+data[14]
        pm2008SensorVals["PM2008_2_5_TSI_LEVEL"] = 256*data[15]+data[16]
        pm2008SensorVals["PM2008_10_TSI_LEVEL"] = 256*data[17]+data[18]
        pm2008SensorVals["PM2008_0_3_L_LEVEL"] = 256*data[19]+data[20]
        pm2008SensorVals["PM2008_0_5_L_LEVEL"] = 256*data[21]+data[22]
        pm2008SensorVals["PM2008_1_0_L_LEVEL"] = 256*data[23]+data[24]
        pm2008SensorVals["PM2008_2_5_L_LEVEL"] = 256*data[25]+data[26]
        pm2008SensorVals["PM2008_5_L_LEVEL"] = 256*data[27]+data[28]
        pm2008SensorVals["PM2008_10_L_LEVEL"] = 256*data[29]+data[30]

    #return PM values
    return pm2008SensorVals

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        bus = init(1)
        pmVals = read(bus)
        
        logger.info(f'PM measurement: {pmVals}')
        
    except Exception as e:
        # Log any exceptions
        logger.error(f'An error occurred: {e}')

    return 0

if __name__ == '__main__':
    main()      