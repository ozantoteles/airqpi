# Import specific modules for each sensor driver
from .cm1107_driver import init as init_cm1107, read as read_cm1107
# from .pm2008_driver import init as init_pm2008, read as read_pm2008
# from .sht4x_driver import init as init_sht4x, read as read_sht4x
# from .sht3x_driver import init as init_sht3x, read as read_sht3x
# from .sfa30_driver import init as init_sfa30, read as read_sfa30
# from .sgp4x_driver import init as init_sgp4x, read as read_sgp4x

# Define any variables or constants that are relevant to the package.
SENSOR_TYPES = ['cm1107', 'pm2008', 'sht4x', 'sht3x', 'sfa30', 'sgp4x']

# Initialize logging
import logging

# Configure the logging module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Leave this file empty/commented if there's no specific initialization code needed.
