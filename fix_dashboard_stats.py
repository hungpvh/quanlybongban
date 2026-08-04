import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the whole block from calculateDashboardStats to the end of renderDashboard
start_idx = content.find("function calculateDashboardStats(")
end_idx = content.find("window.updateDashboardPerspective = function(pers)")

if start_idx != -1 and end_idx != -1:
    old_code = content[start_idx:end_idx]
    
    new_code = """function calculateDashboardStats(filteredMatches, perspective = 'doi_thu_1') {
    const s = {
        matches: { total: 0, win: 0 },
        games: { total: 0, win: 0 },
        points: { total: 0, win: 0, lose: 0 },
        
        winnerByMe: 0, forcedErrorByMe: 0, unforcedErrorByMe: 0, forcedErrorAgainstMe: 0,
        opponentStats: { winner: 0, forced: 0, unforced: 0 },
        
        technique: {}, 
        
        serve: { total: 0, win: 0 },
        receive: { total: 0, win: 0 },
        serveByType: {},
        serveByGame: {},
        
        maxWinStreak: 0, maxForcedStreak: 0, maxUnforcedStreak: 0,
        
        gameSummary: [], 
        
        spin: {},
    };

    filteredMatches.forEach(m => {
        s.matches.total++;
        let mWins = 0, mLoses = 0;
        const me = perspective === 'doi_thu_1' ? m.thong_tin.doi_thu_1 : m.thong_tin.doi_thu_2;
        const opp = perspective === 'doi_thu_1' ? m.thong_tin.doi_thu_2 : m.thong_tin.doi_thu_1;

        if (m.chi_tiet_game) m.chi_tiet_game.forEach((g, gIndex) => {
            s.games.total++;
            let gWins = 0, gLoses = 0;
            let currentWinStreak = 0;
            let currentForcedStreak = 0;
            let currentUnforcedStreak = 0;
            
            let gWinnerMe = 0, gForcedMe = 0, gUnforcedMe = 0;
            
            // For Serve By Game
            const gameKey = `Game ${g.game_so}`;
            if (!s.serveByGame[gameKey]) s.serveByGame[gameKey] = { total: 0, win: 0 };

            if (g.danh_sach_diem) g.danh_sach_diem.forEach(pt => {
                const c = pt.chi_tiet_pha_bong;
                if (!c) return;
                
                s.points.total++;
                const isWin = perspective === 'doi_thu_1' ? pt.loai_diem === 'thang' : pt.loai_diem === 'thua';
                if (isWin) { s.points.win++; gWins++; } else { s.points.lose++; gLoses++; }

                // Serve
                if (pt.nguoi_giao_bong === me) {
                    s.serve.total++;
                    s.serveByGame[gameKey].total++;
                    if (isWin) {
                        s.serve.win++;
                        s.serveByGame[gameKey].win++;
                    }
                    
                    // Serve by type if it's the ending technique
                    if (c.ky_thuat_ket_thuc && appState.dict.loai_giao_bong && appState.dict.loai_giao_bong[c.ky_thuat_ket_thuc]) {
                        const t = c.ky_thuat_ket_thuc;
                        if (!s.serveByType[t]) s.serveByType[t] = { total: 0, win: 0 };
                        s.serveByType[t].total++;
                        if (isWin) s.serveByType[t].win++;
                    }
                } else {
                    s.receive.total++;
                    if (isWin) s.receive.win++;
                }

                // Streaks
                if (isWin) {
                    currentWinStreak++;
                    if (currentWinStreak > s.maxWinStreak) s.maxWinStreak = currentWinStreak;
                } else currentWinStreak = 0;

                if (isWin && c.tinh_chat === 'forced_error') {
                    currentForcedStreak++;
                    if (currentForcedStreak > s.maxForcedStreak) s.maxForcedStreak = currentForcedStreak;
                } else currentForcedStreak = 0;

                if (!isWin && c.tinh_chat === 'unforced_error') {
                    currentUnforcedStreak++;
                    if (currentUnforcedStreak > s.maxUnforcedStreak) s.maxUnforcedStreak = currentUnforcedStreak;
                } else currentUnforcedStreak = 0;

                // Tinh chat
                if (c.nguoi_ket_thuc === me) {
                    if (c.tinh_chat === 'winner') { s.winnerByMe++; gWinnerMe++; }
                    if (c.tinh_chat === 'unforced_error') { s.unforcedErrorByMe++; gUnforcedMe++; }
                    if (c.tinh_chat === 'forced_error') { s.forcedErrorAgainstMe++; }
                } else if (c.nguoi_ket_thuc === opp) {
                    if (c.tinh_chat === 'winner') { s.opponentStats.winner++; }
                    if (c.tinh_chat === 'unforced_error') { s.opponentStats.unforced++; }
                    if (c.tinh_chat === 'forced_error') { s.opponentStats.forced++; }
                }
                
                if (c.nguoi_kien_tao === me && c.tinh_chat === 'forced_error') {
                    s.forcedErrorByMe++;
                    gForcedMe++;
                }

                // Tech
                const techFinish = c.ky_thuat_ket_thuc;
                const techAssist = c.ky_thuat_kien_tao;
                
                const initTech = (t) => {
                    if (!s.technique[t]) s.technique[t] = { scoring: 0, losing: 0, winner: 0, forcedByMe: 0, unforced: 0, forcedAgainstMe: 0 };
                };
                
                if (techFinish && appState.dict.ky_thuat_rally[techFinish]) {
                    if (c.nguoi_ket_thuc === me) {
                        initTech(techFinish);
                        if (c.tinh_chat === 'winner') { s.technique[techFinish].winner++; s.technique[techFinish].scoring++; }
                        if (c.tinh_chat === 'unforced_error') { s.technique[techFinish].unforced++; s.technique[techFinish].losing++; }
                        if (c.tinh_chat === 'forced_error') { s.technique[techFinish].forcedAgainstMe++; s.technique[techFinish].losing++; }
                    }
                }
                
                if (techAssist && appState.dict.ky_thuat_rally[techAssist]) {
                    if (c.nguoi_kien_tao === me && c.tinh_chat === 'forced_error') {
                        initTech(techAssist);
                        s.technique[techAssist].forcedByMe++;
                        s.technique[techAssist].scoring++;
                    }
                }

                // Spin
                const dac_tinh = c.dac_tinh;
                if (dac_tinh && dac_tinh.do_xoay) {
                    if (!s.spin[dac_tinh.do_xoay]) s.spin[dac_tinh.do_xoay] = { total: 0, win: 0, forcedErrorByMe: 0, forcedErrorAgainstMe: 0 };
                    s.spin[dac_tinh.do_xoay].total++;
                    if (isWin) s.spin[dac_tinh.do_xoay].win++;
                    
                    if (c.tinh_chat === 'forced_error') {
                        if (c.nguoi_kien_tao === me) s.spin[dac_tinh.do_xoay].forcedErrorByMe++;
                        if (c.nguoi_ket_thuc === me) s.spin[dac_tinh.do_xoay].forcedErrorAgainstMe++;
                    }
                }
            });
            if (gWins > gLoses) mWins++; else if (gLoses > gWins) mLoses++;
            
            s.gameSummary.push({
                match: `${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}`,
                game_so: g.game_so,
                pts: g.danh_sach_diem ? g.danh_sach_diem.length : 0,
                winnerMe: gWinnerMe,
                forcedMe: gForcedMe,
                unforcedMe: gUnforcedMe,
                isWin: gWins > gLoses
            });
        });
    });

    return s;
}

function renderDashboard(container) {
    if(appState.matches.length === 0) {
        container.innerHTML = `<div class="text-center py-10 text-gray-500">Chưa có dữ liệu thống kê.</div>`;
        return;
    }
    
    if (!appState.dashboardPerspective) {
        appState.dashboardPerspective = 'doi_thu_1';
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
    
    // Build filter HTML
    let matchOpts = `<option value="all">Tất cả trận</option>`;
    appState.matches.forEach(m => matchOpts += `<option value="${m.id_tran_dau}" ${f.matchId===m.id_tran_dau?'selected':''}>${m.thong_tin.ngay_thi_dau}: ${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}</option>`);
    
    let typeOpts = `<option value="all">Tất cả</option>`;
    [...new Set(appState.matches.map(m=>m.thong_tin.loai_hinh))].forEach(t => typeOpts += `<option value="${t}" ${f.loai_hinh===t?'selected':''}>${t}</option>`);
    
    let oppOpts = `<option value="all">Tất cả</option>`;
    [...new Set(appState.matches.map(m=>m.thong_tin.doi_thu_2))].forEach(o => oppOpts += `<option value="${o}" ${f.doi_thu===o?'selected':''}>${o}</option>`);
    
    let name1 = 'Đối thủ 1';
    let name2 = 'Đối thủ 2';
    if (filteredMatches.length > 0) {
        name1 = filteredMatches[0].thong_tin.doi_thu_1 || 'Đối thủ 1';
        name2 = f.doi_thu !== 'all' ? f.doi_thu : (filteredMatches[0].thong_tin.doi_thu_2 || 'Đối thủ 2');
    }
    
    let html = `
        <div class="fixed top-14 left-0 right-0 z-10 bg-white border-b px-4 py-3 shadow-sm flex flex-col gap-3">
            <div class="max-w-3xl mx-auto flex gap-2 w-full">
                <button onclick="updateDashboardPerspective('doi_thu_1')" class="flex-1 py-1.5 text-sm font-bold rounded-lg transition ${appState.dashboardPerspective === 'doi_thu_1' ? 'bg-blue-600 text-white shadow-sm' : 'bg-gray-100 text-gray-600'}">Đối thủ 1</button>
                <button onclick="updateDashboardPerspective('doi_thu_2')" class="flex-1 py-1.5 text-sm font-bold rounded-lg transition ${appState.dashboardPerspective === 'doi_thu_2' ? 'bg-blue-600 text-white shadow-sm' : 'bg-gray-100 text-gray-600'}">Đối thủ 2</button>
            </div>
            <div class="text-center text-xs font-semibold text-gray-700">Đang phân tích theo góc nhìn: <span class="text-blue-600">${appState.dashboardPerspective === 'doi_thu_1' ? name1 : name2}</span></div>
            <div class="max-w-3xl mx-auto flex gap-2 overflow-x-auto no-scrollbar items-center">
                <select id="dbFilterMatch" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[120px]">${matchOpts}</select>
                <input type="date" id="dbFilterFrom" onchange="updateDashboardFilter()" value="${f.fromDate}" class="border rounded p-1.5 text-xs bg-gray-50">
                <input type="date" id="dbFilterTo" onchange="updateDashboardFilter()" value="${f.toDate}" class="border rounded p-1.5 text-xs bg-gray-50">
                <select id="dbFilterType" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[90px]">${typeOpts}</select>
                <select id="dbFilterOpp" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[90px]">${oppOpts}</select>
            </div>
        </div>
        <div class="mt-44 px-4 max-w-3xl mx-auto space-y-6 pb-20">
    `;

    if (filteredMatches.length === 0) {
        html += `<div class="text-center py-10 text-gray-500">Không có dữ liệu phù hợp với bộ lọc.</div></div>`;
        container.innerHTML = html;
        return;
    }

    const s = calculateDashboardStats(filteredMatches, appState.dashboardPerspective);
    const toPct = (num, den) => den > 0 ? Math.round((num/den)*100) : 0;
    const bar = (pct, color='bg-blue-600') => `<div class="w-full bg-gray-200 rounded-full h-2 mt-1"><div class="${color} h-2 rounded-full" style="width: ${pct}%"></div></div>`;
    const getName = (k) => appState.dict.ky_thuat_rally[k] || appState.dict.loai_giao_bong[k] || k;

    // --- NHÓM 1: Score & Technique ---
    html += `
        <div>
            <h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase">1. Hiệu suất ghi điểm</h2>
            <div class="grid grid-cols-2 gap-3 mb-4">
                <div class="bg-blue-50 border border-blue-100 p-4 rounded-xl text-center shadow-sm">
                    <div class="text-xs font-bold text-blue-600 uppercase mb-1">Win Rate</div>
                    <div class="text-3xl font-black text-blue-800">${toPct(s.points.win, s.points.total)}%</div>
                    <div class="text-xs text-gray-500 mt-1">${s.points.win} / ${s.points.total} điểm</div>
                </div>
                <div class="bg-indigo-50 border border-indigo-100 p-4 rounded-xl text-center shadow-sm">
                    <div class="text-xs font-bold text-indigo-600 uppercase mb-1">Tỷ lệ Giao bóng ăn điểm</div>
                    <div class="text-3xl font-black text-indigo-800">${toPct(s.serve.win, s.serve.total)}%</div>
                    <div class="text-xs text-gray-500 mt-1">${s.serve.win} / ${s.serve.total} giao bóng</div>
                </div>
            </div>
            
            <div class="bg-white rounded-xl shadow-sm border p-4 mb-4">
                <h3 class="font-bold text-gray-800 border-b pb-2 mb-3">HIỆU SUẤT GIAO BÓNG THEO GAME</h3>
                <div class="space-y-2 text-sm">
    `;
    Object.keys(s.serveByGame).forEach(k => {
        html += `<div class="flex justify-between items-center py-1 border-b last:border-0"><span class="font-medium">${k}</span><span class="font-bold text-indigo-600">${toPct(s.serveByGame[k].win, s.serveByGame[k].total)}% (${s.serveByGame[k].win}/${s.serveByGame[k].total})</span></div>`;
    });
    html += `</div></div>`;
    
    if (Object.keys(s.serveByType).length > 0) {
        html += `
            <div class="bg-white rounded-xl shadow-sm border p-4 mb-4">
                <h3 class="font-bold text-gray-800 border-b pb-2 mb-3">HIỆU SUẤT THEO LOẠI GIAO BÓNG (LỖI/ACE TRỰC TIẾP)</h3>
                <div class="space-y-2 text-sm">
        `;
        Object.keys(s.serveByType).forEach(k => {
            html += `<div class="flex justify-between items-center py-1 border-b last:border-0"><span>${getName(k)}</span><span class="font-bold text-indigo-600">${toPct(s.serveByType[k].win, s.serveByType[k].total)}% (${s.serveByType[k].win}/${s.serveByType[k].total})</span></div>`;
        });
        html += `</div></div>`;
    }
            
    html += `
            <div class="bg-white rounded-xl shadow-sm border p-4 mb-4">
                <h3 class="font-bold text-gray-800 border-b pb-2 mb-3 text-blue-700">TÍNH CHẤT ĐIỂM (TÔI ĐÁNH)</h3>
                <div class="grid grid-cols-3 gap-2 text-center mb-4">
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Winner</div><div class="font-black text-green-600 text-2xl">${s.winnerByMe}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Ép đối thủ đánh hỏng</div><div class="font-black text-blue-600 text-2xl">${s.forcedErrorByMe}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Tự đánh hỏng</div><div class="font-black text-red-600 text-2xl">${s.unforcedErrorByMe}</div></div>
                </div>
            </div>
            
            <div class="bg-white rounded-xl shadow-sm border p-4 mb-4">
                <h3 class="font-bold text-gray-800 border-b pb-2 mb-3 text-red-700">TÍNH CHẤT ĐIỂM (ĐỐI THỦ ĐÁNH)</h3>
                <div class="grid grid-cols-3 gap-2 text-center mb-4">
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Winner</div><div class="font-black text-green-600 text-2xl">${s.opponentStats.winner}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Ép tôi đánh hỏng</div><div class="font-black text-blue-600 text-2xl">${s.opponentStats.forced}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Tự đánh hỏng</div><div class="font-black text-red-600 text-2xl">${s.opponentStats.unforced}</div></div>
                </div>
            </div>
        </div>
    `;

    // --- NHÓM 2: TACTICAL ANALYTICS ---
    html += `<div><h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">2. Tactical Analytics & Spin</h2>`;
    
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">PHÂN TÍCH ĐỘ XOÁY</h3>`;
    const spinKeys = Object.keys(s.spin);
    if(spinKeys.length > 0) {
        spinKeys.forEach(k => {
            const sp = s.spin[k];
            const name = appState.dict.thuoc_tinh_bong.do_xoay[k] || k;
            html += `
                <div class="py-2 border-b last:border-0">
                    <div class="flex justify-between items-center mb-1"><span class="font-bold text-sm text-gray-800">${name}</span><span class="text-xs text-gray-500">${sp.total} điểm</span></div>
                    <div class="flex gap-2">
                        <div class="flex-1">
                            <div class="flex justify-between text-[10px] font-bold text-gray-500"><span>Win Rate</span><span>${toPct(sp.win, sp.total)}%</span></div>
                            ${bar(toPct(sp.win, sp.total))}
                        </div>
                        <div class="flex-1">
                            <div class="flex justify-between text-[10px] font-bold text-gray-500"><span>Tỷ lệ bị ép đánh hỏng</span><span>${toPct(sp.forcedErrorAgainstMe, s.points.lose)}%</span></div>
                            ${bar(toPct(sp.forcedErrorAgainstMe, s.points.lose), 'bg-red-500')}
                        </div>
                    </div>
                </div>
            `;
        });
    } else {
        html += `<div class="text-sm text-gray-500">Chưa có dữ liệu phân tích độ xoáy.</div>`;
    }
    html += `</div></div>`;

    // --- NHÓM 3: TOP 10 KỸ THUẬT ---
    html += `<div><h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">3. BẢNG XẾP HẠNG KỸ THUẬT (TOP 10)</h2>`;
    
    // Top 10 Scoring
    const topScoring = Object.keys(s.technique).sort((a,b)=>s.technique[b].scoring - s.technique[a].scoring).filter(k => s.technique[k].scoring > 0).slice(0, 10);
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-green-700 border-b pb-2 mb-3">Top 10 Kỹ thuật ghi điểm (Winner + Ép đối thủ lỗi)</h3>`;
    if(topScoring.length>0) {
        topScoring.forEach(k => {
            const tech = s.technique[k];
            html += `
                <div class="py-2 border-b last:border-0 text-sm flex justify-between items-center">
                    <span class="font-semibold">${getName(k)}</span>
                    <div class="text-right">
                        <span class="font-black text-green-600 text-lg">${tech.scoring}</span>
                        <div class="text-[10px] text-gray-500">${tech.winner} winner &bull; ${tech.forcedByMe} ép lỗi</div>
                    </div>
                </div>
            `;
        });
    } else {
        html += `<div class="text-sm text-gray-500">Chưa có dữ liệu ghi điểm.</div>`;
    }
    html += `</div>`;
    
    // Top 10 Losing
    const topLosing = Object.keys(s.technique).sort((a,b)=>s.technique[b].losing - s.technique[a].losing).filter(k => s.technique[k].losing > 0).slice(0, 10);
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-red-700 border-b pb-2 mb-3">Top 10 Kỹ thuật mất điểm (Tự hỏng + Bị ép lỗi)</h3>`;
    if(topLosing.length>0) {
        topLosing.forEach(k => {
            const tech = s.technique[k];
            html += `
                <div class="py-2 border-b last:border-0 text-sm flex justify-between items-center">
                    <span class="font-semibold">${getName(k)}</span>
                    <div class="text-right">
                        <span class="font-black text-red-600 text-lg">${tech.losing}</span>
                        <div class="text-[10px] text-gray-500">${tech.unforced} tự hỏng &bull; ${tech.forcedAgainstMe} bị ép lỗi</div>
                    </div>
                </div>
            `;
        });
    } else {
        html += `<div class="text-sm text-gray-500">Chưa có dữ liệu mất điểm.</div>`;
    }
    html += `</div></div>`;


    // --- NHÓM 4: Momentum & Game Summary ---
    html += `
        <div>
            <h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">4. Momentum & Tóm tắt Game</h2>
            <div class="bg-white rounded-xl shadow-sm border p-4 mb-4">
                <div class="grid grid-cols-3 gap-2 text-center">
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Chuỗi Thắng</div><div class="font-black text-green-600 text-2xl">${s.maxWinStreak}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Chuỗi Ép lỗi</div><div class="font-black text-blue-600 text-2xl">${s.maxForcedStreak}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Chuỗi Tự hỏng</div><div class="font-black text-red-600 text-2xl">${s.maxUnforcedStreak}</div></div>
                </div>
            </div>
    `;

    if (s.gameSummary.length > 0) {
        html += `
                <div class="bg-white rounded-xl shadow-sm border p-4 overflow-x-auto">
                    <table class="w-full text-xs text-left whitespace-nowrap">
                        <thead class="text-gray-500 bg-gray-50 uppercase border-b">
                            <tr>
                                <th class="px-2 py-2">Game</th>
                                <th class="px-2 py-2 text-center">Pha bóng</th>
                                <th class="px-2 py-2 text-center text-green-600">Winner</th>
                                <th class="px-2 py-2 text-center text-blue-600">Ép hỏng</th>
                                <th class="px-2 py-2 text-center text-red-600">Tự hỏng</th>
                                <th class="px-2 py-2 text-center">Kết quả</th>
                            </tr>
                        </thead>
                        <tbody>
        `;
        s.gameSummary.forEach(g => {
            html += `
                <tr class="border-b last:border-0">
                    <td class="px-2 py-2 font-bold">${g.game_so}</td>
                    <td class="px-2 py-2 text-center">${g.pts}</td>
                    <td class="px-2 py-2 text-center text-green-600 font-semibold">${g.winnerMe}</td>
                    <td class="px-2 py-2 text-center text-blue-600 font-semibold">${g.forcedMe}</td>
                    <td class="px-2 py-2 text-center text-red-600 font-semibold">${g.unforcedMe}</td>
                    <td class="px-2 py-2 text-center">
                        ${g.isWin ? `<span class="bg-green-100 text-green-800 text-[10px] uppercase px-2 py-1 rounded font-bold">Thắng</span>` : `<span class="bg-gray-100 text-gray-800 text-[10px] uppercase px-2 py-1 rounded font-bold">Thua</span>`}
                    </td>
                </tr>
            `;
        });
        html += `</tbody></table></div>`;
    }
    html += `</div></div>`;

    container.innerHTML = html;
};
"""

    content = content[:start_idx] + new_code + "\n" + content[end_idx:]
    with open("/app/applet/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully replaced calculateDashboardStats and renderDashboard")
else:
    print("Could not find start or end index.")
