import logging
import logging.config

from configs.configsettings import logconfig
from utils.filehelpers import filehelper
from services.crmsservices import *
from services.process_hsdn_rank import *
from services.process_hsvp_rank import *
from utils.constants import *
from datamodels.crms.qlt_hsdn_xhdn import  *

# from utils.objecthelpers import  helper

def mappingdata(obj: object):
    print(obj.__dict__.keys())


def main():
    ## khởi tạo logging
    logging_config = filehelper.readyalmfile(logconfig.logconfigfile)
    logging.config.dictConfig(logging_config)
    ## end khởi tạo logging


    srvcrms = crmsservice()
    hsdn_params: {} = srvcrms.get_hsdn_params()
    # print("HSDN:")
    # for key, value in hsdn_params.items():
    #     print("key : {}, values : {}".format(key, len(value)))

    hsvp_params: {} = srvcrms.get_hsvp_params()
    # print("HSVP:")
    # for key, value in hsvp_params.items():
    #     print("key : {}, values : {}".format(key, len(value)))

    lstHSDNs = srvcrms.get_hsdns(None, None, None)
    procs_hsdn_rank = process_rank_hsdn(lstHSDNs, hsdn_params)

    # tieuchi_hsdns: {} = procs_hsdn_rank.tinh_giatri_diem_tieuchi_hsdn()
    # print("process_rank_hsdn:")
    # my_list2 = []
    # my_list3 = []
    # for key, values in tieuchi_hsdns.items():
    #     print("key : {}, values : {}".format(key, len(values)))
    #
    #     for i, g in groupby(values, key=lambda x: (x.ID_NHOM, x.NK_XK)):
    #         my_list2.append([i, sum(v.DIEM for v in g)])
    #
    # print(len(my_list2))
    # print(my_list2)
    # my_list3 = list(Counter(key for key, num in my_list2
    #              for idx in range(num)).items())
    #
    # print(len(my_list3))
    # print(my_list3)

    print("get_qlt_hsdn_xhdns:")
    qlt_hsdn_xhdns: List[qlt_hsdn_xhdn] = procs_hsdn_rank.get_qlt_hsdn_xhdns
    for item in qlt_hsdn_xhdns :
        print("MA_DN : {}".format(item.MA_DN))
        print("----- Bang diem tieu chi -----")
        for kl1 in item.qlt_tieuchi_hsdns:
            print("MA_DN: {}; ID_TIEUCHI: {}; GIA_TRI: {}, ID_NHOM: {}, NK_XK: {}, PHUONGTHUCAPDUNG: {}, DIEM: {}, DIEMPHAT : {}, DIEM_MAX : {}".format(
                kl1.MA_DN, kl1.ID_TIEUCHI, kl1.GIA_TRI, kl1.ID_NHOM, kl1.NK_XK, kl1.PHUONGTHUCAPDUNG,
                kl1.DIEM, kl1.DIEMPHAT, kl1.DIEM_MAX)
               )

        print("----- Bang diem nhom tieu chi -----")
        for kl2 in item.qlt_tieuchi_nhoms:
            print(
                "NK_XK: {}; ID_NHOM: {}; DIEMNHOM: {}".format(
                    kl2.NK_XK, kl2.ID_NHOM, kl2.DIEMNHOM)
                )

        print("----- Bang ty trong phan loai nhom -----")
        for kl2 in item.qlt_tytrong_phanloai_nhoms:
            print(
                "NK_XK: {}; ID_NHOM: {}; TYTRONG: {}".format(
                    kl2.NK_XK, kl2.ID_NHOM, kl2.TYTRONG)
            )

        print("----- Bang diem phan loai cuoi cung cua nhom -----")
        values = item.qlt_diem_phanloaicuoicung_nhoms
        for kl2 in values:
            print(
                "NK_XK: {}; ID_NHOM: {}; DIEM_PLCC: {}".format(
                    kl2.NK_XK, kl2.ID_NHOM, kl2.DIEM_PLCC)
            )
        print(" ----- Bang diem phan loai cuoi cung DN -----")
        print("NK_XK: 1    Diem PLCC (DN): {}	 MaDN: {}".format(item.DIEM_PLCC_NK, item.MA_DN))
        print("NK_XK: 2    Diem PLCC (DN): {}	 MaDN: {}".format(item.DIEM_PLCC_XK, item.MA_DN))
        print("NK_XK: 1    Diem Phat (DN): {}	 MaDN: {}".format(item.DIEM_PHAT_NK, item.MA_DN))
        print("NK_XK: 2    Diem Phat (DN): {}	 MaDN: {}".format(item.DIEM_PHAT_XK, item.MA_DN))

    print("succeed")

if __name__ == '__main__':
    print((1, 1) == (1, 1))
    print((1, 1) == (1, 2))
    main()
