import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "const MOCK_MATCHES = ["
end_marker = "        ];"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    old_block = content[start_idx:end_idx + len(end_marker)]
    new_block = """const MOCK_MATCHES = [
            {
                "id_tran_dau": "match_1717123456",
                "thong_tin": { "ngay_thi_dau": "2026-07-30", "loai_hinh": "Đánh bia", "doi_thu_1": "Hungpv", "doi_thu_2": "Nguyễn Văn A", "chap_bong": "Không", "ket_qua": "Đang đấu", "mo_ta": "Dữ liệu mẫu 9 điểm.", "link_youtube": "", "link_facebook": "", "link_khac": "" },
                "chi_tiet_game": [
                    {
                        "game_so": 1, "ty_so_bat_dau": "0-0", "nguoi_giao_bong_truoc": "Hungpv", "ty_so_chung_cuoc": "5-4", "trang_thai": "dang_dau",
                        "danh_sach_diem": [
                            { 
                                "thu_tu_diem": 1, "ty_so_hien_tai": "1-0", "loai_diem": "thang", "nguoi_giao_bong": "Hungpv",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "winner", "nguoi_ket_thuc": "Hungpv", "ky_thuat_ket_thuc": "giao_bong_thuan", "nguoi_kien_tao": "", "ky_thuat_kien_tao": "",
                                    "dac_tinh": { "diem_roi_ngang": "trai", "do_dai": "dai", "do_xoay": "ngang_len", "vi_tri_hong": "" }
                                }
                            },
                            { 
                                "thu_tu_diem": 2, "ty_so_hien_tai": "1-1", "loai_diem": "thua", "nguoi_giao_bong": "Hungpv",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "winner", "nguoi_ket_thuc": "Nguyễn Văn A", "ky_thuat_ket_thuc": "giat_phai", "nguoi_kien_tao": "", "ky_thuat_kien_tao": "",
                                    "dac_tinh": { "diem_roi_ngang": "phai", "do_dai": "ngan", "do_xoay": "ngang_len", "vi_tri_hong": "" }
                                }
                            },
                            { 
                                "thu_tu_diem": 3, "ty_so_hien_tai": "2-1", "loai_diem": "thang", "nguoi_giao_bong": "Nguyễn Văn A",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "forced_error", "nguoi_ket_thuc": "Nguyễn Văn A", "ky_thuat_ket_thuc": "chan_phai", "nguoi_kien_tao": "Hungpv", "ky_thuat_kien_tao": "giat_phai",
                                    "dac_tinh": { "diem_roi_ngang": "trai", "do_dai": "dai", "do_xoay": "ngang_len", "vi_tri_hong": "ruc_luoi" }
                                }
                            },
                            { 
                                "thu_tu_diem": 4, "ty_so_hien_tai": "2-2", "loai_diem": "thua", "nguoi_giao_bong": "Nguyễn Văn A",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "forced_error", "nguoi_ket_thuc": "Hungpv", "ky_thuat_ket_thuc": "giat_phai", "nguoi_kien_tao": "Nguyễn Văn A", "ky_thuat_kien_tao": "cat_nang",
                                    "dac_tinh": { "diem_roi_ngang": "phai", "do_dai": "dai", "do_xoay": "xuong", "vi_tri_hong": "ra_ngoai" }
                                }
                            },
                            { 
                                "thu_tu_diem": 5, "ty_so_hien_tai": "3-2", "loai_diem": "thang", "nguoi_giao_bong": "Hungpv",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "unforced_error", "nguoi_ket_thuc": "Nguyễn Văn A", "ky_thuat_ket_thuc": "giao_bong_trai", "nguoi_kien_tao": "", "ky_thuat_kien_tao": "",
                                    "dac_tinh": { "diem_roi_ngang": "", "do_dai": "", "do_xoay": "", "vi_tri_hong": "ruc_luoi" }
                                }
                            },
                            { 
                                "thu_tu_diem": 6, "ty_so_hien_tai": "3-3", "loai_diem": "thua", "nguoi_giao_bong": "Hungpv",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "unforced_error", "nguoi_ket_thuc": "Hungpv", "ky_thuat_ket_thuc": "go_phai", "nguoi_kien_tao": "", "ky_thuat_kien_tao": "",
                                    "dac_tinh": { "diem_roi_ngang": "", "do_dai": "", "do_xoay": "xuong", "vi_tri_hong": "ra_ngoai" }
                                }
                            },
                            { 
                                "thu_tu_diem": 7, "ty_so_hien_tai": "4-3", "loai_diem": "thang", "nguoi_giao_bong": "Nguyễn Văn A",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "winner", "nguoi_ket_thuc": "Hungpv", "ky_thuat_ket_thuc": "bat_phai", "nguoi_kien_tao": "", "ky_thuat_kien_tao": "",
                                    "dac_tinh": { "diem_roi_ngang": "giua", "do_dai": "dai", "do_xoay": "ngang_len", "vi_tri_hong": "" }
                                }
                            },
                            { 
                                "thu_tu_diem": 8, "ty_so_hien_tai": "4-4", "loai_diem": "thua", "nguoi_giao_bong": "Nguyễn Văn A",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "winner", "nguoi_ket_thuc": "Nguyễn Văn A", "ky_thuat_ket_thuc": "doi_giat_phai", "nguoi_kien_tao": "", "ky_thuat_kien_tao": "",
                                    "dac_tinh": { "diem_roi_ngang": "trai", "do_dai": "ngan", "do_xoay": "ngang_len", "vi_tri_hong": "" }
                                }
                            },
                            { 
                                "thu_tu_diem": 9, "ty_so_hien_tai": "5-4", "loai_diem": "thang", "nguoi_giao_bong": "Hungpv",
                                "chi_tiet_pha_bong": {
                                    "tinh_chat": "forced_error", "nguoi_ket_thuc": "Nguyễn Văn A", "ky_thuat_ket_thuc": "tra_giao_bong", "nguoi_kien_tao": "Hungpv", "ky_thuat_kien_tao": "giao_bong_thuan",
                                    "dac_tinh": { "diem_roi_ngang": "phai", "do_dai": "ngan", "do_xoay": "xuong", "vi_tri_hong": "ruc_luoi" }
                                }
                            }
                        ]
                    }
                ]
            }
        ];"""
    
    new_content = content[:start_idx] + new_block + content[end_idx + len(end_marker):]
    with open("/app/applet/index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("MOCK_MATCHES updated!")
else:
    print("Failed to find MOCK_MATCHES block.")
