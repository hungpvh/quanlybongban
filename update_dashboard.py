import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find renderDashboard function
start_idx = content.find("function renderDashboard(container) {")
if start_idx == -1:
    print("Could not find renderDashboard")
    exit(1)

# Find the end of renderDashboard by looking for the next top-level comment or function
# The next one is `// --- SETTINGS ---` or `function renderSettings(container)`
end_idx = content.find("// --- SETTINGS ---", start_idx)
if end_idx == -1:
    end_idx = content.find("function renderSettings(", start_idx)

if end_idx == -1:
    print("Could not find end of renderDashboard")
    exit(1)

new_func = """function renderDashboard(container) {
    if(appState.matches.length === 0) {
        container.innerHTML = `<div class="text-center py-10 text-gray-500">Chưa có dữ liệu thống kê.</div>`;
        return;
    }
    
    if (!appState.dashboardFilter) {
        appState.dashboardFilter = { matchId: appState.currentMatchId || 'all', fromDate: '', toDate: '', loai_hinh: 'all', doi_thu: 'all', _lastMatchId: appState.currentMatchId };
    } else if (appState.currentMatchId !== appState.dashboardFilter._lastMatchId) {
        appState.dashboardFilter.matchId = appState.currentMatchId || 'all';
        appState.dashboardFilter._lastMatchId = appState.currentMatchId;
    }

    const f = appState.dashboardFilter;

    // Filter matches
    let filteredMatches = appState.matches.filter(m => {
        if (f.matchId !== 'all' && m.id !== f.matchId) return false;
        if (f.fromDate && m.thong_tin.ngay_thi_dau < f.fromDate) return false;
        if (f.toDate && m.thong_tin.ngay_thi_dau > f.toDate) return false;
        if (f.loai_hinh !== 'all' && m.thong_tin.loai_hinh !== f.loai_hinh) return false;
        if (f.doi_thu !== 'all' && m.thong_tin.doi_thu_1 !== f.doi_thu && m.thong_tin.doi_thu_2 !== f.doi_thu) return false;
        return true;
    });

    const uniqueLoaiHinh = [...new Set(appState.matches.map(m => m.thong_tin.loai_hinh).filter(Boolean))];
    const uniqueDoiThu = [...new Set(appState.matches.map(m => m.thong_tin.doi_thu_1).concat(appState.matches.map(m => m.thong_tin.doi_thu_2)).filter(Boolean))];
    const matchOptions = appState.matches.map(m => `<option value="${m.id}" ${f.matchId === m.id ? 'selected' : ''}>${m.thong_tin.ngay_thi_dau} - ${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}</option>`).join('');

    let html = `<h2 class="text-xl font-bold mb-4">Dashboard Phân Tích</h2>`;

    // Filter UI
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
    let techStats = {};
    if (appState.dict && appState.dict.ky_thuat_rally) {
        Object.keys(appState.dict.ky_thuat_rally).forEach(k => techStats[k] = { win: 0, lose: 0, total: 0 });
    }
    let serveWin = 0, serveTotal = 0, receiveWin = 0, receiveTotal = 0;
    
    filteredMatches.forEach(m => {
        const dt1 = m.thong_tin.doi_thu_1;
        (m.chi_tiet_game || []).forEach(g => {
            (g.danh_sach_diem || []).forEach(pt => {
                if(pt.loai_diem === 'thang') totalWin++; else totalLose++;
                if(pt.nhom === 'nhom_ky_thuat' && techStats[pt.ky_thuat]) {
                    techStats[pt.ky_thuat].total++;
                    if(pt.loai_diem === 'thang') techStats[pt.ky_thuat].win++; else techStats[pt.ky_thuat].lose++;
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

    html += `<h3 class="font-bold text-gray-700 mb-3">Hiệu suất Kỹ Thuật Rally</h3><div class="space-y-3 mb-6">`;
    let hasTechStats = false;
    Object.keys(techStats).forEach(k => {
        const s = techStats[k];
        if(s.total === 0) return;
        hasTechStats = true;
        const winRate = Math.round(s.win / s.total * 100);
        const winRatio = totalWin > 0 ? Math.round(s.win / totalWin * 100) : 0;
        const loseRatio = totalLose > 0 ? Math.round(s.lose / totalLose * 100) : 0;
        
        html += `
            <div class="bg-white p-3 rounded-lg shadow-sm border border-gray-100">
                <div class="flex justify-between text-sm font-semibold mb-2">
                    <span>${appState.dict.ky_thuat_rally[k]}</span>
                    <span class="text-blue-600">${winRate}% Thành công (${s.win}/${s.total})</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-1.5 mb-2">
                    <div class="bg-blue-500 h-1.5 rounded-full" style="width: ${winRate}%"></div>
                </div>
                <div class="flex text-xs text-gray-500 justify-between">
                    <span>Đóng góp thắng: ${winRatio}%</span>
                    <span>Chiếm tỷ lệ thua: ${loseRatio}%</span>
                </div>
            </div>
        `;
    });
    if (!hasTechStats) {
        html += `<div class="text-sm text-gray-500 italic">Chưa có dữ liệu kỹ thuật rally cho bộ lọc này.</div>`;
    }
    html += `</div>`;
    
    container.innerHTML = html;
}

window.updateDashboardFilter = function(key, value) {
    appState.dashboardFilter[key] = value;
    renderView('dashboard');
};

window.clearDashboardFilter = function() {
    appState.dashboardFilter = { matchId: 'all', fromDate: '', toDate: '', loai_hinh: 'all', doi_thu: 'all', _lastMatchId: 'all' };
    renderView('dashboard');
};
"""

new_content = content[:start_idx] + new_func + "\n        " + content[end_idx:]

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully updated renderDashboard")
