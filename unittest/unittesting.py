import repackage
repackage.up()

import json
import inspect
import functools
import logging
import unittest
import pandas as pd
from libs.treat_files import init_new_df, complete_new_df_debug


with open("unittest/log.json") as config_file:
    data = json.load(config_file) # Get config

# Setup logging 
logger = logging.getLogger("log")
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("unittest/unittesting.log")
fileHandler.setLevel(getattr(logging, data["log_level_file"]))

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(getattr(logging, data["log_level_console"]))

formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s (L.%(lineno)s - %(real_func_name)s())")
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

# Create ok and error datasets
df_b_ok = pd.read_csv("unittest/base-ic-couples-familles-menages-2017.CSV", sep=";", low_memory=False)
df_b_error = pd.read_csv("unittest/base-ic-logement-2017.CSV", sep=";", low_memory=False)

df_ok_col = ["C17_FAM", "C17_COUPAENF", "C17_FAMMONO", "C17_COUPSENF"]
df_error_col = ["P17_RP_PROP", "P17_RP_LOC", "P17_RP_LOCHLMV", "P17_RP_GRAT"]

df_ok = init_new_df(df_b_ok, df_ok_col)
df_error = init_new_df(df_b_error, df_error_col)

df_ok_complete_sum_min = min(complete_new_df_debug(df_ok, 3, "fr_co#")["sum"])
df_ok_complete_sum_max = max(complete_new_df_debug(df_ok, 3, "fr_co#")["sum"])

df_error_complete_sum_min = min(complete_new_df_debug(df_error, 4, "fr_oc#")["sum"])
df_error_complete_sum_max = max(complete_new_df_debug(df_error, 4, "fr_oc#")["sum"])

with open("config.json") as config_file:
    data = json.load(config_file) # Get all urls

data_lenght = len(data)


def log_message(function):

    @functools.wraps(function)
    def new_function(self, *args, **kwargs):
        try:
            function(self, *args, **kwargs)
            logger.info("OK", extra={'real_func_name': function.__name__})
        except Exception as e:
            logger.error(e, extra={'real_func_name': function.__name__})
        
    return new_function


# Make the test
class TestSum(unittest.TestCase):
    
    @log_message
    def test_ok_min(self):
        self.assertAlmostEqual(df_ok_complete_sum_min, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
        
    @log_message
    def test_ok_max(self):
        self.assertAlmostEqual(df_ok_complete_sum_max, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
        
    @log_message
    def test_error_min(self):
        self.assertNotAlmostEqual(df_error_complete_sum_min, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
        
    @log_message
    def test_error_max(self):
        self.assertNotAlmostEqual(df_error_complete_sum_max, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
            

class TestUrls(unittest.TestCase):
    
    @log_message
    def test_len_of_urls(self):
        self.assertEqual(data_lenght, 9, "Should be equal to 9")


if __name__ == '__main__':
    logger.info("Starting...", extra={'real_func_name': "__main__"})
    unittest.main(exit=False)
    logger.info("Finished!", extra={'real_func_name': "__main__"})
    
# si il n'y pas tous les liens dans le json remonter un erreur
