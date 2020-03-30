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
    hsdn_params: {} = srvcrms.get_hsdn_params()
    print("HSDN:")
    for key, value in hsdn_params.items():
        print("key : {}, values : {}".format(key, len(value)))

    hsvp_params: {} = srvcrms.get_hsvp_params()
    print("HSVP:")
    for key, value in hsvp_params.items():
        print("key : {}, values : {}".format(key, len(value)))

    print("succeed")


if __name__ == '__main__':
    main()
