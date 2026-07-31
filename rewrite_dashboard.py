import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("function renderDashboard(container) {")
end_idx = content.find("window.updateDashboardFilter =", start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find boundaries")
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

    // NHÓM 1 & 2 VARIABLES
    let totalWin = 0, totalLose = 0;
    let techStats = {};
    if (appState.dict && appState.dict.ky_thuat_rally) {
        Object.keys(appState.dict.ky_thuat_rally).forEach(k => techStats[k] = { win: 0, lose: 0, total: 0 });
    }
    let serveWin = 0, serveTotal = 0, receiveWin = 0, receiveTotal = 0;
    
    // NHÓM 3 & 4 VARIABLES
    let gameAnalysis = [];
    
    filteredMatches.forEach(m => {
        const dt1 = m.thong_tin.doi_thu_1;
        const dt2 = m.thong_tin.doi_thu_2;
        
        (m.chi_tiet_game || []).forEach(g => {
            let gWin = 0, gLose = 0;
            let gServeWin = 0, gServeTotal = 0;
            let gReceiveWin = 0, gReceiveTotal = 0;
            
            let currentWinStreak = 0;
            let currentLoseStreak = 0;
            let maxWinStreak = 0;
            let maxLoseStreak = 0;
            
            let winStreakStartScore = "", winStreakEndScore = "";
            let loseStreakStartScore = "", loseStreakEndScore = "";
            let winStreakStartPt = 0, winStreakEndPt = 0;
            let loseStreakStartPt = 0, loseStreakEndPt = 0;
            
            let tempWinStartScore = "", tempWinStartPt = 0;
            let tempLoseStartScore = "", tempLoseStartPt = 0;
            
            let currentScoreP1 = parseInt((g.ty_so_bat_dau || "0-0").split('-')[0]) || 0;
            let currentScoreP2 = parseInt((g.ty_so_bat_dau || "0-0").split('-')[1]) || 0;
            
            (g.danh_sach_diem || []).forEach((pt, ptIndex) => {
                const p1Before = currentScoreP1;
                const p2Before = currentScoreP2;
                
                if(pt.loai_diem === 'thang') {
                    totalWin++;
                    gWin++;
                    currentScoreP1++;
                    
                    if (currentWinStreak === 0) {
                        tempWinStartScore = `${p1Before}-${p2Before}`;
                        tempWinStartPt = ptIndex + 1;
                    }
                    currentWinStreak++;
                    currentLoseStreak = 0;
                    
                    if (currentWinStreak > maxWinStreak) {
                        maxWinStreak = currentWinStreak;
                        winStreakStartScore = tempWinStartScore;
                        winStreakEndScore = `${currentScoreP1}-${currentScoreP2}`;
                        winStreakStartPt = tempWinStartPt;
                        winStreakEndPt = ptIndex + 1;
                    }
                } else {
                    totalLose++;
                    gLose++;
                    currentScoreP2++;
                    
                    if (currentLoseStreak === 0) {
                        tempLoseStartScore = `${p1Before}-${p2Before}`;
                        tempLoseStartPt = ptIndex + 1;
                    }
                    currentLoseStreak++;
                    currentWinStreak = 0;
                    
                    if (currentLoseStreak > maxLoseStreak) {
                        maxLoseStreak = currentLoseStreak;
                        loseStreakStartScore = tempLoseStartScore;
                        loseStreakEndScore = `${currentScoreP1}-${currentScoreP2}`;
                        loseStreakStartPt = tempLoseStartPt;
                        loseStreakEndPt = ptIndex + 1;
                    }
                }
                
                if(pt.nhom === 'nhom_ky_thuat' && techStats[pt.ky_thuat]) {
                    techStats[pt.ky_thuat].total++;
                    if(pt.loai_diem === 'thang') techStats[pt.ky_thuat].win++; 
                    else techStats[pt.ky_thuat].lose++;
                }
                
                if(pt.nguoi_giao_bong === dt1) {
                    serveTotal++;
                    gServeTotal++;
                    if(pt.loai_diem === 'thang') { serveWin++; gServeWin++; }
                } else if(pt.nguoi_giao_bong === dt2) {
                    receiveTotal++;
                    gReceiveTotal++;
                    if(pt.loai_diem === 'thang') { receiveWin++; gReceiveWin++; }
                }
            });
            
            gameAnalysis.push({
                matchDate: m.thong_tin.ngay_thi_dau,
                matchVs: dt2,
                gameSo: g.game_so,
                tySoBatDau: g.ty_so_bat_dau || "0-0",
                tySoChungCuoc: `${currentScoreP1}-${currentScoreP2}`,
                tongDiem: g.danh_sach_diem?.length || 0,
                gWin,
                gLose,
                gServeTotal, gServeWin,
                gReceiveTotal, gReceiveWin,
                maxWinStreak, winStreakStartScore, winStreakEndScore, winStreakStartPt, winStreakEndPt,
                maxLoseStreak, loseStreakStartScore, loseStreakEndScore, loseStreakStartPt, loseStreakEndPt
            });
        });
    });

    html += `
        <h3 class="font-bold text-gray-700 mb-3 text-lg border-b pb-2">Nhóm 1 & 2: Điểm số, Kỹ thuật và Giao bóng</h3>
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
                <div class="text-xs text-gray-500 font-semibold uppercase mb-1">Thắng khi Mình Giao Bóng</div>
                <div class="text-2xl font-bold text-gray-800">${serveTotal>0 ? Math.round(serveWin/serveTotal*100) : 0}%</div>
                <div class="text-sm text-gray-600 font-medium">${serveWin} / ${serveTotal}</div>
            </div>
            <div class="bg-white p-4 rounded-xl shadow border border-gray-100">
                <div class="text-xs text-gray-500 font-semibold uppercase mb-1">Thắng khi Mình Đỡ Giao</div>
                <div class="text-2xl font-bold text-gray-800">${receiveTotal>0 ? Math.round(receiveWin/receiveTotal*100) : 0}%</div>
                <div class="text-sm text-gray-600 font-medium">${receiveWin} / ${receiveTotal}</div>
            </div>
        </div>
    `;

    html += `<h4 class="font-bold text-gray-700 mb-3 text-md">Hiệu suất Kỹ Thuật Rally</h4><div class="space-y-3 mb-6">`;
    let hasTechStats = false;
    let techArr = [];
    Object.keys(techStats).forEach(k => {
        const s = techStats[k];
        if(s.total === 0 && s.win === 0 && s.lose === 0) return;
        hasTechStats = true;
        
        const successRate = s.total > 0 ? Math.round(s.win / s.total * 100) : 0;
        const winContribution = totalWin > 0 ? Math.round(s.win / totalWin * 100) : 0;
        const loseContribution = totalLose > 0 ? Math.round(s.lose / totalLose * 100) : 0;
        
        techArr.push({ key: k, name: appState.dict.ky_thuat_rally[k], win: s.win, lose: s.lose });
        
        html += `
            <div class="bg-white p-3 rounded-lg shadow-sm border border-gray-100">
                <div class="flex justify-between text-sm font-semibold mb-2">
                    <span class="text-gray-800">${appState.dict.ky_thuat_rally[k]} <span class="text-xs font-normal text-gray-500 ml-1">(Xuất hiện: ${s.total} lần, Thắng: ${s.win}, Thua: ${s.lose})</span></span>
                </div>
                
                <div class="mb-2">
                    <div class="flex justify-between text-xs text-gray-600 mb-1">
                        <span>Tỷ lệ thành công</span>
                        <span class="font-bold text-blue-600">${successRate}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-1.5">
                        <div class="bg-blue-500 h-1.5 rounded-full" style="width: ${successRate}%"></div>
                    </div>
                </div>
                <div class="mb-2">
                    <div class="flex justify-between text-xs text-gray-600 mb-1">
                        <span>Tỷ trọng điểm thắng</span>
                        <span class="font-bold text-green-600">${winContribution}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-1.5">
                        <div class="bg-green-500 h-1.5 rounded-full" style="width: ${winContribution}%"></div>
                    </div>
                </div>
                <div>
                    <div class="flex justify-between text-xs text-gray-600 mb-1">
                        <span>Tỷ trọng điểm thua</span>
                        <span class="font-bold text-red-500">${loseContribution}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-1.5">
                        <div class="bg-red-500 h-1.5 rounded-full" style="width: ${loseContribution}%"></div>
                    </div>
                </div>
            </div>
        `;
    });
    
    if (!hasTechStats) {
        html += `<div class="text-sm text-gray-500 italic">Chưa có dữ liệu kỹ thuật rally cho bộ lọc này.</div>`;
    } else {
        techArr.sort((a,b) => b.win - a.win);
        const topWins = techArr.slice(0,3).filter(t => t.win > 0);
        techArr.sort((a,b) => b.lose - a.lose);
        const topLoses = techArr.slice(0,3).filter(t => t.lose > 0);
        
        html += `<div class="bg-gray-50 p-3 rounded border border-gray-200 text-sm mt-4">`;
        html += `<div class="mb-2"><span class="font-semibold text-green-700">Top 3 ghi điểm:</span> ${topWins.length > 0 ? topWins.map(t => `${t.name} (${t.win})`).join(', ') : 'Không có'}</div>`;
        html += `<div><span class="font-semibold text-red-600">Top 3 mất điểm:</span> ${topLoses.length > 0 ? topLoses.map(t => `${t.name} (${t.lose})`).join(', ') : 'Không có'}</div>`;
        html += `</div>`;
    }
    html += `</div>`;
    
    html += `<h3 class="font-bold text-gray-700 mb-3 text-lg border-b pb-2 mt-8">Nhóm 3 & 4: Phân tích theo Game & Momentum</h3>`;
    
    if (gameAnalysis.length === 0) {
        html += `<div class="text-sm text-gray-500 italic">Chưa có dữ liệu game.</div>`;
    } else {
        let globalMaxWinStreak = 0;
        let globalMaxWinGame = null;
        let globalMaxLoseStreak = 0;
        let globalMaxLoseGame = null;
        
        gameAnalysis.forEach(ga => {
            if (ga.maxWinStreak > globalMaxWinStreak) {
                globalMaxWinStreak = ga.maxWinStreak;
                globalMaxWinGame = ga;
            }
            if (ga.maxLoseStreak > globalMaxLoseStreak) {
                globalMaxLoseStreak = ga.maxLoseStreak;
                globalMaxLoseGame = ga;
            }
        });
        
        html += `<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">`;
        if (globalMaxWinStreak > 0) {
            html += `
                <div class="bg-green-50 p-4 rounded-xl border border-green-200 shadow-sm">
                    <div class="text-sm font-semibold text-green-800 mb-1">Chuỗi thắng liên tiếp dài nhất</div>
                    <div class="text-2xl font-black text-green-600 mb-2">${globalMaxWinStreak} điểm</div>
                    <div class="text-xs text-gray-600 space-y-1">
                        <div><span class="font-medium">Trận:</span> ${globalMaxWinGame.matchDate} (vs ${globalMaxWinGame.matchVs})</div>
                        <div><span class="font-medium">Game:</span> ${globalMaxWinGame.gameSo}</div>
                        <div><span class="font-medium">Từ điểm:</span> ${globalMaxWinGame.winStreakStartPt} đến ${globalMaxWinGame.winStreakEndPt}</div>
                        <div><span class="font-medium">Tỷ số:</span> ${globalMaxWinGame.winStreakStartScore} &rarr; ${globalMaxWinGame.winStreakEndScore}</div>
                    </div>
                </div>
            `;
        }
        if (globalMaxLoseStreak > 0) {
            html += `
                <div class="bg-red-50 p-4 rounded-xl border border-red-200 shadow-sm">
                    <div class="text-sm font-semibold text-red-800 mb-1">Chuỗi thua liên tiếp dài nhất</div>
                    <div class="text-2xl font-black text-red-600 mb-2">${globalMaxLoseStreak} điểm</div>
                    <div class="text-xs text-gray-600 space-y-1">
                        <div><span class="font-medium">Trận:</span> ${globalMaxLoseGame.matchDate} (vs ${globalMaxLoseGame.matchVs})</div>
                        <div><span class="font-medium">Game:</span> ${globalMaxLoseGame.gameSo}</div>
                        <div><span class="font-medium">Từ điểm:</span> ${globalMaxLoseGame.loseStreakStartPt} đến ${globalMaxLoseGame.loseStreakEndPt}</div>
                        <div><span class="font-medium">Tỷ số:</span> ${globalMaxLoseGame.loseStreakStartScore} &rarr; ${globalMaxLoseGame.loseStreakEndScore}</div>
                    </div>
                </div>
            `;
        }
        if(globalMaxWinStreak > 0 || globalMaxLoseStreak > 0) {
            html += `<div class="col-span-1 sm:col-span-2 text-xs text-gray-400 italic text-right">* Nếu có nhiều chuỗi dài bằng nhau, chuỗi xuất hiện sớm nhất sẽ được hiển thị.</div>`;
        }
        html += `</div>`;
        
        html += `
            <div class="overflow-x-auto bg-white rounded-lg shadow border border-gray-200">
                <table class="min-w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-gray-100 text-gray-700 uppercase text-xs">
                        <tr>
                            <th class="px-3 py-2 border-b">Trận/Game</th>
                            <th class="px-3 py-2 border-b">Tỷ số</th>
                            <th class="px-3 py-2 border-b">Tổng Điểm</th>
                            <th class="px-3 py-2 border-b text-green-600">Thắng</th>
                            <th class="px-3 py-2 border-b text-red-500">Thua</th>
                            <th class="px-3 py-2 border-b">Thắng Giao Bóng</th>
                            <th class="px-3 py-2 border-b">Thắng Đỡ Giao</th>
                            <th class="px-3 py-2 border-b text-green-600">Chuỗi Thắng</th>
                            <th class="px-3 py-2 border-b text-red-500">Chuỗi Thua</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                        ${gameAnalysis.map(ga => {
                            const serveRate = ga.gServeTotal > 0 ? Math.round(ga.gServeWin/ga.gServeTotal*100) : 0;
                            const receiveRate = ga.gReceiveTotal > 0 ? Math.round(ga.gReceiveWin/ga.gReceiveTotal*100) : 0;
                            return `
                                <tr class="hover:bg-gray-50">
                                    <td class="px-3 py-2">
                                        <div class="font-medium text-gray-800">${ga.matchVs}</div>
                                        <div class="text-xs text-gray-500">${ga.matchDate} - G${ga.gameSo}</div>
                                    </td>
                                    <td class="px-3 py-2 text-gray-700 font-semibold">${ga.tySoBatDau} &rarr; ${ga.tySoChungCuoc}</td>
                                    <td class="px-3 py-2 text-center">${ga.tongDiem}</td>
                                    <td class="px-3 py-2 text-green-600 font-bold">${ga.gWin}</td>
                                    <td class="px-3 py-2 text-red-500 font-bold">${ga.gLose}</td>
                                    <td class="px-3 py-2 text-gray-600">${serveRate}% <span class="text-xs">(${ga.gServeWin}/${ga.gServeTotal})</span></td>
                                    <td class="px-3 py-2 text-gray-600">${receiveRate}% <span class="text-xs">(${ga.gReceiveWin}/${ga.gReceiveTotal})</span></td>
                                    <td class="px-3 py-2 text-green-600 font-semibold">${ga.maxWinStreak}</td>
                                    <td class="px-3 py-2 text-red-500 font-semibold">${ga.maxLoseStreak}</td>
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

new_content = content[:start_idx] + new_func + "\n        " + content[end_idx:]

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated renderDashboard")
