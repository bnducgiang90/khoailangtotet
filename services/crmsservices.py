import sys
# đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
sys.path.append('.')
# define top level module logger
import logging
logger = logging.getLogger(__name__)

from databases.crmsdb import *
from datamodels.crms.qlt_params import *


class servicecrms:
    def __init__(self):
        self.db = crmsdatabase()

##get thông tin doanh nghiệp
    def get_hsdns(self) -> []:
        lstHSDNs = self.db.get_hsdns()
        return lstHSDNs

    def get_hsdn_params(self) -> {}:
        hsdn_params = self.db.get_hsdn_params()
        return hsdn_params
##END get thông tin doanh nghiệp

##get thông tin hồ sơ vi phạm
    def get_hsvps(self) -> []:
        lstHSVPs = self.db.get_hsvps()
        return lstHSVPs

    def get_hsvp_params(self) -> {}:
        hsvp_params = self.db.get_hsvp_params()
        return hsvp_params

##END get thông tin doanh nghiệp

#test:
    def getdata(self) -> []:
        lstobj = self.db.getdata()
        return lstobj
#END test

