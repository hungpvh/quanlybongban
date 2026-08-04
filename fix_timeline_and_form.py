import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update timeline render logic
timeline_target = """                                            `<br><span class="text-blue-500 font-medium">` + (pt.chi_tiet_pha_bong.tinh_chat === 'winner' ? 'Thông số đường bóng ghi điểm: ' : 'Thông số đường bóng trước khi đánh hỏng: ') + `</span><span class="text-blue-500">` + 
                                            [
                                                pt.chi_tiet_pha_bong.dac_tinh.do_xoay ? appState.dict.thuoc_tinh_bong.do_xoay[pt.chi_tiet_pha_bong.dac_tinh.do_xoay] || pt.chi_tiet_pha_bong.dac_tinh.do_xoay : '',
                                                pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'trai' ? 'Trái' : pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'giua' ? 'Giữa' : pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'phai' ? 'Phải' : '',
                                                pt.chi_tiet_pha_bong.dac_tinh.do_dai === 'ngan' ? 'Ngắn' : pt.chi_tiet_pha_bong.dac_tinh.do_dai === 'dai' ? 'Dài' : ''
                                            ].filter(Boolean).join(' - ') + `</span>` """

timeline_replacement = """                                            `<br><span class="text-blue-500 font-medium">` + (pt.chi_tiet_pha_bong.tinh_chat === 'winner' ? 'Thông số đường bóng ghi điểm: ' : 'Thông số đường bóng trước khi đánh hỏng: ') + `</span><span class="text-blue-500">` + 
                                            [
                                                pt.chi_tiet_pha_bong.tinh_chat !== 'winner' && pt.chi_tiet_pha_bong.ky_thuat_kien_tao ? (appState.dict.ky_thuat_rally[pt.chi_tiet_pha_bong.ky_thuat_kien_tao] || appState.dict.loai_giao_bong[pt.chi_tiet_pha_bong.ky_thuat_kien_tao] || pt.chi_tiet_pha_bong.ky_thuat_kien_tao) : '',
                                                pt.chi_tiet_pha_bong.dac_tinh.do_xoay ? appState.dict.thuoc_tinh_bong.do_xoay[pt.chi_tiet_pha_bong.dac_tinh.do_xoay] || pt.chi_tiet_pha_bong.dac_tinh.do_xoay : '',
                                                pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'trai' ? 'Trái' : pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'giua' ? 'Giữa' : pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'phai' ? 'Phải' : '',
                                                pt.chi_tiet_pha_bong.dac_tinh.do_dai === 'ngan' ? 'Ngắn' : pt.chi_tiet_pha_bong.dac_tinh.do_dai === 'dai' ? 'Dài' : ''
                                            ].filter(Boolean).join(' - ') + `</span>` """

content = content.replace(timeline_target, timeline_replacement)

# 2. Update renderTechSelect
tech_select_target = """            const renderTechSelect = (label, key) => `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">${label}</label>
                    <div class="grid grid-cols-2 gap-2 mb-2">
                        ${serveKeys.map(k => `<button onclick="updatePtState('${key}', '${k}')" class="p-3 rounded-xl font-semibold text-xs border transition ${s[key]===k?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${appState.dict.loai_giao_bong[k]}</button>`).join('')}
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        ${techKeys.map(k => `<button onclick="updatePtState('${key}', '${k}')" class="p-2 rounded-xl font-semibold text-xs border transition ${s[key]===k?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${appState.dict.ky_thuat_rally[k]}</button>`).join('')}
                    </div>
                </div>
            `;"""

tech_select_replacement = """            const renderTechSelect = (label, key, hideServe = false) => `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">${label}</label>
                    ${!hideServe ? `
                    <div class="grid grid-cols-2 gap-2 mb-2">
                        ${serveKeys.map(k => `<button onclick="updatePtState('${key}', '${k}')" class="p-3 rounded-xl font-semibold text-xs border transition ${s[key]===k?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${appState.dict.loai_giao_bong[k]}</button>`).join('')}
                    </div>` : ''}
                    <div class="grid grid-cols-3 gap-2">
                        ${techKeys.map(k => `<button onclick="updatePtState('${key}', '${k}')" class="p-2 rounded-xl font-semibold text-xs border transition ${s[key]===k?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${appState.dict.ky_thuat_rally[k]}</button>`).join('')}
                    </div>
                </div>
            `;"""

content = content.replace(tech_select_target, tech_select_replacement)

# 3. Update the form logic for forced_error
form_logic_target = """            if (s.tinh_chat === 'winner') {
                html += renderPlayerSelect("Người ghi điểm (Kết thúc)", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật kết thúc", "ky_thuat_ket_thuc");
            } else if (s.tinh_chat === 'forced_error') {
                html += renderPlayerSelect("Người kiến tạo (Ép)", "nguoi_kien_tao");
                html += renderTechSelect("Kỹ thuật kiến tạo", "ky_thuat_kien_tao");
                html += renderPlayerSelect("Người đánh hỏng", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật đánh hỏng", "ky_thuat_ket_thuc");
                html += renderViTriHong();
            } else if (s.tinh_chat === 'unforced_error') {
                html += renderPlayerSelect("Người đánh hỏng", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật đánh hỏng", "ky_thuat_ket_thuc");
                html += renderViTriHong();
            }"""

form_logic_replacement = """            if (s.tinh_chat === 'winner') {
                html += renderPlayerSelect("Người ghi điểm (Kết thúc)", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật kết thúc", "ky_thuat_ket_thuc");
            } else if (s.tinh_chat === 'forced_error') {
                const hideServe = s.loai_diem === 'thua';
                html += renderPlayerSelect("Người kiến tạo (Ép)", "nguoi_kien_tao");
                html += renderTechSelect("Kỹ thuật kiến tạo", "ky_thuat_kien_tao", hideServe);
                html += renderPlayerSelect("Người đánh hỏng", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật đánh hỏng", "ky_thuat_ket_thuc", hideServe);
                html += renderViTriHong();
            } else if (s.tinh_chat === 'unforced_error') {
                html += renderPlayerSelect("Người đánh hỏng", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật đánh hỏng", "ky_thuat_ket_thuc");
                html += renderViTriHong();
            }"""

content = content.replace(form_logic_target, form_logic_replacement)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated successfully.")
