import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace openEditPointModal
old_open_edit = r"""        function openEditPointModal\(idx\) \{.*?\n        \}"""
new_open_edit = """        window.openEditPointModal = function(idx) {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            const pt = game.danh_sach_diem[idx];
            
            window.ptEntryState = {
                isEdit: true,
                editIdx: idx,
                loai_diem: pt.loai_diem,
                tinh_chat: pt.chi_tiet_pha_bong ? pt.chi_tiet_pha_bong.tinh_chat : 'winner',
                nguoi_ket_thuc: pt.chi_tiet_pha_bong ? pt.chi_tiet_pha_bong.nguoi_ket_thuc : match.thong_tin.doi_thu_1,
                ky_thuat_ket_thuc: pt.chi_tiet_pha_bong ? pt.chi_tiet_pha_bong.ky_thuat_ket_thuc : '',
                nguoi_kien_tao: pt.chi_tiet_pha_bong ? pt.chi_tiet_pha_bong.nguoi_kien_tao : '',
                ky_thuat_kien_tao: pt.chi_tiet_pha_bong ? pt.chi_tiet_pha_bong.ky_thuat_kien_tao : '',
                dac_tinh: {
                    do_xoay: '',
                    diem_roi_ngang: '',
                    do_dai: '',
                    vi_tri_hong: ''
                }
            };
            
            if (pt.chi_tiet_pha_bong && pt.chi_tiet_pha_bong.dac_tinh) {
                window.ptEntryState.dac_tinh = { ...pt.chi_tiet_pha_bong.dac_tinh };
            }
            renderPtEntryForm();
        };"""
content = re.sub(old_open_edit, new_open_edit, content, flags=re.DOTALL)

# Delete handleEditPoint and updateEditPhuongThuc since they are not needed anymore
content = re.sub(r"""        function updateEditPhuongThuc\(loai_diem\) \{.*?\n        \}""", "", content, flags=re.DOTALL)
content = re.sub(r"""        async function handleEditPoint\(e, idx\) \{.*?\n        \}""", "", content, flags=re.DOTALL)


# Replace savePtEntry
old_save = r"""        window\.savePtEntry = async function\(\) \{.*?renderView\('gameTimeline'\);\n        \}"""
new_save = """        window.savePtEntry = async function() {
            const s = window.ptEntryState;
            if (!s.nguoi_ket_thuc) { showToast('Vui lòng chọn người kết thúc/đánh hỏng', 'error'); return; }
            if (!s.ky_thuat_ket_thuc) { showToast('Vui lòng chọn kỹ thuật', 'error'); return; }
            if (s.tinh_chat === 'forced_error') {
                if (!s.nguoi_kien_tao) { showToast('Vui lòng chọn người kiến tạo', 'error'); return; }
                if (!s.ky_thuat_kien_tao) { showToast('Vui lòng chọn kỹ thuật kiến tạo', 'error'); return; }
                if (!s.dac_tinh.vi_tri_hong) { showToast('Vui lòng chọn vị trí hỏng', 'error'); return; }
            }
            if (s.tinh_chat === 'unforced_error') {
                if (!s.dac_tinh.vi_tri_hong) { showToast('Vui lòng chọn vị trí hỏng', 'error'); return; }
            }
            
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            
            if (s.isEdit) {
                const pt = game.danh_sach_diem[s.editIdx];
                pt.loai_diem = s.loai_diem;
                pt.chi_tiet_pha_bong = {
                    tinh_chat: s.tinh_chat,
                    nguoi_ket_thuc: s.nguoi_ket_thuc,
                    ky_thuat_ket_thuc: s.ky_thuat_ket_thuc,
                    nguoi_kien_tao: s.nguoi_kien_tao,
                    ky_thuat_kien_tao: s.ky_thuat_kien_tao,
                    dac_tinh: {
                        diem_roi_ngang: s.dac_tinh.diem_roi_ngang,
                        do_dai: s.dac_tinh.do_dai,
                        do_xoay: s.dac_tinh.do_xoay,
                        vi_tri_hong: s.dac_tinh.vi_tri_hong
                    }
                };
                validatePoint(pt);
            } else {
                const state = calculateCurrentState(game.ty_so_bat_dau, game.danh_sach_diem);
                if(isGameFinished(state.p1, state.p2) && !confirm('Game đã đủ điều kiện kết thúc. Bạn có chắc chắn muốn nhập thêm điểm?')) return;
                
                const newPt = {
                    thu_tu_diem: game.danh_sach_diem.length + 1,
                    ty_so_hien_tai: '',
                    loai_diem: s.loai_diem,
                    nguoi_giao_bong: '',
                    chi_tiet_pha_bong: {
                        tinh_chat: s.tinh_chat,
                        nguoi_ket_thuc: s.nguoi_ket_thuc,
                        ky_thuat_ket_thuc: s.ky_thuat_ket_thuc,
                        nguoi_kien_tao: s.nguoi_kien_tao,
                        ky_thuat_kien_tao: s.ky_thuat_kien_tao,
                        dac_tinh: {
                            diem_roi_ngang: s.dac_tinh.diem_roi_ngang,
                            do_dai: s.dac_tinh.do_dai,
                            do_xoay: s.dac_tinh.do_xoay,
                            vi_tri_hong: s.dac_tinh.vi_tri_hong
                        }
                    }
                };
                validatePoint(newPt);
                game.danh_sach_diem.push(newPt);
            }
            
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            closeModal();
            renderView('gameTimeline');
        }"""
content = re.sub(old_save, new_save, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
