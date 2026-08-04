import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

target = """const MOCK_MATCHES = [
            {
                "id_tran_dau": "match_1717123456",
                "thong_tin": { "ngay_thi_dau": "2026-07-30", "loai_hinh": "Đánh bia", "doi_thu_1": "Hungpv", "doi_thu_2": "Nguyễn Văn A", "chap_bong": "Tôi chấp 2", "ket_qua": "3-2", "mo_ta": "Đối thủ gò nặng.", "link_youtube": "", "link_facebook": "", "link_khac": "" },
                "chi_tiet_game": [
                    {
                        "game_so": 1, "ty_so_bat_dau": "0-2", "nguoi_giao_bong_truoc": "Hungpv", "ty_so_chung_cuoc": "11-8", "trang_thai": "hoan_thanh",
                        "danh_sach_diem": [
                            { "thu_tu_diem": 1, "ty_so_hien_tai": "1-2", "loai_diem": "thang", "nhom": "nhom_giao_bong", "ky_thuat": "xuong_ngan", "nguoi_giao_bong": "Hungpv" },
                            { "thu_tu_diem": 2, "ty_so_hien_tai": "1-3", "loai_diem": "thua", "nhom": "nhom_ky_thuat", "ky_thuat": "phong_thu_trai", "nguoi_giao_bong": "Hungpv" }
                        ]
                    }
                ]
            }
        ];"""

replacement = """const MOCK_MATCHES = [
            {
                "id_tran_dau": "match_1717123456",
                "thong_tin": { "ngay_thi_dau": "2026-07-30", "loai_hinh": "Đánh bia", "doi_thu_1": "Hungpv", "doi_thu_2": "Nguyễn Văn A", "chap_bong": "Tôi chấp 2", "ket_qua": "3-2", "mo_ta": "Đối thủ gò nặng.", "link_youtube": "", "link_facebook": "", "link_khac": "" },
                "chi_tiet_game": [
                    {
                        "game_so": 1, "ty_so_bat_dau": "0-2", "nguoi_giao_bong_truoc": "Hungpv", "ty_so_chung_cuoc": "11-8", "trang_thai": "hoan_thanh",
                        "danh_sach_diem": [
                            { 
                                "thu_tu_diem": 1, "ty_so_hien_tai": "1-2", "loai_diem": "thang", "nguoi_giao_bong": "Hungpv",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "winner",
                                    "nguoi_ket_thuc": "Hungpv",
                                    "ky_thuat_ket_thuc": "giao_bong_thuan",
                                    "nguoi_kien_tao": "",
                                    "ky_thuat_kien_tao": "",
                                    "dac_tinh": {
                                        "diem_roi_ngang": "trai",
                                        "do_dai": "ngan",
                                        "do_xoay": "xuong",
                                        "vi_tri_hong": ""
                                    }
                                }
                            },
                            { 
                                "thu_tu_diem": 2, "ty_so_hien_tai": "1-3", "loai_diem": "thua", "nguoi_giao_bong": "Hungpv",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "unforced_error",
                                    "nguoi_ket_thuc": "Hungpv",
                                    "ky_thuat_ket_thuc": "phong_thu_trai",
                                    "nguoi_kien_tao": "",
                                    "ky_thuat_kien_tao": "",
                                    "dac_tinh": {
                                        "diem_roi_ngang": "",
                                        "do_dai": "",
                                        "do_xoay": "",
                                        "vi_tri_hong": "ruc_luoi"
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        ];"""

new_content = content.replace(target, replacement)
if new_content == content:
    print("Could not find target!")
else:
    with open("/app/applet/index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully replaced!")
