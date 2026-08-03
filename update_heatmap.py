import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update rHeatmap in Dashboard
old_rheatmap = """    const rHeatmap = (data, title, overlayColorClass, reverseCols = false) => {
        const total = Object.values(data).reduce((a,b)=>a+b,0) || 1;
        const cell = (k) => {
            const c = data[k]||0; const pct = Math.round(c/total*100);
            const textColor = c > 0 ? (pct > 40 ? 'text-white' : 'text-gray-900') : 'text-gray-400';
            const overlayOp = c > 0 ? (pct / 100).toFixed(2) : '0';
            return `<div class="border p-2 flex flex-col items-center justify-center h-20 bg-gray-50 relative overflow-hidden"><div class="absolute inset-0 ${overlayColorClass}" style="opacity: ${overlayOp}"></div><span class="relative z-10 font-bold text-lg ${textColor}">${c}</span><span class="relative z-10 text-[10px] font-semibold ${textColor}">${pct}%</span></div>`;
        };
        const cols = reverseCols ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
        return `
            <div class="flex-1">
                <div class="text-xs font-bold text-center mb-2 uppercase text-gray-600">${title}</div>
                <div class="grid grid-cols-3 gap-0.5 border bg-gray-200">
                    ${cell('dai_' + cols[0])}${cell('dai_' + cols[1])}${cell('dai_' + cols[2])}
                    ${cell('ngan_' + cols[0])}${cell('ngan_' + cols[1])}${cell('ngan_' + cols[2])}
                </div>
                <div class="flex justify-between text-[10px] text-gray-500 mt-1 px-1">
                    <span>${cols[0]==='trai'?'Trái':'Phải'}</span>
                    <span>Giữa</span>
                    <span>${cols[2]==='trai'?'Trái':'Phải'}</span>
                </div>
            </div>
        `;
    };"""

new_rheatmap = """    const rHeatmap = (data, title, overlayColorClass, reverseCols = false, reverseRows = false) => {
        const total = Object.values(data).reduce((a,b)=>a+b,0) || 1;
        const cell = (k) => {
            const c = data[k]||0; const pct = Math.round(c/total*100);
            const textColor = c > 0 ? (pct > 40 ? 'text-white' : 'text-gray-900') : 'text-gray-400';
            const overlayOp = c > 0 ? (pct / 100).toFixed(2) : '0';
            return `<div class="border p-2 flex flex-col items-center justify-center h-20 bg-gray-50 relative overflow-hidden"><div class="absolute inset-0 ${overlayColorClass}" style="opacity: ${overlayOp}"></div><span class="relative z-10 font-bold text-lg ${textColor}">${c}</span><span class="relative z-10 text-[10px] font-semibold ${textColor}">${pct}%</span></div>`;
        };
        const cols = reverseCols ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
        const row1 = reverseRows ? `${cell('ngan_' + cols[0])}${cell('ngan_' + cols[1])}${cell('ngan_' + cols[2])}` : `${cell('dai_' + cols[0])}${cell('dai_' + cols[1])}${cell('dai_' + cols[2])}`;
        const row2 = reverseRows ? `${cell('dai_' + cols[0])}${cell('dai_' + cols[1])}${cell('dai_' + cols[2])}` : `${cell('ngan_' + cols[0])}${cell('ngan_' + cols[1])}${cell('ngan_' + cols[2])}`;
        return `
            <div class="flex-1">
                <div class="text-xs font-bold text-center mb-2 uppercase text-gray-600">${title}</div>
                <div class="grid grid-cols-3 gap-0.5 border bg-gray-200">
                    ${row1}
                    ${row2}
                </div>
                <div class="flex justify-between text-[10px] text-gray-500 mt-1 px-1">
                    <span>${cols[0]==='trai'?'Trái':'Phải'}</span>
                    <span>Giữa</span>
                    <span>${cols[2]==='trai'?'Trái':'Phải'}</span>
                </div>
            </div>
        `;
    };"""

content = content.replace(old_rheatmap, new_rheatmap)
content = content.replace("rHeatmap(s.heatmapWinner, 'GHI ĐIỂM (WINNER)', 'bg-blue-600', true)", "rHeatmap(s.heatmapWinner, 'GHI ĐIỂM (WINNER)', 'bg-blue-600', true, false)")
content = content.replace("rHeatmap(s.heatmapLost, 'MẤT ĐIỂM (LỖI)', 'bg-red-600', false)", "rHeatmap(s.heatmapLost, 'MẤT ĐIỂM (LỖI)', 'bg-red-600', false, true)")


# 2. Update renderPtEntryForm logic to show DiemRoi and DoXoay for all
old_tinh_chat_block = """            if (s.tinh_chat === 'winner') {
                html += renderPlayerSelect("Người ghi điểm (Kết thúc)", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật kết thúc", "ky_thuat_ket_thuc");
                html += renderDiemRoi();
                html += renderDoXoay();
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

new_tinh_chat_block = """            if (s.tinh_chat === 'winner') {
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
            }
            html += renderDiemRoi();
            html += renderDoXoay();"""

content = content.replace(old_tinh_chat_block, new_tinh_chat_block)

# 3. Update renderDiemRoi
old_render_diem_roi = """            const renderDiemRoi = () => {
                const isWin = s.loai_diem === 'thang';
                const cols = isWin ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
                return `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Điểm rơi & Độ dài (Góc nhìn của bạn)</label>
                    <div class="grid grid-cols-3 gap-2">
                        ${cols.map(col => `
                            <div class="flex flex-col gap-2">
                                <button onclick="updateDiemRoi('${col}', 'dai')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='dai')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Dài<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                                <button onclick="updateDiemRoi('${col}', 'ngan')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='ngan')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Ngắn<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `};"""

new_render_diem_roi = """            const renderDiemRoi = () => {
                const isWin = s.loai_diem === 'thang';
                const cols = isWin ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
                return `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Điểm rơi & Độ dài (Góc nhìn của bạn)</label>
                    <div class="grid grid-cols-3 gap-2">
                        ${cols.map(col => {
                            const btnDai = `<button onclick="updateDiemRoi('${col}', 'dai')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='dai')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Dài<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>`;
                            const btnNgan = `<button onclick="updateDiemRoi('${col}', 'ngan')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='ngan')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Ngắn<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>`;
                            return `<div class="flex flex-col gap-2">
                                ${isWin ? btnDai : btnNgan}
                                ${isWin ? btnNgan : btnDai}
                            </div>`;
                        }).join('')}
                    </div>
                </div>
            `};"""

content = content.replace(old_render_diem_roi, new_render_diem_roi)

# 4. update savePtEntry to store null for missing properties in dac_tinh
old_save_dac_tinh = """                    dac_tinh: {
                        diem_roi_ngang: s.dac_tinh.diem_roi_ngang,
                        do_dai: s.dac_tinh.do_dai,
                        do_xoay: s.dac_tinh.do_xoay,
                        vi_tri_hong: s.dac_tinh.vi_tri_hong
                    }"""

new_save_dac_tinh = """                    dac_tinh: {
                        diem_roi_ngang: s.dac_tinh.diem_roi_ngang || null,
                        do_dai: s.dac_tinh.do_dai || null,
                        do_xoay: s.dac_tinh.do_xoay || null,
                        vi_tri_hong: s.dac_tinh.vi_tri_hong || null
                    }"""

content = content.replace(old_save_dac_tinh, new_save_dac_tinh)

# Need to do the same for the non-edit save path
old_save_dac_tinh_2 = """                        dac_tinh: {
                            diem_roi_ngang: s.dac_tinh.diem_roi_ngang,
                            do_dai: s.dac_tinh.do_dai,
                            do_xoay: s.dac_tinh.do_xoay,
                            vi_tri_hong: s.dac_tinh.vi_tri_hong
                        }"""
new_save_dac_tinh_2 = """                        dac_tinh: {
                            diem_roi_ngang: s.dac_tinh.diem_roi_ngang || null,
                            do_dai: s.dac_tinh.do_dai || null,
                            do_xoay: s.dac_tinh.do_xoay || null,
                            vi_tri_hong: s.dac_tinh.vi_tri_hong || null
                        }"""
content = content.replace(old_save_dac_tinh_2, new_save_dac_tinh_2)


with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
