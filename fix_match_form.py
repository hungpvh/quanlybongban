import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update dictionary
old_dict_regex = r"const MOCK_DICTIONARY = \{.*?\};"
new_dict = """const MOCK_DICTIONARY = {
  "thong_tin_tran_dau": {
    "ngay_thi_dau": "Ngày thi đấu",
    "loai_hinh": "Loại hình (Giao hữu / Đánh bia / Giải đấu)",
    "doi_thu_1": "Tên của bạn",
    "doi_thu_2": "Tên đối thủ",
    "chap_bong": "Thông tin chấp bóng",
    "ket_qua": "Tỷ số chung cuộc",
    "mo_ta": "Ghi chú & Phân tích trận đấu",
    "link_youtube": "Video YouTube",
    "link_facebook": "Video Facebook",
    "link_khac": "Video lưu trữ khác"
  },
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
    "diem_roi_ngang": {
      "trai": "Trái tay (Backhand)",
      "giua": "Giữa bàn (Middle)",
      "phai": "Phải tay (Forehand)"
    },
    "do_dai": {
      "ngan": "Ngắn (2 nảy)",
      "dai": "Dài"
    },
    "do_xoay": {
      "xuong": "Xoáy xuống",
      "len": "Xoáy lên",
      "long": "Bóng lỏng"
    }
  },
  "thuoc_tinh_loi": {
    "vi_tri_hong": {
      "ruc_luoi": "Rúc lưới",
      "ra_ngoai_dai": "Ra ngoài cạnh đáy",
      "ra_ngoai_bien": "Ra ngoài cạnh bên",
      "truot_bong": "Đánh hụt"
    }
  }
};"""
content = re.sub(old_dict_regex, new_dict, content, flags=re.DOTALL)

# Re-write renderMatchForm and handleMatchSubmit
old_block_regex = r"function renderMatchForm\(container, editId = null\) \{.*?}        // --- MATCH DETAIL \(GAMES LIST\) ---"

new_block = """function renderMatchForm(container, editId = null) {
            let match = { thong_tin: { ngay_thi_dau: new Date().toISOString().split('T')[0], loai_hinh: 'Giao hữu', doi_thu_1: 'Tôi' } };
            if (editId) match = appState.matches.find(m => m.id_tran_dau === editId) || match;
            const info = match.thong_tin || {};
            const schema = appState.dict.thong_tin_tran_dau || {};
            
            let formHtml = '';
            Object.keys(schema).forEach(key => {
                const label = schema[key];
                const value = info[key] || '';
                
                if (key === 'ngay_thi_dau') {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="date" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm" required></div>`;
                } else if (key === 'mo_ta') {
                    formHtml += `<div class="col-span-1 md:col-span-2"><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><textarea id="mf_${key}" rows="2" class="w-full border rounded p-2 text-sm">${escapeHtml(value)}</textarea></div>`;
                } else if (key.startsWith('link_')) {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="url" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm"></div>`;
                } else if (key === 'loai_hinh') {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="text" id="mf_${key}" list="loai_hinh_list" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm" required><datalist id="loai_hinh_list"><option value="Giao hữu"></option><option value="Đánh bia"></option><option value="Thi đấu giải"></option></datalist></div>`;
                } else if (key === 'doi_thu_1' || key === 'doi_thu_2' || key === 'ket_qua') {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="text" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm" required></div>`;
                } else {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="text" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm"></div>`;
                }
            });

            container.innerHTML = `
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
                    <h2 class="text-xl font-bold mb-4">${editId ? 'Sửa trận đấu' : 'Thêm trận đấu mới'}</h2>
                    <form id="match-form" class="space-y-4" onsubmit="handleMatchSubmit(event, '${editId}')">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            ${formHtml}
                        </div>
                        <div class="flex gap-2 pt-4">
                            <button type="button" onclick="renderView('list')" class="flex-1 bg-gray-200 text-gray-800 py-2 rounded-lg font-medium">Hủy</button>
                            <button type="submit" class="flex-1 bg-blue-600 text-white py-2 rounded-lg font-medium">Lưu trận đấu</button>
                        </div>
                    </form>
                </div>
            `;
        }

        async function handleMatchSubmit(e, editId) {
            e.preventDefault();
            const schema = appState.dict.thong_tin_tran_dau || {};
            const info = {};
            Object.keys(schema).forEach(key => {
                const el = document.getElementById(`mf_${key}`);
                if (el) {
                    info[key] = el.value;
                }
            });
            if (editId && editId !== 'null') {
                const match = appState.matches.find(m => m.id_tran_dau === editId);
                if(match) match.thong_tin = info;
            } else {
                appState.matches.unshift({ id_tran_dau: `match_${Date.now()}`, thong_tin: info, chi_tiet_game: [] });
            }
            await saveToGithub();
        }

        // --- MATCH DETAIL (GAMES LIST) ---"""

content = re.sub(old_block_regex, new_block, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done replace renderMatchForm")
