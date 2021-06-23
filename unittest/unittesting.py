import repackage
repackage.up()

import json
import inspect
import logging
import unittest
import pandas as pd
from libs.treat_files import init_new_df, complete_new_df_debug


with open("unittest/log.json") as config_file:
    data = json.load(config_file)

logger = logging.getLogger("log")
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("unittest/unittesting.log")
fileHandler.setLevel(getattr(logging, data["log_level_file"]))

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(getattr(logging, data["log_level_console"]))

formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s: %(message)s (l.%(lineno)s - %(funcName)s())")
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

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

class TestSum(unittest.TestCase):
    def test_ok_min(self):
        try:
            self.assertAlmostEqual(df_ok_complete_sum_min, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
            logger.info("OK")
        except Exception as e:
            logger.error(e)
        
    def test_ok_max(self):
        try:
            self.assertAlmostEqual(df_ok_complete_sum_max, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
            logger.info("OK")
        except Exception as e:
            logger.error(e)
        
    def test_error_min(self):
        try:
            self.assertNotAlmostEqual(df_error_complete_sum_min, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
            logger.info("OK")
        except Exception as e:
            logger.error(e)
        
    def test_error_max(self):
        try:
            self.assertNotAlmostEqual(df_error_complete_sum_max, 1, 4, "Should be equal to 1 with a tolerance of 4 decimals")
            logger.info("OK")
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    logger.info("Starting...")
    unittest.main(exit=False)
    logger.info("Finished!")
