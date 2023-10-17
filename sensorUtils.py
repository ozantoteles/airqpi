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
        self.sensorData = {}
        
    def init_sensor(self, init_function, bus_number, sensor_name):
        try:
            sensor_bus = init_function(bus_number)
            logging.info(f"{sensor_name} initialized successfully.")
            return sensor_bus
        except Exception as e:
            logging.error(f"Error initializing {sensor_name}: {e}")
            return None
            
    def read_sensor(self, sensor_bus, read_function, sensor_name, *args):
        if sensor_bus is not None:
            try:
                data = read_function(sensor_bus, *args)
                return data
            except Exception as e:
                logging.error(f"Error reading {sensor_name}: {e}")
        else:
            logging.info(f"{sensor_name} not initialized. Cannot read data.")
            return None

    def init_sensors(self):
        self.busCM1107 = self.init_sensor(init_cm1107, busNR_CM1107, "CM1107")
        self.busPM2008 = self.init_sensor(init_pm2008, busNR_PM2008, "PM2008")
        self.busSFA3x = self.init_sensor(init_sfa3x, busNR_SFA3X, "SFA3x")
        self.busSHT40 = self.init_sensor(init_sht4x, busNR_SHT40, "SHT40")
        self.busSGP40 = self.init_sensor(init_sgp4x, busNR_SGP40, "SGP40")

    def handler(self):
        
        if self.busCM1107 is not None:
            dataCO2 = self.read_sensor(self.busCM1107, read_cm1107, "CM1107")
            self.sensorData["CM1107_CO2LEVEL"] = dataCO2
        
        if self.busPM2008 is not None:
            dataPM2008 = self.read_sensor(self.busPM2008, read_pm2008, "PM2008")
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
        
        if self.busSFA3x is not None:
            dataSFA3x = self.read_sensor(self.busSFA3x, read_sfa3x, "SFA3x")
            self.sensorData["SFA3X_HCHO"] = dataSFA3x[2]
            self.sensorData["SFA3X_TEMP"] = dataSFA3x[0]
            self.sensorData["SFA3X_HUM"] = dataSFA3x[1]
        
        if self.busSHT40 is not None:
            dataSHT40 = self.read_sensor(self.busSHT40, read_sht4x, "SHT40")
            self.sensorData["SHT40_TEMP"] = round(dataSHT40["SHT40_TEMP"],2)
            self.sensorData["SHT40_HUM"] = round(dataSHT40["SHT40_HUM"],2)
        
        if self.busSGP40 is not None:
            dataSGP40 = self.read_sensor(self.busSGP40, read_sgp4x, "SGP40", dataSHT40["SHT40_TEMP"], dataSHT40["SHT40_HUM"])
            self.sensorData["SGP40_SRAW_VOC"] = dataSGP40["SGP40_SRAW_VOC"]
            self.sensorData["SGP40_VOC_INDEX"] = dataSGP40["SGP40_VOC_INDEX"]

        return self.sensorData 

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info("Starting Sensor Application")

    sensor_object = SensorHandler()
    sensor_object.init_sensors()

    try:
        sensor_data = sensor_object.handler()
        logging.info(f'Measurements: {sensor_data}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()