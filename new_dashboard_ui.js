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

            // NHÓM 1 & TACTICAL SUMMARY
            html += `
                <div class="grid grid-cols-2 gap-3">
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
            `;
            
            // CHI TIẾT ĐIỂM
            html += `
                <div class="bg-white rounded-xl shadow-sm border p-4">
                    <h3 class="font-bold text-gray-800 border-b pb-2 mb-3">TÍNH CHẤT ĐIỂM</h3>
                    <div class="grid grid-cols-3 gap-2 text-center mb-4">
                        <div><div class="text-xs text-gray-500">Winner</div><div class="font-bold text-green-600 text-xl">${s.winnerByMe}</div></div>
                        <div><div class="text-xs text-gray-500">Forced Error (Ép)</div><div class="font-bold text-blue-600 text-xl">${s.forcedErrorByMe}</div></div>
                        <div><div class="text-xs text-gray-500">Unforced Error</div><div class="font-bold text-red-600 text-xl">${s.unforcedErrorByMe}</div></div>
                    </div>
                    <div class="space-y-3">
                        <div>
                            <div class="flex justify-between text-xs font-bold"><span>Điểm ghi được (Winner + Ép)</span><span>${toPct(s.winnerByMe + s.forcedErrorByMe, s.points.win)}%</span></div>
                            ${bar(toPct(s.winnerByMe + s.forcedErrorByMe, s.points.win), 'bg-green-500')}
                        </div>
                        <div>
                            <div class="flex justify-between text-xs font-bold"><span>Điểm mất do tự hỏng (Unforced)</span><span>${toPct(s.unforcedErrorByMe, s.points.total - s.points.win)}%</span></div>
                            ${bar(toPct(s.unforcedErrorByMe, s.points.total - s.points.win), 'bg-red-500')}
                        </div>
                    </div>
                </div>
            `;

            // TOP KỸ THUẬT WINNER
            const topWinner = Object.keys(s.technique).sort((a,b)=>s.technique[b].winnerByMe - s.technique[a].winnerByMe).slice(0,3);
            if(topWinner.length > 0 && s.technique[topWinner[0]].winnerByMe > 0) {
                html += `<div class="bg-white rounded-xl shadow-sm border p-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">KỸ THUẬT WINNER NHIỀU NHẤT</h3>`;
                topWinner.forEach(k => {
                    if (s.technique[k].winnerByMe === 0) return;
                    html += `<div class="flex justify-between items-center py-1 text-sm border-b last:border-0"><span>${appState.dict.ky_thuat_rally[k]||appState.dict.loai_giao_bong[k]||k}</span><span class="font-bold text-green-600">${s.technique[k].winnerByMe}</span></div>`;
                });
                html += `</div>`;
            }

            // TOP KỸ THUẬT KIẾN TẠO (ÉP LỖI)
            const topAssist = Object.keys(s.assistTech).sort((a,b)=>s.assistTech[b].forcedErrorOpponent - s.assistTech[a].forcedErrorOpponent).slice(0,3);
            if(topAssist.length > 0 && s.assistTech[topAssist[0]].forcedErrorOpponent > 0) {
                html += `<div class="bg-white rounded-xl shadow-sm border p-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">KỸ THUẬT ÉP LỖI (FORCED ERROR)</h3>`;
                topAssist.forEach(k => {
                    if (s.assistTech[k].forcedErrorOpponent === 0) return;
                    html += `<div class="flex justify-between items-center py-1 text-sm border-b last:border-0"><span>${appState.dict.ky_thuat_rally[k]||appState.dict.loai_giao_bong[k]||k}</span><span class="font-bold text-blue-600">${s.assistTech[k].forcedErrorOpponent}</span></div>`;
                });
                html += `</div>`;
            }

            // UNFORCED ERROR
            const topUnforced = Object.keys(s.technique).sort((a,b)=>s.technique[b].unforcedErrorByMe - s.technique[a].unforcedErrorByMe).slice(0,3);
            if(topUnforced.length > 0 && s.technique[topUnforced[0]].unforcedErrorByMe > 0) {
                html += `<div class="bg-white rounded-xl shadow-sm border p-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">KỸ THUẬT MẮC LỖI NHIỀU NHẤT</h3>`;
                topUnforced.forEach(k => {
                    if (s.technique[k].unforcedErrorByMe === 0) return;
                    html += `<div class="flex justify-between items-center py-1 text-sm border-b last:border-0"><span>${appState.dict.ky_thuat_rally[k]||appState.dict.loai_giao_bong[k]||k}</span><span class="font-bold text-red-600">${s.technique[k].unforcedErrorByMe}</span></div>`;
                });
                html += `</div>`;
            }

            // HEATMAP WINNER / LOST
            const rHeatmap = (data, title) => {
                const total = Object.values(data).reduce((a,b)=>a+b,0) || 1;
                const cell = (k) => {
                    const c = data[k]||0; const pct = Math.round(c/total*100);
                    return `<div class="border p-2 flex flex-col items-center justify-center h-16 ${c>0?'bg-blue-100':'bg-gray-50'} relative"><div class="absolute inset-0 bg-blue-500 opacity-${Math.min(pct*2, 100)}"></div><span class="relative z-10 font-bold">${c}</span><span class="relative z-10 text-[10px] text-gray-600">${pct}%</span></div>`;
                };
                return `
                    <div class="flex-1">
                        <div class="text-xs font-bold text-center mb-1">${title}</div>
                        <div class="grid grid-cols-3">
                            ${cell('dai_trai')}${cell('dai_giua')}${cell('dai_phai')}
                            ${cell('ngan_trai')}${cell('ngan_giua')}${cell('ngan_phai')}
                        </div>
                    </div>
                `;
            };
            html += `<div class="bg-white rounded-xl shadow-sm border p-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">ĐIỂM RƠI (HEATMAP)</h3><div class="flex gap-4">${rHeatmap(s.heatmapWinner, 'GHI ĐIỂM')}${rHeatmap(s.heatmapLost, 'MẤT ĐIỂM')}</div></div>`;

            // ERROR LOCATION
            const errTotals = Object.values(s.errorLocation).reduce((a,b)=>a+b,0);
            if(errTotals > 0) {
                html += `<div class="bg-white rounded-xl shadow-sm border p-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">VỊ TRÍ HỎNG BÓNG</h3><div class="space-y-2">`;
                Object.keys(s.errorLocation).forEach(k => {
                    const c = s.errorLocation[k];
                    if (c === 0) return;
                    html += `<div><div class="flex justify-between text-xs"><span>${appState.dict.thuoc_tinh_loi.vi_tri_hong[k]}</span><span class="font-bold">${c} (${toPct(c, errTotals)}%)</span></div>${bar(toPct(c, errTotals), 'bg-orange-500')}</div>`;
                });
                html += `</div></div>`;
            }
            
            // SPIN
            const totalSpins = Object.values(s.spin).reduce((acc, val) => acc + val.total, 0);
            if (totalSpins > 0) {
                html += `<div class="bg-white rounded-xl shadow-sm border p-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">ĐỘ XOÁY</h3><div class="space-y-3">`;
                Object.keys(s.spin).forEach(k => {
                    const obj = s.spin[k];
                    if (obj.total === 0) return;
                    html += `<div><div class="flex justify-between text-xs"><span>${appState.dict.thuoc_tinh_bong.do_xoay[k]}</span><span class="font-bold">${obj.total} lần (Tỉ lệ thắng: ${toPct(obj.win, obj.total)}%)</span></div>${bar(toPct(obj.win, obj.total), 'bg-indigo-500')}</div>`;
                });
                html += `</div></div>`;
            }

            // MOMENTUM (STREAKS)
            html += `
                <div class="bg-white rounded-xl shadow-sm border p-4">
                    <h3 class="font-bold text-gray-800 border-b pb-2 mb-3">CHUỖI ĐIỂM (MOMENTUM)</h3>
                    <div class="grid grid-cols-3 gap-2 text-center">
                        <div><div class="text-xs text-gray-500">Win Streak</div><div class="font-bold text-green-600 text-xl">${s.maxWinStreak}</div></div>
                        <div><div class="text-xs text-gray-500">Forced Streak</div><div class="font-bold text-blue-600 text-xl">${s.maxForcedStreak}</div></div>
                        <div><div class="text-xs text-gray-500">Unforced Streak</div><div class="font-bold text-red-600 text-xl">${s.maxUnforcedStreak}</div></div>
                    </div>
                </div>
            `;

            // GAME SUMMARY TABLE
            if (s.gameSummary.length > 0) {
                html += `
                    <div class="bg-white rounded-xl shadow-sm border p-4 overflow-x-auto">
                        <h3 class="font-bold text-gray-800 border-b pb-2 mb-3">GAME SUMMARY</h3>
                        <table class="w-full text-sm text-left whitespace-nowrap">
                            <thead class="text-xs text-gray-500 bg-gray-50 uppercase border-b">
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
                                ${g.isWin ? `<span class="bg-green-100 text-green-800 text-xs px-2 py-0.5 rounded font-bold">Thắng</span>` : `<span class="bg-gray-100 text-gray-800 text-xs px-2 py-0.5 rounded font-bold">Thua</span>`}
                            </td>
                        </tr>
                    `;
                });
                html += `</tbody></table></div>`;
            }

            html += `</div>`;
            container.innerHTML = html;
        };

        window.updateDashboardFilter = function() {
            if(!appState.dashboardFilter) return;
            appState.dashboardFilter.matchId = document.getElementById('dbFilterMatch').value;
            appState.dashboardFilter.fromDate = document.getElementById('dbFilterFrom').value;
            appState.dashboardFilter.toDate = document.getElementById('dbFilterTo').value;
            appState.dashboardFilter.loai_hinh = document.getElementById('dbFilterType').value;
            appState.dashboardFilter.doi_thu = document.getElementById('dbFilterOpp').value;
            renderView('dashboard');
        };
