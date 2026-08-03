import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

migration_code = """
        // --- DATA MIGRATION & VALIDATION ---
        function normalizePoint(pt, m) {
            if (pt.chi_tiet_pha_bong) return pt;
            const isWin = pt.loai_diem === 'thang';
            const me = m.thong_tin.doi_thu_1 || 'Hungpv';
            const opp = m.thong_tin.doi_thu_2 || 'Doi_thu';

            let tinh_chat = isWin ? 'winner' : 'unforced_error';
            let nguoi_ket_thuc = isWin ? me : me; // default
            let ky_thuat_ket_thuc = pt.ky_thuat || null;

            if (pt.phuong_thuc === 'toi_ghi_diem') {
                tinh_chat = 'winner';
                nguoi_ket_thuc = me;
            } else if (pt.phuong_thuc === 'doi_thu_danh_hong') {
                tinh_chat = 'unforced_error';
                nguoi_ket_thuc = opp;
            } else if (pt.phuong_thuc === 'toi_danh_hong') {
                tinh_chat = 'unforced_error';
                nguoi_ket_thuc = me;
            } else if (pt.phuong_thuc === 'doi_thu_ghi_diem') {
                tinh_chat = 'winner';
                nguoi_ket_thuc = opp;
            }

            pt.chi_tiet_pha_bong = {
                tinh_chat: tinh_chat,
                nguoi_ket_thuc: nguoi_ket_thuc,
                ky_thuat_ket_thuc: ky_thuat_ket_thuc,
                nguoi_kien_tao: null,
                ky_thuat_kien_tao: null,
                dac_tinh: {
                    diem_roi_ngang: null,
                    do_dai: null,
                    do_xoay: null,
                    vi_tri_hong: null
                }
            };

            delete pt.nhom;
            delete pt.ky_thuat;
            delete pt.phuong_thuc;
            return pt;
        }

        function normalizeGame(g, m) {
            if (!g.danh_sach_diem) return g;
            g.danh_sach_diem.forEach(pt => normalizePoint(pt, m));
            return g;
        }

        function normalizeMatch(m) {
            if (!m.chi_tiet_game) return m;
            m.chi_tiet_game.forEach(g => normalizeGame(g, m));
            return m;
        }

        function migrateOldSchema() {
            if (!appState.matches) return;
            appState.matches.forEach(m => normalizeMatch(m));
        }

        function validatePoint(pt) {
            const chi_tiet = pt.chi_tiet_pha_bong;
            if (!chi_tiet) return;
            
            // Validate unused properties are null
            if (chi_tiet.tinh_chat === 'winner') {
                if(chi_tiet.dac_tinh) chi_tiet.dac_tinh.vi_tri_hong = null;
            }
            if (chi_tiet.tinh_chat === 'forced_error' && !chi_tiet.nguoi_kien_tao) {
                // Must have nguoi_kien_tao
                chi_tiet.nguoi_kien_tao = "Unknown";
            }
            if (chi_tiet.tinh_chat === 'unforced_error') {
                chi_tiet.nguoi_kien_tao = null;
                chi_tiet.ky_thuat_kien_tao = null;
            }
        }
"""

appState_str = """        const appState = {
            view: 'list', // list, matchForm, matchDetail, gameTimeline, dashboard, settings
            matches: [],
            dict: null,
            isMock: true,
            currentMatchId: null,
            currentGameIndex: null,
            github: { user: '', repo: '', branch: 'main', dataPath: 'dulieubongban.json', dictPath: 'tu_dien_bong_ban.json', token: '', sha: null, dictSha: null },
            isLoading: false
        };"""

content = content.replace(appState_str, appState_str + "\n" + migration_code)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
