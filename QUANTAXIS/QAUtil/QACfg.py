import os
import sys

from configparser import ConfigParser


def QA_util_cfg_initial(CONFIG_FILE):

    pass


def QA_util_get_cfg(__file_path, __file_name):
    __setting_file = ConfigParser()
    try:
        return __setting_file.read(__file_path + __file_name)
    except:
        return 'wrong'
