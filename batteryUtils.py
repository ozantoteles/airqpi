import logging
from drivers.bq25887_driver import init as init_bq25887, read as read_bq25887

busNR_BQ25887 = 1


class BatteryHandler:
    def __init__(self):
        self.busBQ25887 = -1
        self.batData = {}

    def init_ic(self):
        try:
            self.busBQ25887 = init_bq25887(busNR_BQ25887)
        except Exception as e:
            logging.info(e)

    def handler(self):
    
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        dataBQ25887 = -999
        
        self.batData["BQ25887_BAT_PERC"] = -999
        self.batData["BQ25887_STATUS"] = -999

        if not self.busBQ25887 == -1:

            try:
                self.busBQ25887 = init_bq25887(busNR_BQ25887)
            except Exception as e:
                self.busBQ25887 = -1
                logger.info(e)

            try:
                dataBQ25887_perc, dataBQ25887_stat = read_bq25887(self.busBQ25887)
            except Exception as e:	
                logger.info(e)	                
        
        self.batData["BQ25887_BAT_PERC"] = dataBQ25887_perc
        self.batData["BQ25887_STATUS"] = dataBQ25887_stat
            
        return self.batData 

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    ic_object = BatteryHandler()
    ic_object.init_ic()

    try:
        bat_data = ic_object.handler()
        logger.info(f'Percentage: {bat_data["BQ25887_BAT_PERC"]}, Status: {bat_data["BQ25887_STATUS"]}')
    except Exception as e:
        logger.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()