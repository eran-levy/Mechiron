import unittest
from mechiron.extractors.storesextractor import StoreExtractor
from mechiron.extractors.pricesgzextractor import PricesExtractor


class MyTestCase(unittest.TestCase):

    def test_extractstores(self):
        extractor = StoreExtractor("/home/eran/Downloads/mechiron-downloads/2016-10-16_07_48_06")
        extractor.extract_stores_to_csv()
        # self.assertEqual(True, False)

    def test_extractprices(self):
        prices_extractor = PricesExtractor("/home/eran/Downloads/mechiron-downloads/2016-10-16_07_48_06")
        prices_extractor.process_gz_files()

if __name__ == '__main__':
    unittest.main()
