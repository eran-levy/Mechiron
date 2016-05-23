__author__ = 'Eran levy'

import ConfigParser
from datetime import datetime
import os
from mechiron.collector.ftpcollector import FtpCollector
from mechiron.extractors.storesextractor import StoreExtractor
from mechiron.extractors.pricesgzextractor import PricesExtractor
import logging


def main():
    logging.info("Starting dataflow...")
    config = ConfigParser.SafeConfigParser()
    config.read('mechiron-conf.cfg')
    url = config.get('general', 'ftpurl')
    download_folder = config.get('general', 'download-folder')
    retail_names = config.get('general', 'retails-to-process')
    current_time = str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
    retail_list = retail_names.split(',')
    base_folder = download_folder + os.sep + current_time
    num_processed = 0
    retails_to_process = len(retail_list)
    logging.info("Starting collection step...")
    # for each retail
    for name in retail_list:
        logging.info("Starting to collect: " + name)
        folder_for_collect = base_folder + os.sep + name
        if not os.path.exists(folder_for_collect):
            os.makedirs(folder_for_collect)
        user_str = config.get(name, 'user')
        password_str = ''
        if config.has_option(name, 'pass'):
            password_str = config.get(name, 'pass')

        collector = FtpCollector(folder_for_collect, url, user_str, password_str)
        collector.retrieve_files()
        logging.info("Finished to collect: " + name)
        num_processed += 1
    logging.info("Finished collection step...")
    if num_processed == retails_to_process:
        logging.info("Starting store extraction step...")
        # extract stores
        store_extractor = StoreExtractor(base_folder)
        store_extractor.extract_stores_to_csv()
        logging.info("Finished store extraction step...")

        logging.info("Starting prices extraction step...")
        # extract prices per each retail
        prices_extractor = PricesExtractor(base_folder)
        prices_extractor.process_gz_files()
        logging.info("Starting prices extraction step...")

if __name__ == '__main__':
    main()