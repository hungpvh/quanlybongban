function calculateDashboardStats(filteredMatches) {
    const s = {
        matches: { total: 0, win: 0 },
        games: { total: 0, win: 0 },
        points: { total: 0, win: 0 },
        
        winnerByMe: 0, forcedErrorByMe: 0, unforcedErrorByMe: 0,
        winnerByOpp: 0, forcedErrorByOpp: 0, unforcedErrorByOpp: 0,
        
        technique: {}, 
        assistTech: {},
        
        serve: { total: 0, win: 0 },
        receive: { total: 0, win: 0 },
        serveType: {},
        
        maxWinStreak: 0, maxForcedStreak: 0, maxUnforcedStreak: 0,
        
        gameSummary: [], 
        
        heatmapWinner: { ngan_trai: 0, ngan_giua: 0, ngan_phai: 0, dai_trai: 0, dai_giua: 0, dai_phai: 0 },
        heatmapLost: { ngan_trai: 0, ngan_giua: 0, ngan_phai: 0, dai_trai: 0, dai_giua: 0, dai_phai: 0 },
        spin: { xuong: { total: 0, win: 0, forcedError: 0 }, len: { total: 0, win: 0, forcedError: 0 }, long: { total: 0, win: 0, forcedError: 0 } },
        errorLocation: { ruc_luoi: 0, ra_ngoai_dai: 0, ra_ngoai_bien: 0, truot_bong: 0 }
    };

    filteredMatches.forEach(m => {
        s.matches.total++;
        let mWins = 0, mLoses = 0;
        const me = m.thong_tin.doi_thu_1;

        if (m.chi_tiet_game) m.chi_tiet_game.forEach((g, gIndex) => {
            s.games.total++;
            let gWins = 0, gLoses = 0;
            let currentWinStreak = 0;
            let currentForcedStreak = 0;
            let currentUnforcedStreak = 0;
            
            let gWinnerMe = 0, gForcedMe = 0, gUnforcedMe = 0;

            if (g.danh_sach_diem) g.danh_sach_diem.forEach(pt => {
                const c = pt.chi_tiet_pha_bong;
                if (!c) return;
                
                s.points.total++;
                const isWin = pt.loai_diem === 'thang';
                if (isWin) { s.points.win++; gWins++; } else { gLoses++; }

                // Serve
                if (pt.nguoi_giao_bong === me) {
                    s.serve.total++;
                    if (isWin) s.serve.win++;
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
                if (isWin) {
                    if (c.tinh_chat === 'winner') { s.winnerByMe++; gWinnerMe++; }
                    if (c.tinh_chat === 'forced_error') { s.forcedErrorByMe++; gForcedMe++; }
                    if (c.tinh_chat === 'unforced_error') s.unforcedErrorByOpp++;
                } else {
                    if (c.tinh_chat === 'winner') s.winnerByOpp++;
                    if (c.tinh_chat === 'forced_error') s.forcedErrorByOpp++;
                    if (c.tinh_chat === 'unforced_error') { s.unforcedErrorByMe++; gUnforcedMe++; }
                }

                // Tech & Assist
                const techFinish = c.ky_thuat_ket_thuc;
                const techAssist = c.ky_thuat_kien_tao;
                
                if (techFinish && c.nguoi_ket_thuc === me) {
                    if (!s.technique[techFinish]) s.technique[techFinish] = { total: 0, winnerByMe: 0, forcedErrorByMe: 0, unforcedErrorByMe: 0 };
                    s.technique[techFinish].total++;
                    if (c.tinh_chat === 'winner') s.technique[techFinish].winnerByMe++;
                    if (c.tinh_chat === 'unforced_error') s.technique[techFinish].unforcedErrorByMe++;
                    if (c.tinh_chat === 'forced_error' && c.nguoi_ket_thuc === me) {
                        // Actually if I hit a forced error, it means I made the error. So forcedErrorByMe?
                        // "forcedErrorByMe" usually means I FORCED the opponent into an error. 
                        // If I made a forced error, it's forced error against me.
                        // I will track my own errors separately if needed, but let's keep it simple: unforced is what matters for negative stats.
                    }
                }
                
                if (techAssist && c.nguoi_kien_tao === me) {
                    if (!s.assistTech[techAssist]) s.assistTech[techAssist] = { totalAssist: 0, forcedErrorOpponent: 0, winner: 0 };
                    s.assistTech[techAssist].totalAssist++;
                    if (c.tinh_chat === 'forced_error') s.assistTech[techAssist].forcedErrorOpponent++;
                    if (c.tinh_chat === 'winner') s.assistTech[techAssist].winner++;
                }
                
                // Serve Type
                if (pt.nguoi_giao_bong === me && (c.tinh_chat === 'winner' || c.tinh_chat === 'unforced_error' || c.tinh_chat === 'forced_error')) {
                    // Wait, we don't always know the serve type of EVERY point unless it's logged as the ending/assist tech.
                    // But if it's logged as a serve, we can track it.
                    if (appState.dict.loai_giao_bong[techFinish]) {
                        if (!s.serveType[techFinish]) s.serveType[techFinish] = { total: 0, win: 0 };
                        s.serveType[techFinish].total++;
                        if (isWin) s.serveType[techFinish].win++;
                    }
                }

                // Heatmap & Spin
                const dac_tinh = c.dac_tinh;
                if (dac_tinh) {
                    if (dac_tinh.diem_roi_ngang && dac_tinh.do_dai) {
                        const key = `${dac_tinh.do_dai}_${dac_tinh.diem_roi_ngang}`;
                        if (isWin) s.heatmapWinner[key] = (s.heatmapWinner[key] || 0) + 1;
                        else s.heatmapLost[key] = (s.heatmapLost[key] || 0) + 1;
                    }
                    if (dac_tinh.do_xoay && s.spin[dac_tinh.do_xoay]) {
                        s.spin[dac_tinh.do_xoay].total++;
                        if (isWin) s.spin[dac_tinh.do_xoay].win++;
                        if (isWin && c.tinh_chat === 'forced_error') s.spin[dac_tinh.do_xoay].forcedError++;
                    }
                    if (dac_tinh.vi_tri_hong && c.nguoi_ket_thuc === me) {
                        if (s.errorLocation[dac_tinh.vi_tri_hong] !== undefined) {
                            s.errorLocation[dac_tinh.vi_tri_hong]++;
                        }
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

        if (mWins > mLoses) s.matches.win++;
    });

    return s;
}
