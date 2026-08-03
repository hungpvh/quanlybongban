import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_timeline = r"""                                <div>
                                    <div class="font-bold text-gray-800">\$\{name\} <span class="text-xs font-semibold px-1\.5 py-0\.5 rounded ml-1 bg-gray-100 \$\{ptColor\}">\$\{ptName\}</span></div>
                                    <div class="text-xs text-gray-500 mt-0\.5">Giao: \$\{pt\.nguoi_giao_bong\} &bull; #\$\{pt\.thu_tu_diem\}</div>
                                </div>"""

new_timeline = """                                <div>
                                    <div class="font-bold text-gray-800">${name} <span class="text-xs font-semibold px-1.5 py-0.5 rounded ml-1 bg-gray-100 ${ptColor}">${ptName}</span></div>
                                    <div class="text-xs text-gray-500 mt-0.5">
                                        Giao: ${pt.nguoi_giao_bong} &bull; #${pt.thu_tu_diem}
                                        ${pt.chi_tiet_pha_bong && pt.chi_tiet_pha_bong.dac_tinh && (pt.chi_tiet_pha_bong.dac_tinh.do_xoay || pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang || pt.chi_tiet_pha_bong.dac_tinh.do_dai) ? 
                                            `<br><span class="text-blue-500">` + 
                                            [
                                                pt.chi_tiet_pha_bong.dac_tinh.do_xoay ? appState.dict.thuoc_tinh_bong.do_xoay[pt.chi_tiet_pha_bong.dac_tinh.do_xoay] || pt.chi_tiet_pha_bong.dac_tinh.do_xoay : '',
                                                pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'trai' ? 'Trái' : pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'giua' ? 'Giữa' : pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang === 'phai' ? 'Phải' : '',
                                                pt.chi_tiet_pha_bong.dac_tinh.do_dai === 'ngan' ? 'Ngắn' : pt.chi_tiet_pha_bong.dac_tinh.do_dai === 'dai' ? 'Dài' : ''
                                            ].filter(Boolean).join(' - ') + `</span>` 
                                        : ''}
                                    </div>
                                </div>"""

content = re.sub(old_timeline, new_timeline, content)

content = content.replace("FORCED ERROR (Kiến tạo ép lỗi)", "Ép đối thủ đánh hỏng")
content = content.replace("UNFORCED ERROR (Theo kỹ thuật)", "Bị ép nên tự đánh hỏng")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
