import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("function renderDashboard(container) {")
end_idx = content.find("window.updateDashboardFilter", start_idx)

new_func = """function renderDashboard(container) {
    let f = appState.dashboardFilter;
    if (f.matchId === 'all') f = { ...f, matchId: appState.matches[0]?.id_tran_dau || 'all' };
    
    let filteredMatches = appState.matches.filter(m => {
        if (f.matchId !== 'all' && m.id_tran_dau !== f.matchId) return false;
        if (f.fromDate && m.thong_tin.ngay_thi_dau < f.fromDate) return false;
        if (f.toDate && m.thong_tin.ngay_thi_dau > f.toDate) return false;
        if (f.loai_hinh !== 'all' && m.thong_tin.loai_hinh !== f.loai_hinh) return false;
        if (f.doi_thu !== 'all' && m.thong_tin.doi_thu_1 !== f.doi_thu && m.thong_tin.doi_thu_2 !== f.doi_thu) return false;
        return true;
    });

    const uniqueLoaiHinh = [...new Set(appState.matches.map(m => m.thong_tin.loai_hinh).filter(Boolean))];
    const uniqueDoiThu = [...new Set(appState.matches.map(m => m.thong_tin.doi_thu_1).concat(appState.matches.map(m => m.thong_tin.doi_thu_2)).filter(Boolean))];
    const matchOptions = appState.matches.map(m => `<option value="${m.id_tran_dau}" ${f.matchId === m.id_tran_dau ? 'selected' : ''}>${m.thong_tin.ngay_thi_dau} - ${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}</option>`).join('');

    let html = `<h2 class="text-xl font-bold mb-4">Dashboard Phân Tích</h2>`;

    html += `
        <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 mb-6 space-y-3">
            <div class="flex justify-between items-center">
                <h3 class="font-semibold text-sm text-gray-700"><i class="fas fa-filter"></i> Lọc dữ liệu</h3>
                <button onclick="clearDashboardFilter()" class="text-xs text-blue-600 hover:underline">Xóa bộ lọc</button>
            </div>
            <div class="grid grid-cols-2 gap-3">
                <div class="col-span-2">
                    <label class="block text-xs text-gray-500 mb-1">Trận đấu cụ thể</label>
                    <select id="df_matchId" class="w-full border rounded p-1.5 text-sm" onchange="updateDashboardFilter('matchId', this.value)">
                        <option value="all">-- Tất cả trận đấu --</option>
                        ${matchOptions}
                    </select>
                </div>
                <div>
                    <label class="block text-xs text-gray-500 mb-1">Từ ngày</label>
                    <input type="date" id="df_fromDate" class="w-full border rounded p-1.5 text-sm" value="${f.fromDate}" onchange="updateDashboardFilter('fromDate', this.value)">
                </div>
                <div>
                    <label class="block text-xs text-gray-500 mb-1">Đến ngày</label>
                    <input type="date" id="df_toDate" class="w-full border rounded p-1.5 text-sm" value="${f.toDate}" onchange="updateDashboardFilter('toDate', this.value)">
                </div>
                <div>
                    <label class="block text-xs text-gray-500 mb-1">Loại hình</label>
                    <select id="df_loai_hinh" class="w-full border rounded p-1.5 text-sm" onchange="updateDashboardFilter('loai_hinh', this.value)">
                        <option value="all">-- Tất cả --</option>
                        ${uniqueLoaiHinh.map(lh => `<option value="${lh}" ${f.loai_hinh === lh ? 'selected' : ''}>${appState.dict?.loai_hinh?.[lh] || lh}</option>`).join('')}
                    </select>
                </div>
                <div>
                    <label class="block text-xs text-gray-500 mb-1">Đối thủ</label>
                    <select id="df_doi_thu" class="w-full border rounded p-1.5 text-sm" onchange="updateDashboardFilter('doi_thu', this.value)">
                        <option value="all">-- Tất cả --</option>
                        ${uniqueDoiThu.map(dt => `<option value="${dt}" ${f.doi_thu === dt ? 'selected' : ''}>${dt}</option>`).join('')}
                    </select>
                </div>
            </div>
        </div>
    `;

    if (filteredMatches.length === 0) {
        html += `<div class="text-center py-10 text-gray-500">Không có dữ liệu phù hợp với tiêu chí lọc.</div>`;
        container.innerHTML = html;
        return;
    }

    let totalWin = 0, totalLose = 0;
    
    // Stats structure: { tech_key: { toi_ghi_diem: 0, doi_thu_danh_hong: 0, toi_danh_hong: 0, doi_thu_ghi_diem: 0, total: 0 } }
    let rallyStats = {};
    let serveStats = {};

    if (appState.dict && appState.dict.ky_thuat_rally) {
        Object.keys(appState.dict.ky_thuat_rally).forEach(k => rallyStats[k] = { toi_ghi_diem: 0, doi_thu_danh_hong: 0, toi_danh_hong: 0, doi_thu_ghi_diem: 0, total: 0 });
    }
    if (appState.dict && appState.dict.loai_giao_bong) {
        Object.keys(appState.dict.loai_giao_bong).forEach(k => serveStats[k] = { toi_ghi_diem: 0, doi_thu_danh_hong: 0, toi_danh_hong: 0, doi_thu_ghi_diem: 0, total: 0 });
    }

    let serveWin = 0, serveTotal = 0, receiveWin = 0, receiveTotal = 0;
    
    filteredMatches.forEach(m => {
        const dt1 = m.thong_tin.doi_thu_1;
        (m.chi_tiet_game || []).forEach(g => {
            (g.danh_sach_diem || []).forEach(pt => {
                if(pt.loai_diem === 'thang') totalWin++; else totalLose++;
                
                const phuong_thuc = pt.phuong_thuc || (pt.loai_diem === 'thang' ? 'toi_ghi_diem' : 'toi_danh_hong'); // fallback

                if(pt.nhom === 'nhom_ky_thuat' && rallyStats[pt.ky_thuat]) {
                    rallyStats[pt.ky_thuat].total++;
                    if(rallyStats[pt.ky_thuat][phuong_thuc] !== undefined) {
                        rallyStats[pt.ky_thuat][phuong_thuc]++;
                    }
                }
                if(pt.nhom === 'nhom_giao_bong' && serveStats[pt.ky_thuat]) {
                    serveStats[pt.ky_thuat].total++;
                    if(serveStats[pt.ky_thuat][phuong_thuc] !== undefined) {
                        serveStats[pt.ky_thuat][phuong_thuc]++;
                    }
                }

                if(pt.nguoi_giao_bong === dt1) {
                    serveTotal++;
                    if(pt.loai_diem === 'thang') serveWin++;
                } else {
                    receiveTotal++;
                    if(pt.loai_diem === 'thang') receiveWin++;
                }
            });
        });
    });

    html += `
        <div class="grid grid-cols-2 gap-4 mb-6">
            <div class="bg-blue-600 text-white p-4 rounded-xl shadow">
                <div class="text-sm opacity-80">Tổng Điểm Thắng</div>
                <div class="text-3xl font-black">${totalWin}</div>
            </div>
            <div class="bg-yellow-500 text-white p-4 rounded-xl shadow">
                <div class="text-sm opacity-80">Tổng Điểm Thua</div>
                <div class="text-3xl font-black">${totalLose}</div>
            </div>
            <div class="bg-white p-4 rounded-xl shadow border border-gray-100">
                <div class="text-xs text-gray-500 font-semibold uppercase mb-1">Mình Giao Bóng</div>
                <div class="text-2xl font-bold text-gray-800">${serveTotal>0 ? Math.round(serveWin/serveTotal*100) : 0}%</div>
                <div class="text-xs text-gray-400">Thắng ${serveWin}/${serveTotal}</div>
            </div>
            <div class="bg-white p-4 rounded-xl shadow border border-gray-100">
                <div class="text-xs text-gray-500 font-semibold uppercase mb-1">Mình Đỡ Giao</div>
                <div class="text-2xl font-bold text-gray-800">${receiveTotal>0 ? Math.round(receiveWin/receiveTotal*100) : 0}%</div>
                <div class="text-xs text-gray-400">Thắng ${receiveWin}/${receiveTotal}</div>
            </div>
        </div>
    `;

    // Render Stats Function
    const renderStatTable = (title, statsDict, dictMap) => {
        let hasData = false;
        let tableHtml = `<h3 class="font-bold text-gray-700 mb-3">${title}</h3><div class="overflow-x-auto mb-6 bg-white rounded-lg shadow-sm border border-gray-100">
            <table class="w-full text-left text-xs">
                <thead class="bg-gray-50 border-b">
                    <tr>
                        <th class="p-2 border-r font-semibold text-gray-600" rowspan="2">Loại</th>
                        <th class="p-2 border-r text-center font-semibold text-blue-700" colspan="2">Điểm Thắng</th>
                        <th class="p-2 text-center font-semibold text-red-600" colspan="2">Điểm Thua</th>
                    </tr>
                    <tr class="bg-gray-50 border-b">
                        <th class="p-2 border-r border-t text-center text-blue-600">Tôi ghi điểm</th>
                        <th class="p-2 border-r border-t text-center text-blue-500">Đối thủ hỏng</th>
                        <th class="p-2 border-r border-t text-center text-red-600">Tôi đánh hỏng</th>
                        <th class="p-2 border-t text-center text-red-500">Đối thủ ghi điểm</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">`;
        
        Object.keys(statsDict).forEach(k => {
            const s = statsDict[k];
            if(s.total === 0) return;
            hasData = true;
            tableHtml += `
                <tr class="hover:bg-gray-50">
                    <td class="p-2 border-r font-medium text-gray-800">${dictMap[k] || k}</td>
                    <td class="p-2 border-r text-center text-blue-700 font-bold bg-blue-50/30">${s.toi_ghi_diem}</td>
                    <td class="p-2 border-r text-center text-blue-600 bg-blue-50/10">${s.doi_thu_danh_hong}</td>
                    <td class="p-2 border-r text-center text-red-700 font-bold bg-red-50/30">${s.toi_danh_hong}</td>
                    <td class="p-2 text-center text-red-600 bg-red-50/10">${s.doi_thu_ghi_diem}</td>
                </tr>
            `;
        });
        
        tableHtml += `</tbody></table></div>`;
        if (!hasData) {
            return `<h3 class="font-bold text-gray-700 mb-3">${title}</h3><div class="text-sm text-gray-500 italic mb-6">Chưa có dữ liệu.</div>`;
        }
        return tableHtml;
    };

    html += renderStatTable("Hiệu suất Giao bóng (Điểm trực tiếp)", serveStats, appState.dict.loai_giao_bong);
    html += renderStatTable("Hiệu suất Kỹ Thuật Rally", rallyStats, appState.dict.ky_thuat_rally);

    container.innerHTML = html;
}
"""

new_content = content[:start_idx] + new_func + "\n        " + content[end_idx:]

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
