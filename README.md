# Air Quality Monitoring System

An air quality sensor device software project utilizing An air quality sensor device software project utilizing i2c sensors and other peripherals with Raspberry Pi Zero W. This repository contains drivers for various sensors used in an air quality monitoring system. Currently, it includes the driver for the CM1107 CO2 sensor.

## Installation

To use the sensor drivers, you'll need to install the required Python packages. You can do this using `pip`:
'pip install smbus2'
'pip install pytest'

This will install all the necessary dependencies for the sensor drivers.

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

## Contributing

If you'd like to contribute to this project by adding support for additional sensors or making improvements, please see our [contribution guidelines](docs/CONTRIBUTING.md).

License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
