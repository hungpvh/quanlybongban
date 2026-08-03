import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update MOCK_DICTIONARY
old_dict_regex = r"const MOCK_DICTIONARY = \{.*?\};"
new_dict = """const MOCK_DICTIONARY = {
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
        "giao_bong_thuan": "Giao bóng con lắc thuận tay (Pendulum)",
        "giao_bong_trai": "Giao bóng trái tay",
        "giao_bong_con_lac_nguoc": "Giao bóng con lắc ngược (Reverse Pendulum)",
        "giao_bong_duc": "Giao bóng đục",
        "giao_bong_tomahawk": "Giao bóng Tomahawk"
    },
    "thuoc_tinh_bong": {
        "diem_roi_ngang": { "trai": "Trái tay (Backhand)", "giua": "Giữa bàn (Middle)", "phai": "Phải tay (Forehand)" },
        "do_dai": { "ngan": "Ngắn (2 nảy)", "dai": "Dài (Ra ngoài bàn)" },
        "do_xoay": { "xuong": "Xoáy xuống", "len": "Xoáy lên", "long": "Bóng lỏng" }
    },
    "thuoc_tinh_loi": {
        "vi_tri_hong": { "ruc_luoi": "Rúc lưới", "ra_ngoai_dai": "Ra ngoài cạnh đáy", "ra_ngoai_bien": "Ra ngoài cạnh bên", "truot_bong": "Đánh hụt" }
    }
};"""
content = re.sub(old_dict_regex, new_dict, content, flags=re.DOTALL)

# 2. Update modal header
old_header = r"\$\{s\.tinh_chat === 'winner' \? 'Điểm trực tiếp' : s\.tinh_chat === 'forced_error' \? 'Bị ép đánh hỏng' : 'Tự đánh hỏng'\}"
new_header = "${appState.dict.tinh_chat_pha_bong[s.tinh_chat] || s.tinh_chat}"
content = re.sub(old_header, new_header, content)

# 3. Update nature selection buttons
old_btn_winner = r"Điểm trực tiếp \(Winner\)"
new_btn_winner = "${appState.dict.tinh_chat_pha_bong.winner || 'Điểm trực tiếp'}"
content = re.sub(old_btn_winner, new_btn_winner, content)

old_btn_forced = r"Bị ép đánh hỏng \(Forced Error\)"
new_btn_forced = "${appState.dict.tinh_chat_pha_bong.forced_error || 'Bị ép đánh hỏng'}"
content = re.sub(old_btn_forced, new_btn_forced, content)

old_btn_unforced = r"Tự đánh hỏng \(Unforced Error\)"
new_btn_unforced = "${appState.dict.tinh_chat_pha_bong.unforced_error || 'Tự đánh hỏng'}"
content = re.sub(old_btn_unforced, new_btn_unforced, content)

# 4. Update renderDiemRoi
old_renderDiemRoi = r"""const renderDiemRoi = \(\) => \{
                const isWin = s\.loai_diem === 'thang';
                const cols = isWin \? \['phai', 'giua', 'trai'\] : \['trai', 'giua', 'phai'\];
                return `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Điểm rơi & Độ dài \(Góc nhìn của bạn\)</label>
                    <div class="grid grid-cols-3 gap-2">
                        \$\{cols\.map\(col => \{
                            const btnDai = `<button onclick="updateDiemRoi\('\$\{col\}', 'dai'\)" class="p-3 rounded-xl font-bold text-xs border transition \$\{\(s\.dac_tinh\.diem_roi_ngang===col && s\.dac_tinh\.do_dai==='dai'\)\?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'\}">Dài<br>\$\{col==='trai'\?'Trái':col==='giua'\?'Giữa':'Phải'\}</button>`;
                            const btnNgan = `<button onclick="updateDiemRoi\('\$\{col\}', 'ngan'\)" class="p-3 rounded-xl font-bold text-xs border transition \$\{\(s\.dac_tinh\.diem_roi_ngang===col && s\.dac_tinh\.do_dai==='ngan'\)\?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'\}">Ngắn<br>\$\{col==='trai'\?'Trái':col==='giua'\?'Giữa':'Phải'\}</button>`;
                            return `<div class="flex flex-col gap-2">
                                \$\{isWin \? btnDai : btnNgan\}
                                \$\{isWin \? btnNgan : btnDai\}
                            </div>`;
                        \}\)\.join\(''\)\}
                    </div>
                </div>
            `\};"""

new_renderDiemRoi = """const renderDiemRoi = () => {
                const isWin = s.loai_diem === 'thang';
                // Lấy danh sách keys từ từ điển thay vì fix cứng 'trai', 'giua', 'phai'
                // Nếu dict có các key khác, vẫn render được.
                const allCols = Object.keys(appState.dict.thuoc_tinh_bong.diem_roi_ngang);
                // Giữ logic đảo ngược thứ tự cột nếu là điểm thắng để UI thuận góc nhìn
                const cols = isWin ? [...allCols].reverse() : allCols;
                return `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Điểm rơi & Độ dài (Góc nhìn của bạn)</label>
                    <div class="grid grid-cols-${cols.length} gap-2">
                        ${cols.map(col => {
                            const tenDai = appState.dict.thuoc_tinh_bong.do_dai.dai || 'Dài';
                            const tenNgan = appState.dict.thuoc_tinh_bong.do_dai.ngan || 'Ngắn';
                            const tenNgang = appState.dict.thuoc_tinh_bong.diem_roi_ngang[col] || col;
                            const btnDai = `<button onclick="updateDiemRoi('${col}', 'dai')" class="p-2 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='dai')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${tenDai}<br>${tenNgang}</button>`;
                            const btnNgan = `<button onclick="updateDiemRoi('${col}', 'ngan')" class="p-2 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='ngan')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${tenNgan}<br>${tenNgang}</button>`;
                            return `<div class="flex flex-col gap-2">
                                ${isWin ? btnDai : btnNgan}
                                ${isWin ? btnNgan : btnDai}
                            </div>`;
                        }).join('')}
                    </div>
                </div>
            `};"""
content = re.sub(old_renderDiemRoi, new_renderDiemRoi, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
