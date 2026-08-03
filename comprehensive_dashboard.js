window.renderDashboard = function(container) {
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
    
    // Build filter HTML
    let matchOpts = `<option value="all">Tất cả trận</option>`;
    appState.matches.forEach(m => matchOpts += `<option value="${m.id_tran_dau}" ${f.matchId===m.id_tran_dau?'selected':''}>${m.thong_tin.ngay_thi_dau}: ${m.thong_tin.doi_thu_1} vs ${m.thong_tin.doi_thu_2}</option>`);

    let typeOpts = `<option value="all">Tất cả</option>`;
    [...new Set(appState.matches.map(m=>m.thong_tin.loai_hinh))].forEach(t => typeOpts += `<option value="${t}" ${f.loai_hinh===t?'selected':''}>${t}</option>`);

    let oppOpts = `<option value="all">Tất cả</option>`;
    [...new Set(appState.matches.map(m=>m.thong_tin.doi_thu_2))].forEach(o => oppOpts += `<option value="${o}" ${f.doi_thu===o?'selected':''}>${o}</option>`);

    let html = `
        <div class="fixed top-14 left-0 right-0 z-10 bg-white border-b px-4 py-3 shadow-sm">
            <div class="max-w-3xl mx-auto flex gap-2 overflow-x-auto no-scrollbar items-center">
                <select id="dbFilterMatch" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[120px]">${matchOpts}</select>
                <input type="date" id="dbFilterFrom" onchange="updateDashboardFilter()" value="${f.fromDate}" class="border rounded p-1.5 text-xs bg-gray-50">
                <input type="date" id="dbFilterTo" onchange="updateDashboardFilter()" value="${f.toDate}" class="border rounded p-1.5 text-xs bg-gray-50">
                <select id="dbFilterType" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[90px]">${typeOpts}</select>
                <select id="dbFilterOpp" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[90px]">${oppOpts}</select>
            </div>
        </div>
        <div class="mt-32 px-4 max-w-3xl mx-auto space-y-6 pb-20">
    `;

    if (filteredMatches.length === 0) {
        html += `<div class="text-center py-10 text-gray-500">Không có dữ liệu phù hợp với bộ lọc.</div></div>`;
        container.innerHTML = html;
        return;
    }

    const s = calculateDashboardStats(filteredMatches);
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
                <h3 class="font-bold text-gray-800 border-b pb-2 mb-3">TÍNH CHẤT ĐIỂM (TÔI ĐÁNH)</h3>
                <div class="grid grid-cols-3 gap-2 text-center mb-4">
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Winner</div><div class="font-black text-green-600 text-2xl">${s.winnerByMe}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Forced Error</div><div class="font-black text-blue-600 text-2xl">${s.forcedErrorByMe}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Unforced Error</div><div class="font-black text-red-600 text-2xl">${s.unforcedErrorByMe}</div></div>
                </div>
            </div>
        </div>
    `;

    // --- NHÓM 5: TACTICAL ANALYTICS ---
    html += `<div><h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">2. Tactical Analytics</h2>`;
    
    // Winner Analysis
    const topWinner = Object.keys(s.technique).sort((a,b)=>s.technique[b].winnerByMe - s.technique[a].winnerByMe).filter(k => s.technique[k].winnerByMe > 0);
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">WINNER ANALYSIS (Theo kỹ thuật)</h3>`;
    if(topWinner.length>0) {
        topWinner.forEach(k => {
            html += `<div class="flex justify-between items-center py-2 border-b last:border-0 text-sm"><span>${getName(k)}</span><span class="font-bold text-green-600">${s.technique[k].winnerByMe}</span></div>`;
        });
    } else {
        html += `<div class="text-sm text-gray-500">Chưa có dữ liệu Winner.</div>`;
    }
    html += `</div>`;

    // Forced Error
    const topAssist = Object.keys(s.assistTech).sort((a,b)=>s.assistTech[b].forcedErrorOpponent - s.assistTech[a].forcedErrorOpponent).filter(k => s.assistTech[k].forcedErrorOpponent > 0);
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">FORCED ERROR (Kiến tạo ép lỗi)</h3>`;
    if(topAssist.length>0) {
        topAssist.forEach(k => {
            html += `<div class="flex justify-between items-center py-2 border-b last:border-0 text-sm"><span>${getName(k)}</span><span class="font-bold text-blue-600">${s.assistTech[k].forcedErrorOpponent}</span></div>`;
        });
    } else {
        html += `<div class="text-sm text-gray-500">Chưa có dữ liệu ép lỗi.</div>`;
    }
    html += `</div>`;

    // Unforced Error
    const topUnforced = Object.keys(s.technique).sort((a,b)=>s.technique[b].unforcedErrorByMe - s.technique[a].unforcedErrorByMe).filter(k => s.technique[k].unforcedErrorByMe > 0);
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">UNFORCED ERROR (Theo kỹ thuật)</h3>`;
    if(topUnforced.length>0) {
        topUnforced.forEach(k => {
            html += `<div class="flex justify-between items-center py-2 border-b last:border-0 text-sm"><span>${getName(k)}</span><span class="font-bold text-red-600">${s.technique[k].unforcedErrorByMe}</span></div>`;
        });
    } else {
        html += `<div class="text-sm text-gray-500">Chưa có dữ liệu tự hỏng.</div>`;
    }
    html += `</div>`;

    // Heatmap
    const rHeatmap = (data, title, colClass) => {
        const total = Object.values(data).reduce((a,b)=>a+b,0) || 1;
        const cell = (k) => {
            const c = data[k]||0; const pct = Math.round(c/total*100);
            return `<div class="border p-2 flex flex-col items-center justify-center h-20 ${c>0?colClass:'bg-gray-50'} relative"><div class="absolute inset-0 bg-current opacity-${Math.min(pct*2, 100)}"></div><span class="relative z-10 font-bold text-lg">${c}</span><span class="relative z-10 text-[10px] font-semibold">${pct}%</span></div>`;
        };
        return `
            <div class="flex-1">
                <div class="text-xs font-bold text-center mb-2 uppercase text-gray-600">${title}</div>
                <div class="grid grid-cols-3 gap-0.5 border bg-gray-200">
                    ${cell('dai_trai')}${cell('dai_giua')}${cell('dai_phai')}
                    ${cell('ngan_trai')}${cell('ngan_giua')}${cell('ngan_phai')}
                </div>
                <div class="flex justify-between text-[10px] text-gray-500 mt-1 px-1"><span>Trái</span><span>Giữa</span><span>Phải</span></div>
            </div>
        `;
    };
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-4">ĐIỂM RƠI (HEATMAP)</h3><div class="flex gap-4">${rHeatmap(s.heatmapWinner, 'GHI ĐIỂM (WINNER)', 'bg-blue-200 text-blue-900')}${rHeatmap(s.heatmapLost, 'MẤT ĐIỂM (LỖI)', 'bg-red-200 text-red-900')}</div></div>`;

    // Spin
    const totalSpins = Object.values(s.spin).reduce((acc, val) => acc + val.total, 0);
    if (totalSpins > 0) {
        html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">PHÂN TÍCH ĐỘ XOÁY</h3><div class="space-y-4">`;
        Object.keys(s.spin).forEach(k => {
            const obj = s.spin[k];
            if (obj.total === 0) return;
            const titleName = appState.dict.thuoc_tinh_bong.do_xoay[k];
            html += `
                <div>
                    <div class="flex justify-between font-bold text-sm mb-1"><span>${titleName} (${obj.total})</span></div>
                    <div class="flex gap-4 text-xs">
                        <div class="flex-1 bg-gray-50 rounded p-2 border"><div class="text-gray-500 mb-1">Tỷ lệ thắng</div><div class="font-black text-green-600">${toPct(obj.win, obj.total)}%</div></div>
                        <div class="flex-1 bg-gray-50 rounded p-2 border"><div class="text-gray-500 mb-1">Tỷ lệ ép lỗi</div><div class="font-black text-blue-600">${toPct(obj.forcedError, obj.total)}%</div></div>
                    </div>
                </div>
            `;
        });
        html += `</div></div>`;
    }

    // Error Location
    const errTotals = Object.values(s.errorLocation).reduce((a,b)=>a+b,0);
    if(errTotals > 0) {
        html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">VỊ TRÍ HỎNG BÓNG</h3><div class="space-y-3">`;
        Object.keys(s.errorLocation).forEach(k => {
            const c = s.errorLocation[k];
            if (c === 0) return;
            html += `<div><div class="flex justify-between text-xs mb-1"><span>${appState.dict.thuoc_tinh_loi.vi_tri_hong[k]}</span><span class="font-bold">${c} (${toPct(c, errTotals)}%)</span></div>${bar(toPct(c, errTotals), 'bg-orange-500')}</div>`;
        });
        html += `</div></div>`;
    }
    
    // Technique Ranking (Top 10)
    const allTechKeys = Object.keys(s.technique);
    if (allTechKeys.length > 0) {
        html += `
            <div class="bg-white rounded-xl shadow-sm border p-4 mb-4 overflow-x-auto">
                <h3 class="font-bold text-gray-800 border-b pb-2 mb-3">BẢNG XẾP HẠNG KỸ THUẬT (TOP 10)</h3>
                <table class="w-full text-xs text-left whitespace-nowrap">
                    <thead class="text-gray-500 bg-gray-50 uppercase border-b">
                        <tr>
                            <th class="px-2 py-2">Kỹ thuật</th>
                            <th class="px-2 py-2 text-center text-green-600">Winner</th>
                            <th class="px-2 py-2 text-center text-red-600">Unforced</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        const rankedTechs = allTechKeys.sort((a,b) => (s.technique[b].winnerByMe) - (s.technique[a].winnerByMe)).slice(0, 10);
        rankedTechs.forEach(k => {
            html += `
                <tr class="border-b last:border-0">
                    <td class="px-2 py-2 font-bold">${getName(k)}</td>
                    <td class="px-2 py-2 text-center font-bold text-green-600">${s.technique[k].winnerByMe}</td>
                    <td class="px-2 py-2 text-center font-bold text-red-600">${s.technique[k].unforcedErrorByMe}</td>
                </tr>
            `;
        });
        html += `</tbody></table></div>`;
    }

    html += `</div>`; // End Tactical Analytics

    // --- NHÓM 3: MOMENTUM ---
    html += `
        <div>
            <h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">3. Momentum (Chuỗi điểm)</h2>
            <div class="bg-white rounded-xl shadow-sm border p-4 mb-4">
                <div class="grid grid-cols-3 gap-2 text-center">
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Chuỗi Thắng</div><div class="font-black text-green-600 text-2xl">${s.maxWinStreak}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Chuỗi Ép lỗi</div><div class="font-black text-blue-600 text-2xl">${s.maxForcedStreak}</div></div>
                    <div><div class="text-[10px] uppercase text-gray-500 font-bold">Chuỗi Tự hỏng</div><div class="font-black text-red-600 text-2xl">${s.maxUnforcedStreak}</div></div>
                </div>
            </div>
        </div>
    `;

    // --- NHÓM 4: GAME SUMMARY ---
    if (s.gameSummary.length > 0) {
        html += `
            <div>
                <h2 class="text-xl font-black text-gray-800 border-b-2 border-gray-800 pb-2 mb-4 uppercase mt-8">4. Game Summary</h2>
                <div class="bg-white rounded-xl shadow-sm border p-4 overflow-x-auto">
                    <table class="w-full text-xs text-left whitespace-nowrap">
                        <thead class="text-gray-500 bg-gray-50 uppercase border-b">
                            <tr>
                                <th class="px-2 py-2">Game</th>
                                <th class="px-2 py-2 text-center">Pha bóng</th>
                                <th class="px-2 py-2 text-center text-green-600">Winner</th>
                                <th class="px-2 py-2 text-center text-blue-600">Forced</th>
                                <th class="px-2 py-2 text-center text-red-600">Unforced</th>
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
        html += `</tbody></table></div></div>`;
    }

    html += `</div>`;
    container.innerHTML = html;
};
