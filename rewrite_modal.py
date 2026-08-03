import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to replace
pattern = r"        function openPointModal\(loai_diem\) \{.*?\}\s*function openEditPointModal\(idx\) \{"

new_code = """        window.openPointModal = function(loai_diem) {
            window.ptEntryState = {
                loai_diem: loai_diem,
                tinh_chat: null,
                nguoi_ket_thuc: null,
                ky_thuat_ket_thuc: null,
                nguoi_kien_tao: null,
                ky_thuat_kien_tao: null,
                dac_tinh: {
                    diem_roi_ngang: null,
                    do_dai: null,
                    do_xoay: null,
                    vi_tri_hong: null
                }
            };
            
            const title = loai_diem === 'thang' ? 'ĐIỂM THẮNG CỦA TÔI' : 'ĐIỂM THUA CỦA TÔI';
            const colorClass = loai_diem === 'thang' ? 'text-blue-600' : 'text-red-600';
            
            showModal(`
                <h3 class="font-black text-xl mb-6 text-center ${colorClass}">${title}</h3>
                <p class="text-sm font-bold text-gray-500 mb-2 text-center">TÍNH CHẤT PHA BÓNG</p>
                <div class="grid grid-cols-1 gap-3">
                    <button onclick="selectTinhChat('winner')" class="bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold p-4 rounded-xl border border-blue-200 shadow-sm flex flex-col items-center justify-center gap-1 transition"><i class="fas fa-bolt text-2xl"></i> Điểm trực tiếp (Winner)</button>
                    <button onclick="selectTinhChat('forced_error')" class="bg-orange-50 hover:bg-orange-100 text-orange-700 font-bold p-4 rounded-xl border border-orange-200 shadow-sm flex flex-col items-center justify-center gap-1 transition"><i class="fas fa-compress-arrows-alt text-2xl"></i> Bị ép đánh hỏng (Forced Error)</button>
                    <button onclick="selectTinhChat('unforced_error')" class="bg-red-50 hover:bg-red-100 text-red-700 font-bold p-4 rounded-xl border border-red-200 shadow-sm flex flex-col items-center justify-center gap-1 transition"><i class="fas fa-times-circle text-2xl"></i> Tự đánh hỏng (Unforced Error)</button>
                </div>
                <button onclick="closeModal()" class="w-full mt-6 p-4 bg-gray-200 text-gray-800 rounded-xl font-bold shadow-sm">HỦY BỎ</button>
            `);
        }

        window.selectTinhChat = function(val) {
            window.ptEntryState.tinh_chat = val;
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const me = match.thong_tin.doi_thu_1 || 'Tôi';
            const opp = match.thong_tin.doi_thu_2 || 'Đối thủ';

            if (val === 'winner') {
                window.ptEntryState.nguoi_ket_thuc = (window.ptEntryState.loai_diem === 'thang') ? me : opp;
            } else if (val === 'unforced_error') {
                window.ptEntryState.nguoi_ket_thuc = (window.ptEntryState.loai_diem === 'thua') ? me : opp;
            } else if (val === 'forced_error') {
                window.ptEntryState.nguoi_ket_thuc = (window.ptEntryState.loai_diem === 'thua') ? me : opp;
                window.ptEntryState.nguoi_kien_tao = (window.ptEntryState.loai_diem === 'thua') ? opp : me;
            }

            renderPtEntryForm();
        }

        window.renderPtEntryForm = function() {
            const s = window.ptEntryState;
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const me = match.thong_tin.doi_thu_1 || 'Tôi';
            const opp = match.thong_tin.doi_thu_2 || 'Đối thủ';
            const serveKeys = Object.keys(appState.dict.loai_giao_bong);
            const techKeys = Object.keys(appState.dict.ky_thuat_rally);
            const hongKeys = Object.keys(appState.dict.thuoc_tinh_loi.vi_tri_hong);

            const renderPlayerSelect = (label, key) => `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">${label}</label>
                    <div class="flex gap-2">
                        <button onclick="updatePtState('${key}', '${me}')" class="flex-1 p-3 rounded-xl font-bold border transition ${s[key]===me?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${me}</button>
                        <button onclick="updatePtState('${key}', '${opp}')" class="flex-1 p-3 rounded-xl font-bold border transition ${s[key]===opp?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${opp}</button>
                    </div>
                </div>
            `;

            const renderTechSelect = (label, key) => `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">${label}</label>
                    <div class="grid grid-cols-2 gap-2 mb-2">
                        ${serveKeys.map(k => `<button onclick="updatePtState('${key}', '${k}')" class="p-3 rounded-xl font-semibold text-xs border transition ${s[key]===k?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${appState.dict.loai_giao_bong[k]}</button>`).join('')}
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        ${techKeys.map(k => `<button onclick="updatePtState('${key}', '${k}')" class="p-2 rounded-xl font-semibold text-xs border transition ${s[key]===k?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${appState.dict.ky_thuat_rally[k]}</button>`).join('')}
                    </div>
                </div>
            `;

            const renderDiemRoi = () => `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Điểm rơi & Độ dài</label>
                    <div class="grid grid-cols-3 gap-2">
                        ${['trai', 'giua', 'phai'].map(col => `
                            <div class="flex flex-col gap-2">
                                <button onclick="updateDiemRoi('${col}', 'ngan')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='ngan')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Ngắn<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                                <button onclick="updateDiemRoi('${col}', 'dai')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='dai')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Dài<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;

            const renderDoXoay = () => `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Độ xoáy</label>
                    <div class="flex bg-gray-100 p-1 rounded-xl">
                        ${['xuong', 'long', 'len'].map(x => `
                            <button onclick="updatePtStateDacTinh('do_xoay', '${x}')" class="flex-1 py-3 rounded-lg font-bold text-sm transition ${s.dac_tinh.do_xoay===x?'bg-white text-blue-700 shadow-sm':'text-gray-500 hover:text-gray-700'}">${appState.dict.thuoc_tinh_bong.do_xoay[x]}</button>
                        `).join('')}
                    </div>
                </div>
            `;

            const renderViTriHong = () => `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Vị trí hỏng</label>
                    <div class="grid grid-cols-2 gap-2">
                        ${hongKeys.map(k => `
                            <button onclick="updatePtStateDacTinh('vi_tri_hong', '${k}')" class="p-4 rounded-xl font-bold text-sm border transition ${s.dac_tinh.vi_tri_hong===k?'bg-red-600 text-white border-red-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">${appState.dict.thuoc_tinh_loi.vi_tri_hong[k]}</button>
                        `).join('')}
                    </div>
                </div>
            `;

            let html = `<div class="max-h-[70vh] overflow-y-auto no-scrollbar pb-6 px-1">
                <div class="flex items-center justify-between mb-4 pb-2 border-b sticky top-0 bg-white z-10 pt-2">
                    <h3 class="font-black text-lg text-gray-800">${s.tinh_chat === 'winner' ? 'Điểm trực tiếp' : s.tinh_chat === 'forced_error' ? 'Bị ép đánh hỏng' : 'Tự đánh hỏng'}</h3>
                    <button onclick="openPointModal('${s.loai_diem}')" class="text-sm text-gray-500 hover:text-gray-800 font-bold bg-gray-100 px-3 py-1.5 rounded-full"><i class="fas fa-undo mr-1"></i>Đổi</button>
                </div>
            `;

            if (s.tinh_chat === 'winner') {
                html += renderPlayerSelect("Người ghi điểm (Kết thúc)", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật kết thúc", "ky_thuat_ket_thuc");
                html += renderDiemRoi();
                html += renderDoXoay();
            } else if (s.tinh_chat === 'forced_error') {
                html += renderPlayerSelect("Người kiến tạo (Ép)", "nguoi_kien_tao");
                html += renderTechSelect("Kỹ thuật kiến tạo", "ky_thuat_kien_tao");
                html += renderPlayerSelect("Người đánh hỏng", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật đánh hỏng", "ky_thuat_ket_thuc");
                html += renderViTriHong();
            } else if (s.tinh_chat === 'unforced_error') {
                html += renderPlayerSelect("Người đánh hỏng", "nguoi_ket_thuc");
                html += renderTechSelect("Kỹ thuật đánh hỏng", "ky_thuat_ket_thuc");
                html += renderViTriHong();
            }

            html += `
                </div>
                <div class="mt-4 pt-4 border-t flex gap-3 bg-white">
                    <button onclick="closeModal()" class="flex-1 bg-gray-200 text-gray-800 font-bold py-4 rounded-xl">HỦY</button>
                    <button onclick="savePtEntry()" class="flex-[2] bg-blue-600 text-white font-bold py-4 rounded-xl shadow-md uppercase"><i class="fas fa-save mr-2"></i>Lưu điểm</button>
                </div>
            `;
            
            showModal(html);
        }

        window.updatePtState = function(key, val) {
            window.ptEntryState[key] = val;
            renderPtEntryForm();
        };
        window.updatePtStateDacTinh = function(key, val) {
            window.ptEntryState.dac_tinh[key] = val;
            renderPtEntryForm();
        };
        window.updateDiemRoi = function(ngang, dai) {
            window.ptEntryState.dac_tinh.diem_roi_ngang = ngang;
            window.ptEntryState.dac_tinh.do_dai = dai;
            renderPtEntryForm();
        };

        window.savePtEntry = async function() {
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
            
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            closeModal();
            renderView('gameTimeline');
            showToast('Đã lưu điểm!', 'success');
        }

        async function undoLastPoint() {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            if(game.danh_sach_diem.length===0) return;
            game.danh_sach_diem.pop();
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            renderView('gameTimeline');
            showToast('Đã hoàn tác', 'success');
        }

        async function deletePoint(idx) {
            if(!confirm('Xóa điểm này sẽ tính lại tỷ số các điểm sau. Tiếp tục?')) return;
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            game.danh_sach_diem.splice(idx, 1);
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            renderView('gameTimeline');
        }

        async function toggleGameLock() {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            if(game.trang_thai === 'hoan_thanh') game.trang_thai = 'dang_dau';
            else game.trang_thai = 'hoan_thanh';
            await saveToGithub();
            renderView('gameTimeline');
        }

        function openEditPointModal(idx) {"""

content = re.sub(pattern, new_code, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
