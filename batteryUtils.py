import logging
from drivers.bq25887_driver import init as init_bq25887, read as read_bq25887

busNR_BQ25887 = 1

class BatteryHandler:
    def __init__(self):
        self.batData = {}

    def init_ic(self):
        try:
            self.busBQ25887 = init_bq25887(busNR_BQ25887)
            logging.info(f"BQ25887 initialized successfully.")
        except Exception as e:
            logging.info(f"Error initializing BQ25887: {e}")
            self.busBQ25887 = None

    def handler(self):

        if self.busBQ25887 is not None:
            try:
                dataBQ25887_perc, dataBQ25887_stat = read_bq25887(self.busBQ25887)
                self.batData["BQ25887_BAT_PERC"] = dataBQ25887_perc
                self.batData["BQ25887_STATUS"] = dataBQ25887_stat
            except Exception as e:    
                logging.info(f"Error reading BQ25887: {e}")
        
        return self.batData 

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info("Starting Battery Application")

    ic_object = BatteryHandler()
    ic_object.init_ic()

    try:
        bat_data = ic_object.handler()
        logging.info(f'Percentage: {bat_data["BQ25887_BAT_PERC"]}, Status: {bat_data["BQ25887_STATUS"]}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
