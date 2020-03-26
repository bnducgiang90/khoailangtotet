import logging
import logging.config
from configs.configsettings import logconfig
from datamodels.crms.qlt_params import crms_tokhai_nothue
from utils.filehelpers import filehelper
from services.crmsservices import servicecrms


# from utils.objecthelpers import  helper

def mappingdata(obj: object):
    print(obj.__dict__.keys())


def main():
    ## khởi tạo logging
    logging_config = filehelper.readyalmfile(logconfig.logconfigfile)
    logging.config.dictConfig(logging_config)
    ## end khởi tạo logging

    srvcrms = servicecrms()
    lstobj: [] = srvcrms.getdata()
    for obj in lstobj:
        print("ID : {}, MA_DV : {}".format(obj.ID, obj.MA_DV))

    print("succeed")


if __name__ == '__main__':
    main()
