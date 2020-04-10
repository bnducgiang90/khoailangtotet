import logging
import logging.config

from configs.configsettings import logconfig
from utils.filehelpers import filehelper
from services.process_rank import process_rank
import datetime
# from utils.objecthelpers import  helper

def mappingdata(obj: object):
    print(obj.__dict__.keys())


def main():
    ## khởi tạo logging
    logging_config = filehelper.readyalmfile(logconfig.logconfigfile)
    logging.config.dictConfig(logging_config)
    ## end khởi tạo logging
    print("{} start".format(datetime.datetime.now()))
    _process_rank = process_rank()
    _process_rank.qlt_xhdn()

    print("{} done!".format(datetime.datetime.now()))

if __name__ == '__main__':
    main()
