from arduino_iot_cloud import ArduinoCloudClient, Task
from secrets import DEVICE_ID, SECRET_KEY
from sensorUtils import SensorHandler
from batteryUtils import BatteryHandler
import logging
import asyncio

sensor = SensorHandler()
sensor.init_sensors()
sensor_buffer = {}

charger = BatteryHandler()
charger.init_ic()
charger_buffer = {}

def configure_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

logger = configure_logger()

def update_sensor_values(client):
    global sensor_buffer
    try:
        sensor_data = sensor.handler()
        sensor_buffer = sensor_data  # Update the buffer with the latest sensor values
    except Exception as e:
        # Log any exceptions
        logger.error(f'An error occurred when updating sensor values: {e}')

def read_sensor_value(client, value_name):
    try:
        value = sensor_buffer.get(value_name)
        if value is not None:
            return value
        else:
            return 0  # Default value if key not found
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        
def update_charger_values(client):
    global charger_buffer
    try:
        charger_data = charger.handler()
        charger_buffer = charger_data  # Update the buffer with the latest sensor values
    except Exception as e:
        # Log any exceptions
        logger.error(f'An error occurred when updating charger values: {e}')

def read_charger_value(client, value_name):
    try:
        value = charger_buffer.get(value_name)
        if value is not None:
            return value
        else:
            return 0  # Default value if key not found
    except Exception as e:
        logger.error(f'An error occurred: {e}')
    
def main():
    
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    
    client.register(Task("update_sensor_values", on_run=update_sensor_values, interval=30.0))
    
    client.register(Task("update_charger_values", on_run=update_charger_values, interval=10.0))
    
    int_value_names = [
        "CM1107_CO2LEVEL", "PM2008_1_0_TSI_LEVEL", "PM2008_2_5_TSI_LEVEL", "PM2008_10_TSI_LEVEL",
        "PM2008_0_3_L_LEVEL", "PM2008_0_5_L_LEVEL", "PM2008_1_0_GRIMM_LEVEL", 
        "PM2008_1_0_L_LEVEL", "PM2008_2_5_GRIMM_LEVEL", "PM2008_2_5_L_LEVEL",
        "PM2008_5_L_LEVEL", "PM2008_10_GRIMM_LEVEL", "PM2008_10_L_LEVEL",  "SGP40_SRAW_VOC", "SGP40_VOC_INDEX"
    ]
    
    float_value_names = [
         "SFA3X_HCHO", "SFA3X_TEMP", "SFA3X_HUM", "SHT40_TEMP", "SHT40_HUM"
    ]
    
    int_charger_value_names = [
        "BQ25887_BAT_PERC", "BQ25887_STATUS"
    ]
    
    for value_name in int_value_names:
        client.register(value_name.lower(), value=None, on_read=lambda client, value_name=value_name: read_sensor_value(client, value_name), interval=30.0)
        
    for value_name in float_value_names:
        client.register(value_name.lower(), value=0.0, on_read=lambda client, value_name=value_name: read_sensor_value(client, value_name), interval=30.0)
    
    for value_name in int_charger_value_names:
        client.register(value_name.lower(), value=None, on_read=lambda client, value_name=value_name: read_charger_value(client, value_name), interval=10.0)
      
    
    client.start()

if __name__ == '__main__':
    main()