__author__ = 'Eran Levy'

import csv
import os
import re
import xml.etree.ElementTree as ETree
import fnmatch
import logging


class StoreExtractor(object):

    def __init__(self, download_folder):
        self.download_folder = download_folder + os.sep
        output_folder = self.download_folder + "output" + os.sep
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.csv_line_sep = "#"
        self.header_row = "chain_id,chain_name,store_id,store_name,store_address,store_city,store_zipcode"

    def extract_stores_to_csv(self):
        logging.info("Starting stores extractor...")
        file_pattern = re.compile('Stores.*')
        csv_lines = []
        dirs = os.listdir(self.download_folder)
        for filename in dirs:
            if os.path.isdir(self.download_folder + filename):
                dir_to_process = self.download_folder + filename + os.sep
                logging.info("Starting to process " + filename + " in " + dir_to_process)
                # start to process each retail folder with all its pricess
                list_dir_to_process = os.listdir(dir_to_process)
                for file_to_process in list_dir_to_process:
                    if fnmatch.fnmatch(file_to_process, '*.xml') and file_pattern.match(file_to_process):
                        root = ETree.parse(dir_to_process+file_to_process)
                        chain_id = root.find(".//ChainId").text
                        chain_name = root.find(".//ChainName").text.encode('windows-1255')
                        items_elem = root.findall(".//Stores/Store")
                        for item in items_elem:
                            store_id = item.find("StoreId")
                            if store_id is not None:
                                store_id = store_id.text.encode('windows-1255')
                            store_name = item.find("StoreName")
                            if store_name is not None:
                                store_name = store_name.text.replace("\"", "").encode('windows-1255')
                            store_address = item.find("Address")
                            if store_address is not None:
                                store_address = store_address.text.replace("\"", "").encode('windows-1255')
                            # if city is unknown set to Address value
                            store_city = item.find("City")
                            if store_city is not None:
                                store_city = store_city.text.encode('windows-1255')
                            store_zipcode = item.find("ZipCode")
                            if store_zipcode is not None:
                                store_zipcode = store_zipcode.text.encode('windows-1255')

                            the_line = chain_id + self.csv_line_sep + chain_name + self.csv_line_sep + store_id + \
                                       self.csv_line_sep + store_name + self.csv_line_sep \
                                       + store_address + self.csv_line_sep + store_city + self.csv_line_sep + \
                                       store_zipcode
                            csv_lines.append(the_line.split(self.csv_line_sep))
                logging.info("Successfuly processed file: " + filename + " in " + dir_to_process)

                csv_file = self.output_folder + "stores.csv"
                logging.info("Writing file: " + csv_file)
                with open(csv_file, "wb") as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(self.header_row.split(","))
                    for line in csv_lines:
                        writer.writerow(line)
                    logging.info("Finished writing to file: " + csv_file)