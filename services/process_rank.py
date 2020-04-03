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
from datamodels.crms.qlt_xhdn import QLT_XEPHANGDN_20, QLT_LYDOXEPHANG_HSDN_DIEMTC


class process_rank:
    def __init__(self):
        self._srvcrms = crmsservice()

    ## tính toán xhdn
    def qlt_xhdn(self):
        _ID_TH = self._srvcrms.get_XHDN_TH_GetID()
        if _ID_TH is None or _ID_TH ==0:
            logger.warning("Chưa có thông tin tổng hợp doanh nghiệp!")
            logger.warning("Kết thúc đánh giá xếp hạng!")
            return

        # 0. Lấy Phiên bản và id_lydo:
        _ID_PHIENBAN = self._srvcrms.get_next_id_phienban()
        _ID_LYDOXEPHANG = self._srvcrms.get_next_id_lydoxephang()
        if _ID_PHIENBAN is None or _ID_PHIENBAN ==0 or _ID_LYDOXEPHANG is None or _ID_LYDOXEPHANG ==0:
            logger.warning("Lỗi khởi tạo ID_PHIENBAN  và ID_LYDOXEPHANG  !")
            logger.warning("Kết thúc đánh giá xếp hạng!")

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
        logger.info("------Bắt đầu xếp cộng điểm HSDN + HSVP  + xếp RANK---------")

        _qlt_xephangs:List[QLT_XEPHANGDN_20] = []
        _lst_lydo_diem_tc: List[QLT_LYDOXEPHANG_HSDN_DIEMTC] = []
        
        _params_qltxephang =  self._srvcrms.get_params_plxephangs()

        for _hsdn in _qlt_hsdn_xhdns:
            _qlt_xephangdn = QLT_XEPHANGDN_20()
            _qlt_xephangdn.MADN = _hsdn.MA_DN
            _qlt_xephangdn.ID_PHIENBAN = _ID_PHIENBAN
            _qlt_xephangdn.ID_LYDOXEPHANG = _ID_LYDOXEPHANG
            _qlt_xephangdn.DIEMPHANLOAINK = _hsdn.DIEM_PLCC.DIEM_PLCC_NK + _hsdn.DIEM_PLCC.DIEM_PHAT_NK
            _qlt_xephangdn.DIEMPHANLOAIXK = _hsdn.DIEM_PLCC.DIEM_PLCC_XK + _hsdn.DIEM_PLCC.DIEM_PHAT_XK
            _hsvp = [item for item in _qlt_hsvp_xhdns if item.MA_DN == _hsdn.MA_DN]
            if _hsvp:
                _qlt_xephangdn.DIEMPHANLOAINK += _hsvp[0].DIEM_PLCC.DIEM_PLCC_NK
                _qlt_xephangdn.DIEMPHANLOAIXK += _hsvp[0].DIEM_PLCC.DIEM_PLCC_XK

            ## tính hạng:
            #NK
            for p in [item for item in _params_qltxephang if item.NK_XK == const_crms.LOAI_HINH_NK]:
                if _qlt_xephangdn.DIEMPHANLOAINK <= p.GIATRI:
                    _qlt_xephangdn.HANGNK = p.HANG
                    break
            #XK
            for p in [item for item in _params_qltxephang if item.NK_XK == const_crms.LOAI_HINH_XK]:
                if _qlt_xephangdn.DIEMPHANLOAIXK <= p.GIATRI:
                    _qlt_xephangdn.HANGXK = p.HANG
                    break

            _qlt_xephangs.append(_qlt_xephangdn)

            ##tính điểm tiêu chí:
            for _tc in _hsdn.qlt_tieuchi_hsdns:
                _lydo_diem_tc = QLT_LYDOXEPHANG_HSDN_DIEMTC()
                _lydo_diem_tc.NK_XK = _tc.NK_XK
                _lydo_diem_tc.ID_PHIENBAN = _ID_PHIENBAN
                _lydo_diem_tc.MADN = _hsdn.MA_DN
                _lydo_diem_tc.ID_TIEUCHI = _tc.ID_TIEUCHI
                _lydo_diem_tc.DIEM = _tc.DIEM
                _lydo_diem_tc.DIEMPHAT = _tc.DIEMPHAT
                _lst_lydo_diem_tc.append(_lydo_diem_tc)



        logger.info("------Kết thúc xếp cộng điểm HSDN + HSVP  + xếp RANK---------")

        logger.info("------Bắt đầu ghi kết quả xếp RANK---------")
        self._srvcrms.insert_qlt_tmp_xephangdn(_qlt_xephangs)
        logger.info("------Kết thúc ghi kết quả xếp RANK---------")


        #4. Ghi lý do
        logger.info("------Bắt đầu ghi lý do xếp RANK HSDN & HSVP ---------")
        self._srvcrms.insert_qlt_xephangdn(_ID_PHIENBAN, _ID_LYDOXEPHANG)
        logger.info("------Kết thúc ghi lý do xếp RANK HSDN & HSVP ---------")


        logger.info("------Bắt đầu ghi lý do Điểm tiêu chí xếp RANK HSDN---------")
        self._srvcrms.insert_hsdn_lydoxephang_diemtc(_lst_lydo_diem_tc)
        logger.info("------Bắt đầu ghi lý do Điểm tiêu chí xếp RANK HSDN---------")


        logger.info("------Kết thúc đánh giá RANK ---------")

# hiển thị biểu  đồ
# x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
# plt.plot(x, np.sin(x))       # Plot the sine of each x point
# plt.show()
