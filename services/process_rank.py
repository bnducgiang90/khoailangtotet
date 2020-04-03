import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)

from services.crmsservices import *
from services.process_hsdn_rank import *
from services.process_hsvp_rank import *
from utils.constants import *
from datamodels.crms.qlt_hsdn_xhdn import  *
from datamodels.crms.qlt_hsvp_xhdn import *
from datamodels.crms.qlt_xhdn import QLT_XEPHANGDN_20

class process_rank:
    def __init__(self):
        self._srvcrms = crmsservice()

    ## tính toán xhdn
    def qlt_xhdn(self):

        # 1. tính toán XHDN HSDN
        ### lấy danh sách params HSDN:
        _hsdn_params: {} = self._srvcrms.get_hsdn_params()

        ### lấy danh sách dn cần đánh giá:
        _lstHSDNs = self._srvcrms.get_hsdns(None, None, None)

        ### khởi tạo process RANK HSDN:
        _procs_hsdn_rank = process_rank_hsdn(_lstHSDNs, _hsdn_params)

        ### Đánh giá RANK HSDN:
        logger.info("------Bắt đầu đánh giá RANK HSDN ---------")
        _qlt_hsdn_xhdns: List[qlt_hsdn_xhdn] = _procs_hsdn_rank.process_qlt_hsdn_xhdn()
        logger.info("------Kết thúc đánh giá RANK HSDN ---------")

        # 2. tính toán XHDN HSVP
        ### lấy danh sách params HSVP:
        _hsvp_params: {} = self._srvcrms.get_hsvp_params()

        ### lấy danh sách HSVP cần đánh giá:
        _lstHSVPs = self._srvcrms.get_hsvps()

        ### khởi tại process RANK HSVP:
        _procs_hsvp_rank = process_rank_hsvp(_lstHSVPs, _hsvp_params)

        ### Đánh giá RANK HSVP:
        logger.info("------Bắt đầu đánh giá RANK HSVP ---------")
        _qlt_hsvp_xhdns: List[qlt_hsvp_xhdn] = _procs_hsvp_rank.process_qlt_hsvp_xhdn()
        logger.info("------Kết thúc đánh giá RANK HSVP ---------")

        # 3. Cộng điểm HSDN + HSVP để thực hiện xếp RANK:
        logger.info("------Bắt đầu xếp cộng điểm HSDN + HSVP  ---------")
        _qlt_xephangs:List[QLT_XEPHANGDN_20] = []

        for _hsdn in _qlt_hsdn_xhdns:
            for _hsvp in _qlt_hsvp_xhdns:
                pass


        logger.info("------Kết thúc cộng điểm HSDN + HSVP  ---------")

        logger.info("------Bắt đầu xếp RANK  ---------")
        _params_plxephang: List[QLT_PARAMS_PLXEPHANG]  = self._srvcrms.get_params_plxephangs()

        logger.info("------Kết thúc xếp RANK  ---------")

        logger.info("------Kết thúc đánh giá RANK ---------")

# hiển thị biểu  đồ
# x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
# plt.plot(x, np.sin(x))       # Plot the sine of each x point
# plt.show()
