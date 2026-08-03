import re
import json

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update MOCK_DICTIONARY
old_mock_dict = r"const MOCK_DICTIONARY = \{[\s\S]*?\};\s*const MOCK_MATCHES ="
new_mock_dict = """const MOCK_DICTIONARY = {
    "thong_tin_tran_dau": { "ngay_thi_dau": "Ngày thi đấu", "loai_hinh": "Loại hình", "doi_thu_1": "Tên Đối thủ 1", "doi_thu_2": "Tên Đối thủ 2", "chap_bong": "Chấp bóng", "ket_qua": "Tỷ số", "mo_ta": "Mô tả", "link_video": "Link video" },
    "tinh_chat_pha_bong": {
        "winner": "Điểm trực tiếp",
        "unforced_error": "Lỗi tự đánh hỏng",
        "forced_error": "Lỗi bị ép đánh hỏng"
    },
    "ky_thuat_rally": {
        "giat_phai": "Giật phải",
        "doi_cong_phai": "Đôi công phải",
        "flick_phai": "Flick / Hất phải",
        "giat_trai": "Giật trái",
        "doi_cong_trai": "Đôi công trái",
        "flick_trai": "Flick / Hất trái",
        "bat_dap_bong": "Bạt / Đập",
        "doi_giat_xa_ban": "Đối giật xa bàn",
        "phong_thu_phai": "Phòng thủ / Kê chặn phải",
        "phong_thu_trai": "Phòng thủ / Kê chặn trái",
        "go_day_bong": "Gò / Cắt / Đẩy",
        "bat_ngan_tha_long": "Bắt ngắn / Thả lỏng",
        "cau_bong_bong": "Câu bóng bổng",
        "loi_khac": "Lỗi khác (Giao hỏng, di chuyển...)"
    },
    "loai_giao_bong": {
        "giao_bong_thuan": "Giao bóng thuận tay",
        "giao_bong_trai": "Giao bóng trái tay",
        "giao_bong_ngoi": "Giao bóng ngồi xổm (Tomahawk)",
        "giao_bong_con_lac": "Giao bóng con lắc (Pendulum)"
    },
    "thuoc_tinh_bong": {
        "diem_roi_ngang": { "trai": "Trái tay (Backhand)", "giua": "Giữa bàn (Middle)", "phai": "Phải tay (Forehand)" },
        "do_dai": { "ngan": "Ngắn (2 nảy)", "dai": "Dài (Ra ngoài bàn)" },
        "do_xoay": { "xuong": "Xoáy xuống", "len": "Xoáy lên", "long": "Bóng lỏng" }
    },
    "thuoc_tinh_loi": {
        "vi_tri_hong": { "ruc_luoi": "Rúc lưới", "ra_ngoai_dai": "Ra ngoài cạnh đáy", "ra_ngoai_bien": "Ra ngoài cạnh bên", "truot_bong": "Đánh hụt" }
    }
};

const MOCK_MATCHES ="""

content = re.sub(old_mock_dict, new_mock_dict, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
