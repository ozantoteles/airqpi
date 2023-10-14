import logging
from drivers.cm1107_driver import init as init_cm1107, read as read_cm1107
from drivers.pm2008_driver import init as init_pm2008, read as read_pm2008

busNR_CM1107 = 1
busNR_PM2008 = 1

class SensorHandler:
    def __init__(self):
        self.busCM1107 = -1
        self.busPM2008 = -1
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

    def handler(self):
    
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        dataCO2 = -999
        dataPM2008 = -999

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
        
        self.sensorData["CO2LEVEL"] = dataCO2

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