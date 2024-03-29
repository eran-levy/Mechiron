__author__ = 'Eran Levy'

import os
import fnmatch
import re
import gzip
import csv
from xml.etree.ElementTree import fromstring, ElementTree
import logging
from datetime import datetime


class PricesExtractor(object):

    def __init__(self, download_folder):
        self.download_folder = download_folder + os.sep
        output_folder = self.download_folder + "output" + os.sep
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.csv_line_sep = "|"
        self.header_line = "chain_id,sub_chain_id,store_id,item_id,item_price,qty,manufacture_name" \
                           ",manufacture_country,manufacture_item_desc,item_name,item_code,price_update_date"
        self.current_time = str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))

    def process_gz_files(self):
        file_pattern = re.compile('Price.*')
        dirs = os.listdir(self.download_folder)
        for filename in dirs:
            if os.path.isdir(self.download_folder+filename):
                dir_to_process = self.download_folder+filename+os.sep
                logging.info("Starting to process " + filename + " in " + dir_to_process)
                # start to process each retail folder with all its pricess
                list_dir_to_process = os.listdir(dir_to_process)
                for file_to_process in list_dir_to_process:
                    if fnmatch.fnmatch(file_to_process, '*.gz') and file_pattern.match(file_to_process):
                        self._extract_prices_to_csv(dir_to_process+file_to_process, filename, self.output_folder)

    def _extract_prices_to_csv(self, fullpath, store_name, csv_output_folder):
        logging.info("Starting to process file: " + fullpath)
        input_file = gzip.open(fullpath, "rb")
        strdata = input_file.read()
        root = ElementTree(fromstring(strdata))
        itemscount = root.find(".//Items")
        num = itemscount.attrib.get("Count")
        if num > 0:
            csv_lines = []
            store_id = root.find(".//StoreId").text
            chain_id = root.find(".//ChainId").text
            sub_chain_id = root.find(".//SubChainId").text
            items_elem = root.findall(".//Items/Item")
            for item in items_elem:
                try:
                    price_update_date = item.find("PriceUpdateDate")
                    if price_update_date is not None and price_update_date.text is not None:
                        price_update_date = price_update_date.text
                    item_code = item.find("ItemCode")
                    if item_code is not None and item_code.text is not None:
                        item_code = item_code.text.encode('utf-8')
                    item_name = item.find("ItemName")
                    if item_name is not None and item_name.text is not None:
                        item_name = item_name.text.replace("#", "-").encode('utf-8')
                    manufacture_name = item.find("ManufacturerName")
                    if manufacture_name is not None and manufacture_name.text is not None:
                        manufacture_name = manufacture_name.text.replace("#", "-").encode('utf-8')
                    manufacture_country = item.find("ManufactureCountry")
                    if manufacture_country is not None and manufacture_country.text is not None:
                        manufacture_country = manufacture_country.text.replace("#", "-").encode('utf-8')
                    manufacture_item_desc = item.find("ManufacturerItemDescription")
                    if manufacture_item_desc is not None and manufacture_item_desc.text is not None:
                        manufacture_item_desc = manufacture_item_desc.text.replace("#", "-").encode('utf-8')
                    qty = item.find("Quantity")
                    if qty is not None and qty.text is not None:
                        qty = qty.text.encode('utf-8')
                    item_price = item.find("ItemPrice")
                    if item_price is not None and item_price.text is not None:
                        item_price = item_price.text.encode('utf-8')
                    item_id = item.find("ItemId")
                    if item_id is not None and item_id.text is not None:
                        item_id = item_id.text.encode('utf-8')

                    the_line = chain_id+self.csv_line_sep+sub_chain_id+self.csv_line_sep+store_id +\
                           self.csv_line_sep+item_id + self.csv_line_sep + item_price + self.csv_line_sep + \
                           qty + self.csv_line_sep + manufacture_name + self.csv_line_sep + manufacture_country + \
                           self.csv_line_sep + manufacture_item_desc + self.csv_line_sep + item_name + \
                           self.csv_line_sep + item_code + self.csv_line_sep + price_update_date
                    csv_lines.append(the_line.decode('utf-8').split(self.csv_line_sep))
                except TypeError, e:
                    logging.error(
                        "Got problem with one of the xml elements... Error: " + str(e))
                except AttributeError, e:
                    logging.error(
                        "Got problem with one of the xml elements and couldnt perform an action... Error: " + str(e))

            # file pattern -  retailname_yyyy-mm-dd_HH_MM_SS.csv
            full_output_filename = csv_output_folder+store_name+"_"+self.current_time+".csv"
            if not os.path.isfile(full_output_filename):
                with open(full_output_filename, "wb") as outfile:
                    logging.info(full_output_filename + " not exists, writing a new file")
                    writer = csv.writer(outfile, delimiter=self.csv_line_sep)
                    writer.writerow(self.header_line.split(","))
                    for line in csv_lines:
                        writer.writerow([unicode(s).encode('utf-8') for s in line])
            else:
                with open(full_output_filename, "a") as outfile:
                    logging.info("Writing to file: " + full_output_filename)
                    writer = csv.writer(outfile, delimiter=self.csv_line_sep)
                    for line in csv_lines:
                        writer.writerow([unicode(s).encode('utf-8') for s in line])
                    logging.info("Finished writing to file: " + full_output_filename)