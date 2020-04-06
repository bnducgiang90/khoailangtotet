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
        self._qlt_hsdn_xhdns: List[qlt_hsdn_xhdn] = []
        self._qlt_hsvp_xhdns: List[qlt_hsvp_xhdn] = []
        self._qlt_xephangs: List[QLT_XEPHANGDN_20] = []
        self._lst_lydo_diem_tc: List[QLT_LYDOXEPHANG_HSDN_DIEMTC] = []
        self._hsdn_rowIdmin = 0
        self._hsdn_rowIdmax = 0
        self._params_qltxephang = self._srvcrms.get_params_plxephangs()
        self._dict_qlt_hsvp_xhdns = {}

    ## tính toán xhdn
    def qlt_xhdn(self):
        try:
            _ID_TH = self._srvcrms.get_XHDN_TH_GetID()
            if _ID_TH is None or _ID_TH == 0:
                logger.warning("Chưa có thông tin tổng hợp doanh nghiệp!")
                logger.warning("Kết thúc đánh giá xếp hạng!")
                return

            # 0. Lấy Phiên bản và id_lydo:
            _ID_PHIENBAN = self._srvcrms.get_id_phienban(0)
            _ID_LYDOXEPHANG = self._srvcrms.get_next_id_lydoxephang()
            if _ID_PHIENBAN is None or _ID_PHIENBAN == 0 or _ID_LYDOXEPHANG is None or _ID_LYDOXEPHANG == 0:
                logger.warning("Lỗi khởi tạo ID_PHIENBAN  và ID_LYDOXEPHANG  !")
                logger.warning("Kết thúc đánh giá xếp hạng!")
                return

            # 1. tính toán XHDN HSVP
            ### lấy danh sách params HSVP:
            _hsvp_params: {} = self._srvcrms.get_hsvp_params()

            ### lấy danh sách HSVP cần đánh giá:
            _lstHSVPs = self._srvcrms.get_hsvps()
            if len(_lstHSVPs) >0:
                ### khởi tại process RANK HSVP:
                _procs_hsvp_rank = process_rank_hsvp(_lstHSVPs, _hsvp_params)

                ### Đánh giá RANK HSVP:
                logger.info("------Bắt đầu đánh giá RANK HSVP ---------")
                self._qlt_hsvp_xhdns = _procs_hsvp_rank.process_qlt_hsvp_xhdn()
                logger.info("------Kết thúc đánh giá RANK HSVP ---------")
                self._dict_qlt_hsvp_xhdns = {item.MA_DN: (item.DIEM_PLCC.DIEM_PLCC_NK, item.DIEM_PLCC.DIEM_PLCC_XK) for item in self._qlt_hsvp_xhdns}

            # 2. tính toán XHDN HSDN
            ### lấy danh sách params HSDN:
            _hsdn_params: {} = self._srvcrms.get_hsdn_params()
            self._hsdn_rowIdmin = _hsdn_params[const_hsdn_params.QLT_MIN_MAX_ID][0]
            self._hsdn_rowIdmax = _hsdn_params[const_hsdn_params.QLT_MIN_MAX_ID][1]
            _fromRowid = self._hsdn_rowIdmin

            logger.info("Từ rowID: {} - Đến rowID: {} - Số lượng row mỗi process : {}".format(_fromRowid, self._hsdn_rowIdmax, const_crms.NUMBER_RECORD_PROCESS))
            ### lấy danh sách dn cần đánh giá:
            while _fromRowid < self._hsdn_rowIdmax:
                logger.info("Lấy thông tin HSDN và tính điểm từ rowID: {} - đến rowID : {}".format(_fromRowid, _fromRowid + const_crms.NUMBER_RECORD_PROCESS))
                _lstHSDNs = self._srvcrms.get_hsdns(_fromRowid, _fromRowid + const_crms.NUMBER_RECORD_PROCESS, 0)

                ### khởi tạo process RANK HSDN:
                _procs_hsdn_rank = process_rank_hsdn(_lstHSDNs, _hsdn_params)

                ### Đánh giá RANK HSDN:
                logger.info("------Bắt đầu đánh giá RANK HSDN ---------")
                self._qlt_hsdn_xhdns = _procs_hsdn_rank.process_qlt_hsdn_xhdn()
                logger.info("------Kết thúc đánh giá RANK HSDN ---------")


                # 3. Cộng điểm HSDN + HSVP để thực hiện xếp RANK:
                logger.info("------Bắt đầu xếp cộng điểm HSDN + HSVP  + xếp RANK---------")
                # logger.info("------1. Bắt đầu xếp cộng điểm HSDN + HSVP---------")
                #
                # _qlt_hsdn_xhdns_exist_hsvp = [item for item in  self._qlt_hsdn_xhdns if item.MA_DN in list(_dict_qlt_hsvp_xhdns.keys())]
                #
                # for item in _qlt_hsdn_xhdns_exist_hsvp:
                #     _hsvp = _dict_qlt_hsvp_xhdns[item.MA_DN]
                #     item.DIEM_PLCC.DIEM_PLCC_NK = item.DIEM_PLCC.DIEM_PLCC_NK +  _hsvp[0]
                #     item.DIEM_PLCC.DIEM_PLCC_XK = item.DIEM_PLCC.DIEM_PLCC_NK +  _hsvp[1]
                #
                # self._qlt_hsvp_xhdns = [item for item in  self._qlt_hsdn_xhdns if item.MA_DN not in list(_dict_qlt_hsvp_xhdns.keys())]
                # self._qlt_hsdn_xhdns.extend(_qlt_hsdn_xhdns_exist_hsvp)
                # logger.info("------1. Kết thúc xếp cộng điểm HSDN + HSVP---------")

                for _hsdn in self._qlt_hsdn_xhdns:
                    _qlt_xephangdn = QLT_XEPHANGDN_20()
                    _qlt_xephangdn.MADN = _hsdn.MA_DN
                    _qlt_xephangdn.ID_PHIENBAN = _ID_PHIENBAN
                    _qlt_xephangdn.ID_LYDOXEPHANG = _ID_LYDOXEPHANG
                    _qlt_xephangdn.DIEMPHANLOAINK = _hsdn.DIEM_PLCC.DIEM_PLCC_NK + _hsdn.DIEM_PLCC.DIEM_PHAT_NK
                    _qlt_xephangdn.DIEMPHANLOAIXK = _hsdn.DIEM_PLCC.DIEM_PLCC_XK + _hsdn.DIEM_PLCC.DIEM_PHAT_XK

                    # _hsvp = [item for item in self._qlt_hsvp_xhdns if item.MA_DN == _hsdn.MA_DN] #
                    _hsvp = self._dict_qlt_hsvp_xhdns.get(_hsdn.MA_DN)  #[item for item in _qlt_hsvp_xhdns if item.MA_DN == _hsdn.MA_DN]
                    if _hsvp:
                        _qlt_xephangdn.DIEMPHANLOAINK += _hsvp[0] #_hsvp[0].DIEM_PLCC.DIEM_PLCC_NK
                        _qlt_xephangdn.DIEMPHANLOAIXK += _hsvp[1] #_hsvp[0].DIEM_PLCC.DIEM_PLCC_XK

                    ## tính hạng:
                    # NK
                    for p in [item for item in self._params_qltxephang if item.NK_XK == const_crms.LOAI_HINH_NK]:
                        if _qlt_xephangdn.DIEMPHANLOAINK <= p.GIATRI:
                            _qlt_xephangdn.HANGNK = p.HANG
                            break
                    # XK
                    for p in [item for item in self._params_qltxephang if item.NK_XK == const_crms.LOAI_HINH_XK]:
                        if _qlt_xephangdn.DIEMPHANLOAIXK <= p.GIATRI:
                            _qlt_xephangdn.HANGXK = p.HANG
                            break

                    self._qlt_xephangs.append(_qlt_xephangdn)

                    ##tính điểm tiêu chí:
                    for _tc in _hsdn.qlt_tieuchi_hsdns:
                        _lydo_diem_tc = QLT_LYDOXEPHANG_HSDN_DIEMTC()
                        _lydo_diem_tc.NK_XK = _tc.NK_XK
                        _lydo_diem_tc.ID_PHIENBAN = _ID_PHIENBAN
                        _lydo_diem_tc.MADN = _hsdn.MA_DN
                        _lydo_diem_tc.ID_TIEUCHI = _tc.ID_TIEUCHI
                        _lydo_diem_tc.DIEM = _tc.DIEM
                        _lydo_diem_tc.DIEMPHAT = _tc.DIEMPHAT
                        self._lst_lydo_diem_tc.append(_lydo_diem_tc)

                logger.info("------Kết thúc xếp cộng điểm HSDN + HSVP  + xếp RANK---------")

                logger.info("------Bắt đầu ghi kết quả xếp RANK vào bảng Trung gian---------")
                self._srvcrms.insert_qlt_tmp_xephangdn(self._qlt_xephangs)
                self._qlt_xephangs = []
                logger.info("------Kết thúc ghi kết quả xếp RANK vào bảng Trung gian---------")

                # 4. Ghi lý do điểm hsdn:
                logger.info("------Bắt đầu ghi lý do Điểm tiêu chí xếp RANK HSDN---------")
                self._srvcrms.insert_hsdn_lydoxephang_diemtc(self._lst_lydo_diem_tc)
                logger.info("------Kết thúc ghi lý do Điểm tiêu chí xếp RANK HSDN số lượng bản ghi: {}---------".format(len(self._lst_lydo_diem_tc)))

                self._lst_lydo_diem_tc = []
                _fromRowid += (const_crms.NUMBER_RECORD_PROCESS + 1);

            logger.info("------Bắt đầu ghi kết quả tính điểm và xếp hạng doanh nghiệp ---------")
            self._srvcrms.insert_qlt_xephangdn(_ID_PHIENBAN, _ID_LYDOXEPHANG)
            logger.info("------Kết thúc ghi kết quả tính điểm và xếp hạng doanh nghiệp ---------")

            self._srvcrms.XHDN_TH_Update(_ID_TH)

        except Exception as ex:
            logger.exception("Lỗi :")
        finally:
            logger.info("------Kết thúc đánh giá RANK ---------")


# hiển thị biểu  đồ
# x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
# plt.plot(x, np.sin(x))       # Plot the sine of each x point
# plt.show()
