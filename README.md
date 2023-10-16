# A Raspberry Pi-based Air Quality Monitor Project

An air quality sensor device software project utilizing a Raspberry Pi, Python, and connected sensors. This repository contains drivers for various sensors used in an air quality monitoring system.

## Installation

To use the sensor drivers, you'll need to install the required Python packages. You can do this using `pip`:

```bash
pip install smbus2
pip install pytest
```

This will install all the necessary dependencies for the sensor drivers.

## Libraries

The arduino_iot_cloud, senml, and cbor2 libraries have been included from [Arduino IoT Cloud Python client](https://github.com/arduino/ararduduino-iot-cloud-py/tree/main).

## Available Sensor Drivers
### CM1107 CO2 Sensor
The CM1107 CO2 sensor driver allows you to communicate with the CM1107 sensor over I2C. It provides functions to initialize the sensor, read CO2 levels, and retrieve the sensor's serial number.

Usage example:
```
from drivers.cm1107_driver import init, read

bus = init(1)
co2_level = read(bus)
print(f"CO2 Level: {co2_level} ppm")
```
For detailed usage instructions, refer to the [CM1107 driver documentation](https://en.gassensor.com.cn/Product_files/Specifications/CM1107N%20Dual%20Beam%20NDIR%20CO2%20Sensor%20Module%20Specification.pdf).

### PM2008M-M Particulate Matter Sensor
The PM2008M PM sensor driver allows you to communicate with the PM2008M sensor over I2C. It provides functions to initialize the sensor, read PM levels, and retrieve the sensor's serial number.

Usage example:
```
from drivers.pm2008_driver import init, read

bus = init(1)
pmVals = read(bus)
print(f'PM measurement: {pmVals}')
```
For detailed usage instructions, refer to the [PM2008M-M driver documentation](https://en.gassensor.com.cn/Product_files/Specifications/PM2008M-M%20Laser%20Particle%20Sensor%20Module%20Specification.pdf).

## Usage

To run the project, make sure you have the necessary credentials to connect Arduino IoT Cloud in the secrets.py file (DEVICE_ID and SECRET_KEY). Then, execute the main.py script:

```bash
python main.py
```

## Contributing

If you'd like to contribute to this project by adding support for additional sensors or making improvements, please see our [contribution guidelines](docs/CONTRIBUTING.md).

License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
