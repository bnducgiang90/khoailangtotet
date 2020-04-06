
# thông tin bảng tổng hợp QLT_THONGTINDOANHNGHIEP
class QLT_THONGTINDOANHNGHIEP:
    def __init__(self):
        self.ID = 0
        self.MA_DN = ""
        self.SO_NGAY_THANH_LAP_DN = 0
        self.SO_NGAY_THANH_LAP_DN_UNK = 0
        self.DIA_CHI_TRU_SO_DN = 0
        self.QUYEN_SO_HUU_TRU_SO_DN = 0
        self.SO_LUONG_NHAN_VIEN_DN_GC_SXXK = 0
        self.SO_LUONG_NHAN_VIEN_DN_KD = 0
        self.DN_GC_SXXK = 0
        self.QUOC_GIA_HOAT_DONG_DN = ""
        self.LOAI_HINH_DN = ""
        self.CSSX = 0
        self.VON_DANG_KY_KINH_DOANH = 0.0
        self.VON_CHU_SO_HUU = 0.0
        self.THAM_GIA_THI_TRUONG_CK = 0
        self.THAM_GIA_THI_TRUONG_CK_UNK = 0
        self.THOI_GIAN_HOAT_DONG_XNK = 0
        self.SO_TO_KHAI_TRONG_365N = 0
        self.TY_LE_KIEM_TRA_HO_SO_365N = 0.0
        self.TY_LE_KIEM_TRA_THUC_TE_365N = 0.0
        self.KIEM_TRA_STQ = 0
        self.THANH_TRA_KIEM_TRA = 0
        self.TONG_SO_THUE_XNK = 0.0
        self.DOANH_THU = 0.0
        self.LOI_NHUAN = 0.0
        self.KIM_NGACH = 0.0
        self.VP_DN_CN_BUON_LAU_365N = 0
        self.VP_DN_CN_BUON_LAU_730N = 0
        self.VP_DN_HC_TREN_50M_TRONG_730N = 0
        self.VP_DN_HC_TREN_50M_TRONG_365N = 0
        self.VP_DN_HC_DUOI_50M_TRONG_730N = 0
        self.VP_DN_HC_DUOI_50M_TRONG_365N = 0
        self.VP_DN_THUE_TREN_50M_TRONG_730N = 0
        self.VP_DN_THUE_TREN_50M_TRONG_365N = 0
        self.VP_DN_THUE_DUOI_50M_TRONG_730N = 0
        self.VP_DN_THUE_DUOI_50M_TRONG_365N = 0
        self.VP_DN_KTT = 0
        self.VP_DN_KTT_LON_HON_TRONG_730N = 0
        self.VP_DN_KTT_NHO_HON_TRONG_730N = 0
        self.VP_DN_KCH_YEU_CAU_HAI_QUAN = 0
        self.TSL_NO_THUE_QUA_HAN_TRONG_365N = 0
        self.TSL_BI_CUONG_CHE_THUE = 0
        self.TONG_NO_LE_PHI_HAI_QUAN = 0
        self.SOTOKHAIDUOCTHONGQUAN = 0

#thông tin bảng tổng hợp QLT_THONGTINVIPHAM
class QLT_THONGTINVIPHAM:
    def __init__(self):
        self.ID = 0
        self.XNK = ""
        self.COTK = 0
        self.MA_DN = ""
        self.NGHIEMTRONG = 0
        self.LOAIVIPHAM = ""
        self.TRACHNHIEM = 0
        self.CHENHLECHTHUE_DUTY = 0.0
        self.CHENHLECHTHUE_VAT = 0.0
        self.CHENHLECHTHUE_TTDB = 0.0
        self.CHENHLECHTHUE_BVMT = 0.0
        self.CHENHLECHTHUE_TUVE = 0.0
        self.CHENHLECHTHUE_CBPG = 0.0
        self.CHENHLECHTHUE_KHAC = 0.0
        self.NK_XK = 0

    def getvalue(self, v):
        if v is None : v = 0.0
        return v

    @property
    def TONG_CHENHLECHTHUE(self):
        return sum([self.getvalue(self.CHENHLECHTHUE_DUTY), self.getvalue(self.CHENHLECHTHUE_VAT), self.getvalue(self.CHENHLECHTHUE_TTDB)
                    , self.getvalue(self.CHENHLECHTHUE_BVMT), self.getvalue(self.CHENHLECHTHUE_TUVE), self.getvalue(self.CHENHLECHTHUE_CBPG)
                    , self.getvalue(self.CHENHLECHTHUE_KHAC)
                   ])