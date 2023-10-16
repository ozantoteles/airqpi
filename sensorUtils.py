import logging
from drivers.cm1107_driver import init as init_cm1107, read as read_cm1107
from drivers.pm2008_driver import init as init_pm2008, read as read_pm2008
from drivers.sfa3x_driver import init as init_sfa3x, read as read_sfa3x
from drivers.sht4x_driver import init as init_sht4x, read as read_sht4x
from drivers.sgp4x_driver import init as init_sgp4x, read as read_sgp4x

busNR_CM1107 = 1
busNR_PM2008 = 1
busNR_SFA3X = 1
busNR_SHT40 = '/dev/i2c-1'
busNR_SGP40 = '/dev/i2c-1'

class SensorHandler:
    def __init__(self):
        self.busCM1107 = -1
        self.busPM2008 = -1
        self.busSFA3x = -1
        self.busSHT40 = -1
        self.busSGP40 = -1
        self.sensorData = {}

    def init_sensors(self):
        try:
            self.busCM1107 = init_cm1107(busNR_CM1107)
        except Exception as e:
            logging.info(e)

        try:
            self.busPM2008 = init_pm2008(busNR_PM2008)
        except Exception as e:
            logging.info(e)
            
        try:
            self.busSFA3x = init_sfa3x(busNR_SFA3X)
        except Exception as e:
            logging.info(e)
            
        try:
            self.busSHT40 = init_sht4x(busNR_SHT40)
        except Exception as e:
            logging.info(e)
            
        try:
            self.busSGP40 = init_sgp4x(busNR_SGP40)
        except Exception as e:
            logging.info(e)

    def handler(self):
    
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        dataCO2 = -999
        dataPM2008 = -999
        dataSFA3x = -999
        dataSHT40 = -999
        dataSGP40 = -999
        
        self.sensorData["CM1107_CO2LEVEL"] = -999

        self.sensorData["PM2008_1_0_TSI_LEVEL"] = -999
        self.sensorData["PM2008_2_5_TSI_LEVEL"] = -999
        self.sensorData["PM2008_10_TSI_LEVEL"] = -999
        self.sensorData["PM2008_0_3_L_LEVEL"] = -999
        self.sensorData["PM2008_0_5_L_LEVEL"] = -999
        self.sensorData["PM2008_1_0_GRIMM_LEVEL"] = -999
        self.sensorData["PM2008_1_0_L_LEVEL"] = -999
        self.sensorData["PM2008_2_5_GRIMM_LEVEL"] = -999
        self.sensorData["PM2008_2_5_L_LEVEL"] = -999
        self.sensorData["PM2008_5_L_LEVEL"] = -999
        self.sensorData["PM2008_10_GRIMM_LEVEL"] = -999
        self.sensorData["PM2008_10_L_LEVEL"] = -999
        
        self.sensorData["SFA3X_HCHO"] = -999
        self.sensorData["SFA3X_TEMP"] = -999
        self.sensorData["SFA3X_HUM"] = -999
        
        self.sensorData["SHT40_TEMP"] = -999
        self.sensorData["SHT40_HUM"] = -999
        
        self.sensorData["SGP40_SRAW_VOC"] = -999
        self.sensorData["SGP40_VOC_INDEX"] = -999

        if not self.busCM1107 == -1:

            try:
                self.busCM1107 = init_cm1107(busNR_CM1107)
            except Exception as e:
                self.busCM1107 = -1
                logger.info(e)

            try:
                dataCO2 = read_cm1107(self.busCM1107)
            except Exception as e:	
                logger.info(e)	                

        if not self.busPM2008 == -1:

            try:
                self.busPM2008 = init_pm2008(busNR_PM2008)
            except Exception as e:
                self.busPM2008 = -1
                logger.info(e)

            try:
                dataPM2008 = read_pm2008(self.busPM2008)
            except Exception as e:	
                logger.info(e)		
                
        if not self.busSFA3x == -1:

            try:
                self.busSFA3x = init_sfa3x(busNR_SFA3X)
            except Exception as e:
                self.busSFA3x = -1
                logger.info(e)

            try:
                dataSFA3x = read_sfa3x(self.busSFA3x)
            except Exception as e:	
                logger.info(e)
                
        if not self.busSHT40 == -1:

            try:
                self.busSHT40 = init_sht4x(busNR_SHT40)
            except Exception as e:
                self.busSHT40 = -1
                logger.info(e)

            try:
                dataSHT40 = read_sht4x(self.busSHT40)
            except Exception as e:	
                logger.info(e)
                
        if not self.busSGP40 == -1:

            try:
                self.busSGP40 = init_sgp4x(busNR_SGP40)
            except Exception as e:
                self.busSGP40 = -1
                logger.info(e)

            try:
                dataSGP40 = read_sgp4x(self.busSGP40, dataSHT40["SHT40_TEMP"],  dataSHT40["SHT40_HUM"])
            except Exception as e:	
                logger.info(e)
        
        self.sensorData["CM1107_CO2LEVEL"] = dataCO2

        if dataPM2008 != -1:
            self.sensorData["PM2008_1_0_TSI_LEVEL"] = dataPM2008["PM2008_1_0_TSI_LEVEL"]
            self.sensorData["PM2008_2_5_TSI_LEVEL"] = dataPM2008["PM2008_2_5_TSI_LEVEL"]
            self.sensorData["PM2008_10_TSI_LEVEL"] = dataPM2008["PM2008_10_TSI_LEVEL"]
            self.sensorData["PM2008_0_3_L_LEVEL"] = dataPM2008["PM2008_0_3_L_LEVEL"]
            self.sensorData["PM2008_0_5_L_LEVEL"] = dataPM2008["PM2008_0_5_L_LEVEL"] 
            self.sensorData["PM2008_1_0_GRIMM_LEVEL"] = dataPM2008["PM2008_1_0_GRIMM_LEVEL"]
            self.sensorData["PM2008_1_0_L_LEVEL"] = dataPM2008["PM2008_1_0_L_LEVEL"]
            self.sensorData["PM2008_2_5_GRIMM_LEVEL"] = dataPM2008["PM2008_2_5_GRIMM_LEVEL"]
            self.sensorData["PM2008_2_5_L_LEVEL"] = dataPM2008["PM2008_2_5_L_LEVEL"]
            self.sensorData["PM2008_5_L_LEVEL"] = dataPM2008["PM2008_5_L_LEVEL"]
            self.sensorData["PM2008_10_GRIMM_LEVEL"] = dataPM2008["PM2008_10_GRIMM_LEVEL"]
            self.sensorData["PM2008_10_L_LEVEL"] = dataPM2008["PM2008_10_L_LEVEL"]
            
        self.sensorData["SFA3X_HCHO"] = dataSFA3x[2]
        self.sensorData["SFA3X_TEMP"] = dataSFA3x[0]
        self.sensorData["SFA3X_HUM"] = dataSFA3x[1]
        
        self.sensorData["SHT40_TEMP"] = round(dataSHT40["SHT40_TEMP"],2)
        self.sensorData["SHT40_HUM"] = round(dataSHT40["SHT40_HUM"],2)  
        
        self.sensorData["SGP40_SRAW_VOC"] = dataSGP40["SGP40_SRAW_VOC"]
        self.sensorData["SGP40_VOC_INDEX"] = dataSGP40["SGP40_VOC_INDEX"]
            
        return self.sensorData 

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    sensor_object = SensorHandler()
    sensor_object.init_sensors()

    try:
        sensor_data = sensor_object.handler()
        logger.info(f'Measurements: {sensor_data}')
    except Exception as e:
        logger.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()