import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add heatmap objects to s
s_target = "        spin: {},"
s_replacement = """        spin: {},
        heatmapWinner: { ngan_trai: 0, ngan_giua: 0, ngan_phai: 0, dai_trai: 0, dai_giua: 0, dai_phai: 0 },
        heatmapLost: { ngan_trai: 0, ngan_giua: 0, ngan_phai: 0, dai_trai: 0, dai_giua: 0, dai_phai: 0 },"""
content = content.replace(s_target, s_replacement)

# 2. Fix the loop logic
old_spin_logic = """                // Spin
                const dac_tinh = c.dac_tinh;
                if (dac_tinh && dac_tinh.do_xoay) {
                    if (!s.spin[dac_tinh.do_xoay]) s.spin[dac_tinh.do_xoay] = { total: 0, win: 0, forcedErrorByMe: 0, forcedErrorAgainstMe: 0 };
                    s.spin[dac_tinh.do_xoay].total++;
                    if (isWin) s.spin[dac_tinh.do_xoay].win++;
                    
                    if (c.tinh_chat === 'forced_error') {
                        if (c.nguoi_kien_tao === me) s.spin[dac_tinh.do_xoay].forcedErrorByMe++;
                        if (c.nguoi_ket_thuc === me) s.spin[dac_tinh.do_xoay].forcedErrorAgainstMe++;
                    }
                }"""

new_spin_logic = """                // Heatmap & Spin
                const dac_tinh = c.dac_tinh;
                if (dac_tinh) {
                    if (dac_tinh.diem_roi_ngang && dac_tinh.do_dai) {
                        const key = `${dac_tinh.do_dai}_${dac_tinh.diem_roi_ngang}`;
                        if (isWin) s.heatmapWinner[key] = (s.heatmapWinner[key] || 0) + 1;
                        else s.heatmapLost[key] = (s.heatmapLost[key] || 0) + 1;
                    }
                    if (dac_tinh.do_xoay) {
                        if (!s.spin[dac_tinh.do_xoay]) s.spin[dac_tinh.do_xoay] = { total: 0, win: 0, forcedErrorByMe: 0, forcedErrorAgainstMe: 0 };
                        s.spin[dac_tinh.do_xoay].total++;
                        if (isWin) s.spin[dac_tinh.do_xoay].win++;
                        
                        if (c.tinh_chat === 'forced_error') {
                            if (c.nguoi_kien_tao === me) s.spin[dac_tinh.do_xoay].forcedErrorByMe++;
                            if (c.nguoi_ket_thuc === me) s.spin[dac_tinh.do_xoay].forcedErrorAgainstMe++;
                        }
                    }
                }"""
content = content.replace(old_spin_logic, new_spin_logic)

# 3. Add heatmap render
render_target = """    html += `<div><h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">2. Tactical Analytics & Spin</h2>`;
    
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">PHÂN TÍCH ĐỘ XOÁY</h3>`;"""

render_replacement = """    html += `<div><h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">2. Tactical Analytics & Spin</h2>`;
    
    html += `<div class="grid grid-cols-2 gap-4 mb-4">
        <div class="bg-white rounded-xl shadow-sm border p-3">
            <h3 class="text-xs font-bold text-gray-800 text-center mb-2">ĐIỂM RƠI GHI ĐIỂM (THẮNG)</h3>
            <div class="grid grid-cols-3 gap-1 relative bg-blue-100 p-1 border-2 border-blue-300">
                <div class="absolute inset-0 border-b-2 border-dashed border-blue-300 pointer-events-none" style="top: 50%"></div>
                <div class="bg-blue-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Trái</div><div class="font-black text-blue-800">${s.heatmapWinner['ngan_trai']||0}</div></div>
                <div class="bg-blue-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Giữa</div><div class="font-black text-blue-800">${s.heatmapWinner['ngan_giua']||0}</div></div>
                <div class="bg-blue-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Phải</div><div class="font-black text-blue-800">${s.heatmapWinner['ngan_phai']||0}</div></div>
                <div class="bg-blue-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Trái</div><div class="font-black text-blue-900">${s.heatmapWinner['dai_trai']||0}</div></div>
                <div class="bg-blue-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Giữa</div><div class="font-black text-blue-900">${s.heatmapWinner['dai_giua']||0}</div></div>
                <div class="bg-blue-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Phải</div><div class="font-black text-blue-900">${s.heatmapWinner['dai_phai']||0}</div></div>
            </div>
        </div>
        <div class="bg-white rounded-xl shadow-sm border p-3">
            <h3 class="text-xs font-bold text-gray-800 text-center mb-2">ĐIỂM RƠI BỊ MẤT ĐIỂM (THUA)</h3>
            <div class="grid grid-cols-3 gap-1 relative bg-red-100 p-1 border-2 border-red-300">
                <div class="absolute inset-0 border-b-2 border-dashed border-red-300 pointer-events-none" style="top: 50%"></div>
                <div class="bg-red-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Trái</div><div class="font-black text-red-800">${s.heatmapLost['ngan_trai']||0}</div></div>
                <div class="bg-red-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Giữa</div><div class="font-black text-red-800">${s.heatmapLost['ngan_giua']||0}</div></div>
                <div class="bg-red-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Phải</div><div class="font-black text-red-800">${s.heatmapLost['ngan_phai']||0}</div></div>
                <div class="bg-red-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Trái</div><div class="font-black text-red-900">${s.heatmapLost['dai_trai']||0}</div></div>
                <div class="bg-red-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Giữa</div><div class="font-black text-red-900">${s.heatmapLost['dai_giua']||0}</div></div>
                <div class="bg-red-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Phải</div><div class="font-black text-red-900">${s.heatmapLost['dai_phai']||0}</div></div>
            </div>
        </div>
    </div>`;

    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">PHÂN TÍCH ĐỘ XOÁY</h3>`;"""
content = content.replace(render_target, render_replacement)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated successfully")
