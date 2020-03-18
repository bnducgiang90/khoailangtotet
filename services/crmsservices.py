import sys
# đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
sys.path.append('.')
# define top level module logger
import logging
logger = logging.getLogger(__name__)

from databases.crmsdb import *
from datamodels.crms.xephangdoanhnghiep import *


class servicecrms:
    
    def getdata(self):
        db = crmsdatabase()
        lstobj = db.getdata()
        return lstobj
