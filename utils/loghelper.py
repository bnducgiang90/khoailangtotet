import sys
# đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
sys.path.append('.')
import  logging
import logging.config
from configs.configsettings import logconfig
from utils.filehelpers import filehelper

class Logger:
    
    def __init__(self, name):
        logging_config =filehelper.readyalmfile(logconfig.logconfigfile)
        print(logging_config)
        logging.config.dictConfig(logging_config)
        # create logger
        logger = logging.getLogger('log_namespace.%s' % name)
        self._logger = logger

    def get(self):
        return self._logger
