import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("function renderDashboard(container) {")
end_idx = content.find("window.updateDashboardFilter", start_idx)

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

    let f = appState.dashboardFilter;

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
    let serveWin = 0, serveTotal = 0, receiveWin = 0, receiveTotal = 0;
    
    let rallyStats = {};
    let serveStats = {};
    let gameAnalysis = [];

    if (appState.dict && appState.dict.ky_thuat_rally) {
        Object.keys(appState.dict.ky_thuat_rally).forEach(k => rallyStats[k] = { toi_ghi_diem: 0, doi_thu_danh_hong: 0, toi_danh_hong: 0, doi_thu_ghi_diem: 0, total: 0, win: 0, lose: 0 });
    }
    if (appState.dict && appState.dict.loai_giao_bong) {
        Object.keys(appState.dict.loai_giao_bong).forEach(k => serveStats[k] = { toi_ghi_diem: 0, doi_thu_danh_hong: 0, toi_danh_hong: 0, doi_thu_ghi_diem: 0, total: 0, win: 0, lose: 0 });
    }

    let globalMaxWinStreakObj = null;
    let globalMaxLoseStreakObj = null;

    filteredMatches.forEach(m => {
        const dt1 = m.thong_tin.doi_thu_1;
        (m.chi_tiet_game || []).forEach(g => {
            let gWin = 0, gLose = 0;
            let gServeTotal = 0, gServeWin = 0;
            let gReceiveTotal = 0, gReceiveWin = 0;

            let curWinStreak = 0, maxWinStreak = 0;
            let winStart = 0, winEnd = 0, maxWinStart = 0, maxWinEnd = 0;
            let curLoseStreak = 0, maxLoseStreak = 0;
            let loseStart = 0, loseEnd = 0, maxLoseStart = 0, maxLoseEnd = 0;

            const calcScoreAt = (idx) => {
                if (idx < 0) return g.ty_so_bat_dau || "0-0";
                if (idx >= g.danh_sach_diem.length) return g.danh_sach_diem[g.danh_sach_diem.length-1].ty_so_hien_tai;
                return g.danh_sach_diem[idx].ty_so_hien_tai;
            };

            (g.danh_sach_diem || []).forEach((pt, idx) => {
                const isWin = pt.loai_diem === 'thang';
                if(isWin) {
                    totalWin++; gWin++;
                    curWinStreak++;
                    if (curWinStreak === 1) winStart = pt.thu_tu_diem;
                    winEnd = pt.thu_tu_diem;
                    if (curWinStreak > maxWinStreak) {
                        maxWinStreak = curWinStreak; maxWinStart = winStart; maxWinEnd = winEnd;
                    }
                    curLoseStreak = 0;
                } else {
                    totalLose++; gLose++;
                    curLoseStreak++;
                    if (curLoseStreak === 1) loseStart = pt.thu_tu_diem;
                    loseEnd = pt.thu_tu_diem;
                    if (curLoseStreak > maxLoseStreak) {
                        maxLoseStreak = curLoseStreak; maxLoseStart = loseStart; maxLoseEnd = loseEnd;
                    }
                    curWinStreak = 0;
                }
                
                const phuong_thuc = pt.phuong_thuc || (isWin ? 'toi_ghi_diem' : 'toi_danh_hong');

                if(pt.nhom === 'nhom_ky_thuat' && rallyStats[pt.ky_thuat]) {
                    rallyStats[pt.ky_thuat].total++;
                    if (isWin) rallyStats[pt.ky_thuat].win++; else rallyStats[pt.ky_thuat].lose++;
                    if(rallyStats[pt.ky_thuat][phuong_thuc] !== undefined) rallyStats[pt.ky_thuat][phuong_thuc]++;
                }
                if(pt.nhom === 'nhom_giao_bong' && serveStats[pt.ky_thuat]) {
                    serveStats[pt.ky_thuat].total++;
                    if (isWin) serveStats[pt.ky_thuat].win++; else serveStats[pt.ky_thuat].lose++;
                    if(serveStats[pt.ky_thuat][phuong_thuc] !== undefined) serveStats[pt.ky_thuat][phuong_thuc]++;
                }

                if(pt.nguoi_giao_bong === dt1) {
                    serveTotal++; gServeTotal++;
                    if(isWin) { serveWin++; gServeWin++; }
                } else {
                    receiveTotal++; gReceiveTotal++;
                    if(isWin) { receiveWin++; gReceiveWin++; }
                }
            });

            const winObj = { len: maxWinStreak, match: `${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}`, game: g.game_so, startPt: maxWinStart, endPt: maxWinEnd, startScore: calcScoreAt(maxWinStart-2), endScore: calcScoreAt(maxWinEnd-1) };
            const loseObj = { len: maxLoseStreak, match: `${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}`, game: g.game_so, startPt: maxLoseStart, endPt: maxLoseEnd, startScore: calcScoreAt(maxLoseStart-2), endScore: calcScoreAt(maxLoseEnd-1) };

            if (!globalMaxWinStreakObj || winObj.len > globalMaxWinStreakObj.len) globalMaxWinStreakObj = winObj;
            if (!globalMaxLoseStreakObj || loseObj.len > globalMaxLoseStreakObj.len) globalMaxLoseStreakObj = loseObj;

            gameAnalysis.push({
                matchVs: `${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}`,
                matchDate: m.thong_tin.ngay_thi_dau,
                gameSo: g.game_so,
                tySoBatDau: g.ty_so_bat_dau || "0-0",
                tySoChungCuoc: (g.danh_sach_diem && g.danh_sach_diem.length > 0) ? g.danh_sach_diem[g.danh_sach_diem.length-1].ty_so_hien_tai : (g.ty_so_bat_dau || "0-0"),
                tongDiem: g.danh_sach_diem.length,
                gWin, gLose, gServeWin, gServeTotal, gReceiveWin, gReceiveTotal,
                maxWinStreak, maxLoseStreak
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

    const formatPct = (val, total, grandTotal) => {
        if (grandTotal === 0) return `0 <span class="text-gray-400 font-normal">(0%)</span>`;
        const pct = Math.round(val / grandTotal * 100);
        return `${val} <span class="text-gray-500 font-normal">(${pct}%)</span>`;
    };

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
                    <td class="p-2 border-r text-center text-blue-700 font-bold bg-blue-50/30">${formatPct(s.toi_ghi_diem, totalWin, totalWin)}</td>
                    <td class="p-2 border-r text-center text-blue-600 bg-blue-50/10">${formatPct(s.doi_thu_danh_hong, totalWin, totalWin)}</td>
                    <td class="p-2 border-r text-center text-red-700 font-bold bg-red-50/30">${formatPct(s.toi_danh_hong, totalLose, totalLose)}</td>
                    <td class="p-2 text-center text-red-600 bg-red-50/10">${formatPct(s.doi_thu_ghi_diem, totalLose, totalLose)}</td>
                </tr>
            `;
        });
        
        tableHtml += `</tbody></table></div>`;
        if (!hasData) return `<h3 class="font-bold text-gray-700 mb-3">${title}</h3><div class="text-sm text-gray-500 italic mb-6">Chưa có dữ liệu.</div>`;
        return tableHtml;
    };

    html += renderStatTable("Hiệu suất Giao bóng (Điểm trực tiếp)", serveStats, appState.dict.loai_giao_bong);
    html += renderStatTable("Hiệu suất Kỹ Thuật Rally", rallyStats, appState.dict.ky_thuat_rally);

    // Top 3 conclusions for Rally
    let rallyArr = Object.keys(rallyStats).map(k => ({ name: appState.dict.ky_thuat_rally[k], ...rallyStats[k] })).filter(x => x.total > 0);
    rallyArr.sort((a,b) => b.win - a.win);
    const topWin = rallyArr.slice(0,3).filter(x => x.win > 0);
    rallyArr.sort((a,b) => b.lose - a.lose);
    const topLose = rallyArr.slice(0,3).filter(x => x.lose > 0);

    html += `<div class="bg-blue-50 p-4 rounded-xl border border-blue-100 mb-4 shadow-sm">
        <h4 class="font-bold text-blue-800 mb-2"><i class="fas fa-trophy text-yellow-500 mr-1"></i> Top Kỹ thuật Ghi điểm (Thắng)</h4>
        ${topWin.length ? `<ul class="list-disc pl-5 text-sm text-blue-900 space-y-1">
            ${topWin.map(x => `<li><strong>${x.name}</strong>: ${x.win} điểm (${Math.round(x.win/totalWin*100)}%)</li>`).join('')}
        </ul>` : `<div class="text-sm text-blue-700">Chưa có dữ liệu</div>`}
    </div>`;

    html += `<div class="bg-red-50 p-4 rounded-xl border border-red-100 mb-8 shadow-sm">
        <h4 class="font-bold text-red-800 mb-2"><i class="fas fa-exclamation-triangle text-orange-500 mr-1"></i> Top Kỹ thuật Mất điểm (Thua)</h4>
        ${topLose.length ? `<ul class="list-disc pl-5 text-sm text-red-900 space-y-1">
            ${topLose.map(x => `<li><strong>${x.name}</strong>: ${x.lose} điểm (${Math.round(x.lose/totalLose*100)}%)</li>`).join('')}
        </ul>` : `<div class="text-sm text-red-700">Chưa có dữ liệu</div>`}
    </div>`;

    html += `<h3 class="font-bold text-gray-700 mb-3">Chuỗi điểm & Momentum</h3>`;
    html += `<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">`;
    if(globalMaxWinStreakObj && globalMaxWinStreakObj.len > 0) {
        html += `<div class="bg-white rounded-xl shadow-sm border border-green-200 p-4">
            <div class="text-xs uppercase font-bold text-green-600 mb-1">Chuỗi Thắng Dài Nhất</div>
            <div class="text-3xl font-black text-green-700 mb-2">${globalMaxWinStreakObj.len} <span class="text-lg font-bold">điểm</span></div>
            <div class="text-sm text-gray-600 space-y-1">
                <div><span class="text-gray-400">Trận:</span> ${globalMaxWinStreakObj.match}</div>
                <div><span class="text-gray-400">Game:</span> ${globalMaxWinStreakObj.game}</div>
                <div><span class="text-gray-400">Điểm số:</span> #${globalMaxWinStreakObj.startPt} đến #${globalMaxWinStreakObj.endPt}</div>
                <div><span class="text-gray-400">Tỷ số:</span> ${globalMaxWinStreakObj.startScore} &rarr; ${globalMaxWinStreakObj.endScore}</div>
            </div>
        </div>`;
    } else {
        html += `<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 text-center text-gray-400 text-sm flex items-center justify-center">Chưa có chuỗi thắng</div>`;
    }

    if(globalMaxLoseStreakObj && globalMaxLoseStreakObj.len > 0) {
        html += `<div class="bg-white rounded-xl shadow-sm border border-red-200 p-4">
            <div class="text-xs uppercase font-bold text-red-500 mb-1">Chuỗi Thua Dài Nhất</div>
            <div class="text-3xl font-black text-red-600 mb-2">${globalMaxLoseStreakObj.len} <span class="text-lg font-bold">điểm</span></div>
            <div class="text-sm text-gray-600 space-y-1">
                <div><span class="text-gray-400">Trận:</span> ${globalMaxLoseStreakObj.match}</div>
                <div><span class="text-gray-400">Game:</span> ${globalMaxLoseStreakObj.game}</div>
                <div><span class="text-gray-400">Điểm số:</span> #${globalMaxLoseStreakObj.startPt} đến #${globalMaxLoseStreakObj.endPt}</div>
                <div><span class="text-gray-400">Tỷ số:</span> ${globalMaxLoseStreakObj.startScore} &rarr; ${globalMaxLoseStreakObj.endScore}</div>
            </div>
        </div>`;
    } else {
        html += `<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 text-center text-gray-400 text-sm flex items-center justify-center">Chưa có chuỗi thua</div>`;
    }
    html += `</div>`;

    if (gameAnalysis.length > 0) {
        html += `<h3 class="font-bold text-gray-700 mb-3">Phân tích theo Game</h3>`;
        html += `
            <div class="overflow-x-auto bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
                <table class="min-w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-gray-50 text-gray-700 uppercase text-[10px] sm:text-xs">
                        <tr>
                            <th class="px-2 py-2 border-b border-r">Trận/Game</th>
                            <th class="px-2 py-2 border-b border-r">Tỷ số</th>
                            <th class="px-2 py-2 border-b border-r text-center">Tổng Điểm</th>
                            <th class="px-2 py-2 border-b border-r text-green-600 text-center">Thắng</th>
                            <th class="px-2 py-2 border-b border-r text-red-500 text-center">Thua</th>
                            <th class="px-2 py-2 border-b border-r text-center">Thắng Giao Bóng</th>
                            <th class="px-2 py-2 border-b border-r text-center">Thắng Đỡ Giao</th>
                            <th class="px-2 py-2 border-b border-r text-green-600 text-center">Chuỗi Thắng</th>
                            <th class="px-2 py-2 border-b text-red-500 text-center">Chuỗi Thua</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                        ${gameAnalysis.map(ga => {
                            const serveRate = ga.gServeTotal > 0 ? Math.round(ga.gServeWin/ga.gServeTotal*100) : 0;
                            const receiveRate = ga.gReceiveTotal > 0 ? Math.round(ga.gReceiveWin/ga.gReceiveTotal*100) : 0;
                            return `
                                <tr class="hover:bg-gray-50">
                                    <td class="px-2 py-2 border-r">
                                        <div class="font-medium text-gray-800">${ga.matchVs}</div>
                                        <div class="text-xs text-gray-500">${ga.matchDate} - G${ga.gameSo}</div>
                                    </td>
                                    <td class="px-2 py-2 border-r text-gray-700 font-semibold">${ga.tySoBatDau} &rarr; ${ga.tySoChungCuoc}</td>
                                    <td class="px-2 py-2 border-r text-center">${ga.tongDiem}</td>
                                    <td class="px-2 py-2 border-r text-green-600 font-bold text-center">${ga.gWin}</td>
                                    <td class="px-2 py-2 border-r text-red-500 font-bold text-center">${ga.gLose}</td>
                                    <td class="px-2 py-2 border-r text-gray-600 text-center">${serveRate}% <span class="text-xs">(${ga.gServeWin}/${ga.gServeTotal})</span></td>
                                    <td class="px-2 py-2 border-r text-gray-600 text-center">${receiveRate}% <span class="text-xs">(${ga.gReceiveWin}/${ga.gReceiveTotal})</span></td>
                                    <td class="px-2 py-2 border-r text-green-600 font-semibold text-center">${ga.maxWinStreak}</td>
                                    <td class="px-2 py-2 text-red-500 font-semibold text-center">${ga.maxLoseStreak}</td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    container.innerHTML = html;
}
"""

new_content = content[:start_idx] + new_func + "\n" + content[end_idx:]

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
