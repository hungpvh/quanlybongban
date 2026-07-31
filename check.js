        // --- CONSTANTS & MOCK DATA ---
        const MOCK_DICTIONARY = {
            "thong_tin_tran_dau": { "ngay_thi_dau": "Ngày thi đấu", "loai_hinh": "Loại hình", "doi_thu_1": "Tên Đối thủ 1", "doi_thu_2": "Tên Đối thủ 2", "chap_bong": "Chấp bóng", "ket_qua": "Tỷ số", "mo_ta": "Mô tả", "link_video": "Link video" },
            "loai_giao_bong": { "xuong_ngan": "Xoáy xuống ngắn", "xuong_dai": "Xoáy xuống dài sâu", "len_ngan": "Xoáy lên/ngang ngắn", "len_dai": "Xoáy lên/ngang dài nhanh", "long": "Bóng lỏng", "khong_doc_duoc": "Không đọc được" },
            "ky_thuat_rally": { "giat_phai": "Giật phải", "doi_cong_phai": "Đôi công phải", "flick_phai": "Flick phải", "giat_trai": "Giật trái", "doi_cong_trai": "Đôi công trái", "flick_trai": "Flick trái", "bat_dap_bong": "Bạt/Đập", "doi_giat_xa_ban": "Đối giật xa bàn", "phong_thu_phai": "Phòng thủ phải", "phong_thu_trai": "Phòng thủ trái", "go_day_bong": "Gò/Đẩy", "bat_ngan_tha_long": "Bắt ngắn/Thả lỏng", "cau_bong_bong": "Câu bóng bổng", "loi_khac": "Lỗi khác" }
        };
        const MOCK_MATCHES = [
            {
                "id_tran_dau": "match_1717123456",
                "thong_tin": { "ngay_thi_dau": "2026-07-30", "loai_hinh": "Đánh bia", "doi_thu_1": "Hungpv", "doi_thu_2": "Nguyễn Văn A", "chap_bong": "Tôi chấp 2", "ket_qua": "3-2", "mo_ta": "Đối thủ gò nặng.", "link_video": "" },
                "chi_tiet_game": [
                    {
                        "game_so": 1, "ty_so_bat_dau": "0-2", "nguoi_giao_bong_truoc": "Hungpv", "ty_so_chung_cuoc": "11-8", "trang_thai": "hoan_thanh",
                        "danh_sach_diem": [
                            { "thu_tu_diem": 1, "ty_so_hien_tai": "1-2", "loai_diem": "thang", "nhom": "nhom_giao_bong", "ky_thuat": "xuong_ngan", "nguoi_giao_bong": "Hungpv" },
                            { "thu_tu_diem": 2, "ty_so_hien_tai": "1-3", "loai_diem": "thua", "nhom": "nhom_ky_thuat", "ky_thuat": "phong_thu_trai", "nguoi_giao_bong": "Hungpv" }
                        ]
                    }
                ]
            }
        ];

        // --- STATE ---
        const appState = {
            view: 'list', // list, matchForm, matchDetail, gameTimeline, dashboard, settings
            matches: [],
            dict: null,
            isMock: true,
            currentMatchId: null,
            currentGameIndex: null,
            github: { user: '', repo: '', branch: 'main', dataPath: 'dulieubongban.json', dictPath: 'tu_dien_bong_ban.json', token: '', sha: null, dictSha: null },
            isLoading: false
        };

        // --- UTILS ---
        const b64EncodeUnicode = str => btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, (m, p1) => String.fromCharCode('0x' + p1)));
        const b64DecodeUnicode = str => decodeURIComponent(Array.prototype.map.call(atob(str), c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
        const escapeHtml = unsafe => (unsafe||'').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        const showToast = (msg, type='info') => {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            const bg = type==='error'?'bg-red-600':type==='success'?'bg-green-600':'bg-blue-600';
            toast.className = `${bg} text-white px-4 py-2 rounded shadow-lg text-sm transition-opacity duration-300`;
            toast.innerText = msg;
            container.appendChild(toast);
            setTimeout(() => { toast.classList.add('opacity-0'); setTimeout(() => toast.remove(), 300); }, 3000);
        };
        const showModal = (contentHtml) => {
            const m = document.getElementById('modal-container');
            m.innerHTML = `<div class="bg-black bg-opacity-50 absolute inset-0" onclick="closeModal()"></div><div class="bg-white rounded-lg shadow-xl z-10 w-full max-w-md max-h-[90vh] overflow-y-auto relative p-4">${contentHtml}</div>`;
            m.classList.remove('hidden');
        };
        const closeModal = () => document.getElementById('modal-container').classList.add('hidden');

        // --- GITHUB API ---
        async function loadGithubConfig() {
            const stored = localStorage.getItem('bongban_gh_config');
            if (stored) {
                appState.github = { ...appState.github, ...JSON.parse(stored) };
                if (appState.github.token && appState.github.user && appState.github.repo) {
                    await fetchGithubData();
                    return;
                }
            }
            useMockData();
        }
        function saveGithubConfig(config) {
            appState.github = { ...appState.github, ...config };
            localStorage.setItem('bongban_gh_config', JSON.stringify(appState.github));
        }
        async function githubApi(method, path, body = null) {
            const { user, repo, branch, token } = appState.github;
            // Thêm timestamp để tránh cache từ trình duyệt (hoặc dùng cache: 'no-store')
            const cacheBuster = method === 'GET' ? `&t=${Date.now()}` : '';
            const url = `https://api.github.com/repos/${user}/${repo}/contents/${path}${method==='GET'?`?ref=${branch}${cacheBuster}`:''}`;
            const headers = { 'Accept': 'application/vnd.github.v3+json', 'Authorization': `Bearer ${token}` };
            const options = { method, headers, cache: 'no-store' };
            if (body) options.body = JSON.stringify(body);
            const res = await fetch(url, options);
            if (!res.ok) throw new Error(await res.text());
            return res.json();
        }
        async function fetchGithubData() {
            try {
                showToast('Đang tải dữ liệu từ GitHub...', 'info');
                const [dataRes, dictRes] = await Promise.all([
                    githubApi('GET', appState.github.dataPath).catch(e => null),
                    githubApi('GET', appState.github.dictPath).catch(e => null)
                ]);
                
                if (dictRes && dictRes.content) {
                    appState.dict = JSON.parse(b64DecodeUnicode(dictRes.content));
                    appState.github.dictSha = dictRes.sha;
                } else { appState.dict = MOCK_DICTIONARY; }

                if (dataRes && dataRes.content) {
                    appState.matches = JSON.parse(b64DecodeUnicode(dataRes.content));
                    appState.github.sha = dataRes.sha;
                    appState.isMock = false;
                    showToast('Tải dữ liệu thành công!', 'success');
                } else {
                    appState.matches = [];
                    appState.isMock = false;
                    appState.github.sha = null;
                }
            } catch (e) {
                console.error(e);
                showToast('Lỗi tải GitHub. Đang dùng dữ liệu mẫu.', 'error');
                useMockData();
            }
            updateStatusBar();
            renderView(appState.view);
        }
        async function saveToGithub() {
            if (appState.isMock) { showToast('Đã lưu cục bộ (Chế độ mẫu).', 'success'); renderView(appState.view); return; }
            try {
                showToast('Đang đồng bộ lên GitHub...', 'info');
                // Luôn ngầm thực hiện một lệnh GET để xin lại mã SHA mới nhất từ GitHub
                const currentRes = await githubApi('GET', appState.github.dataPath).catch(e => null);
                let latestSha = appState.github.sha;
                if (currentRes && currentRes.sha) {
                    latestSha = currentRes.sha;
                }
                
                const content = b64EncodeUnicode(JSON.stringify(appState.matches, null, 2));
                const body = { message: 'Update matches', content, branch: appState.github.branch };
                if (latestSha) {
                    body.sha = latestSha;
                }
                
                const res = await githubApi('PUT', appState.github.dataPath, body);
                appState.github.sha = res.content.sha;
                showToast('Đã đồng bộ GitHub thành công!', 'success');
            } catch (e) {
                console.error(e);
                showToast('Lỗi đồng bộ: ' + (e.message || 'Unknown'), 'error');
                alert('Lỗi đồng bộ: ' + e.message);
            }
            renderView(appState.view);
        }
        function useMockData() {
            appState.isMock = true;
            appState.dict = MOCK_DICTIONARY;
            appState.matches = JSON.parse(JSON.stringify(MOCK_MATCHES));
            updateStatusBar();
            renderView(appState.view);
        }
        function updateStatusBar() {
            const bar = document.getElementById('status-bar');
            if (appState.isMock) { bar.classList.remove('hidden'); bar.innerText = 'Chế độ dữ liệu mẫu'; bar.classList.remove('bg-green-500'); bar.classList.add('bg-yellow-500'); }
            else { bar.classList.remove('hidden'); bar.innerText = 'Đã kết nối GitHub'; bar.classList.remove('bg-yellow-500'); bar.classList.add('bg-green-500'); }
        }

        // --- ROUTER ---
        function renderView(view, params = {}) {
            appState.view = view;
            if(params.matchId) appState.currentMatchId = params.matchId;
            if(params.gameIndex !== undefined) appState.currentGameIndex = params.gameIndex;
            const main = document.getElementById('app-main');
            main.innerHTML = '';
            closeModal();
            
            if(view === 'list') renderMatchList(main);
            else if(view === 'matchForm') renderMatchForm(main, params.editId);
            else if(view === 'matchDetail') renderMatchDetail(main);
            else if(view === 'gameTimeline') renderGameTimeline(main);
            else if(view === 'dashboard') renderDashboard(main);
            else if(view === 'settings') renderSettings(main);
            window.scrollTo(0,0);
        }

        // --- MATCH LIST ---
        function renderMatchList(container) {
            let html = `<div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold">Danh sách trận đấu</h2>
                <button onclick="renderView('matchForm')" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 shadow"><i class="fas fa-plus"></i> Thêm</button>
            </div>`;
            if (appState.matches.length === 0) {
                html += `<div class="text-center py-10 text-gray-500">Chưa có trận đấu nào.</div>`;
            } else {
                html += `<div class="space-y-4">`;
                appState.matches.forEach(m => {
                    const info = m.thong_tin;
                    const cGames = m.chi_tiet_game ? m.chi_tiet_game.length : 0;
                    html += `
                    <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <div class="text-xs text-gray-500 font-semibold mb-1"><i class="fas fa-calendar-alt"></i> ${info.ngay_thi_dau} &bull; ${escapeHtml(info.loai_hinh)}</div>
                                <h3 class="text-lg font-bold">${escapeHtml(info.doi_thu_1)} <span class="text-gray-400 font-normal">vs</span> ${escapeHtml(info.doi_thu_2)}</h3>
                            </div>
                            <div class="text-right">
                                <div class="text-sm font-semibold text-gray-500 uppercase">Tỷ số</div>
                                <div class="text-2xl font-black text-blue-600">${escapeHtml(info.ket_qua)}</div>
                            </div>
                        </div>
                        <div class="flex flex-wrap gap-2 mt-4 pt-3 border-t border-gray-100">
                            <button onclick="renderView('matchDetail', {matchId: '${m.id_tran_dau}'})" class="flex-1 bg-blue-50 text-blue-700 py-1.5 rounded font-medium text-sm hover:bg-blue-100 transition"><i class="fas fa-eye"></i> Xem & Điểm</button>
                            <button onclick="renderView('matchForm', {editId: '${m.id_tran_dau}'})" class="bg-gray-100 text-gray-700 px-3 py-1.5 rounded hover:bg-gray-200 transition"><i class="fas fa-edit"></i></button>
                            <button onclick="confirmDeleteMatch('${m.id_tran_dau}')" class="bg-red-50 text-red-600 px-3 py-1.5 rounded hover:bg-red-100 transition"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>`;
                });
                html += `</div>`;
            }
            container.innerHTML = html;
        }

        function confirmDeleteMatch(id) {
            showModal(`
                <h3 class="text-lg font-bold mb-2">Xóa trận đấu</h3>
                <p class="text-gray-600 mb-4">Bạn có chắc chắn muốn xóa trận đấu này không? Hành động này không thể hoàn tác.</p>
                <div class="flex justify-end gap-2">
                    <button onclick="closeModal()" class="px-4 py-2 bg-gray-200 rounded">Hủy</button>
                    <button onclick="deleteMatch('${id}')" class="px-4 py-2 bg-red-600 text-white rounded">Xóa</button>
                </div>
            `);
        }
        async function deleteMatch(id) {
            appState.matches = appState.matches.filter(m => m.id_tran_dau !== id);
            await saveToGithub();
            closeModal();
        }

        // --- MATCH FORM ---
        function renderMatchForm(container, editId = null) {
            let match = { thong_tin: { ngay_thi_dau: new Date().toISOString().split('T')[0], loai_hinh: 'Giao hữu', doi_thu_1: 'Hungpv', doi_thu_2: '', chap_bong: '', ket_qua: '', mo_ta: '', link_video: '' } };
            if (editId) match = appState.matches.find(m => m.id_tran_dau === editId) || match;
            const info = match.thong_tin;
            
            container.innerHTML = `
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
                    <h2 class="text-xl font-bold mb-4">${editId ? 'Sửa trận đấu' : 'Thêm trận đấu mới'}</h2>
                    <form id="match-form" class="space-y-4" onsubmit="handleMatchSubmit(event, '${editId}')">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Ngày thi đấu</label>
                                <input type="date" id="mf_ngay" value="${info.ngay_thi_dau}" class="w-full border rounded p-2 text-sm" required>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Loại hình</label>
                                <select id="mf_loai" class="w-full border rounded p-2 text-sm">
                                    <option value="Giao hữu" ${info.loai_hinh==='Giao hữu'?'selected':''}>Giao hữu</option>
                                    <option value="Đánh bia" ${info.loai_hinh==='Đánh bia'?'selected':''}>Đánh bia</option>
                                    <option value="Thi đấu giải" ${info.loai_hinh==='Thi đấu giải'?'selected':''}>Thi đấu giải</option>
                                </select>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Đối thủ 1 (Mình)</label>
                                <input type="text" id="mf_dt1" value="${escapeHtml(info.doi_thu_1)}" class="w-full border rounded p-2 text-sm" required>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Đối thủ 2</label>
                                <input type="text" id="mf_dt2" value="${escapeHtml(info.doi_thu_2)}" class="w-full border rounded p-2 text-sm" required placeholder="Tên đối thủ">
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Chấp bóng</label>
                                <input type="text" id="mf_chap" value="${escapeHtml(info.chap_bong)}" class="w-full border rounded p-2 text-sm" placeholder="VD: Tôi chấp 2">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-gray-600 mb-1">Tỷ số (Tự động hoặc thủ công)</label>
                                <input type="text" id="mf_kq" value="${escapeHtml(info.ket_qua)}" class="w-full border rounded p-2 text-sm" placeholder="VD: 3-2" required>
                            </div>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Mô tả / Nhận xét</label>
                            <textarea id="mf_mota" rows="2" class="w-full border rounded p-2 text-sm">${escapeHtml(info.mo_ta)}</textarea>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Link Video (YouTube/FB)</label>
                            <input type="url" id="mf_video" value="${escapeHtml(info.link_video)}" class="w-full border rounded p-2 text-sm">
                        </div>
                        <div class="flex gap-2 pt-4">
                            <button type="button" onclick="renderView('list')" class="flex-1 bg-gray-200 text-gray-800 py-2 rounded-lg font-medium">Hủy</button>
                            <button type="submit" class="flex-1 bg-blue-600 text-white py-2 rounded-lg font-medium">Lưu trận đấu</button>
                        </div>
                    </form>
                </div>
            `;
        }
        async function handleMatchSubmit(e, editId) {
            e.preventDefault();
            const info = {
                ngay_thi_dau: document.getElementById('mf_ngay').value,
                loai_hinh: document.getElementById('mf_loai').value,
                doi_thu_1: document.getElementById('mf_dt1').value,
                doi_thu_2: document.getElementById('mf_dt2').value,
                chap_bong: document.getElementById('mf_chap').value,
                ket_qua: document.getElementById('mf_kq').value,
                mo_ta: document.getElementById('mf_mota').value,
                link_video: document.getElementById('mf_video').value
            };
            if (editId && editId !== 'null') {
                const match = appState.matches.find(m => m.id_tran_dau === editId);
                if(match) match.thong_tin = info;
            } else {
                appState.matches.unshift({ id_tran_dau: `match_${Date.now()}`, thong_tin: info, chi_tiet_game: [] });
            }
            await saveToGithub();
        }

        // --- MATCH DETAIL (GAMES LIST) ---
        function calculateMatchResult(match) {
            if(!match.chi_tiet_game) return;
            let p1=0, p2=0;
            match.chi_tiet_game.forEach(g => {
                if(g.ty_so_chung_cuoc && g.trang_thai==='hoan_thanh') {
                    const parts = g.ty_so_chung_cuoc.split('-');
                    if(parts.length===2) {
                        const s1=parseInt(parts[0]), s2=parseInt(parts[1]);
                        if(s1>s2) p1++; else if(s2>s1) p2++;
                    }
                }
            });
            match.thong_tin.ket_qua = `${p1}-${p2}`;
        }
        
        async function autoUpdateResult() {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            calculateMatchResult(match);
            await saveToGithub();
            renderView('matchDetail', {matchId: appState.currentMatchId});
        }

        function renderMatchDetail(container) {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const info = match.thong_tin;
            const games = match.chi_tiet_game || [];
            
            let html = `
                <div class="mb-4 flex items-center justify-between">
                    <button onclick="renderView('list')" class="text-blue-600 font-medium"><i class="fas fa-chevron-left"></i> Quay lại</button>
                    <h2 class="text-lg font-bold">Chi tiết trận đấu</h2>
                    <div class="w-6"></div>
                </div>
                
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
                    <div class="flex justify-between items-center mb-2">
                        <div class="text-lg font-bold">${escapeHtml(info.doi_thu_1)} <span class="text-gray-400">vs</span> ${escapeHtml(info.doi_thu_2)}</div>
                        <div class="text-xl font-black text-blue-600">${escapeHtml(info.ket_qua)}</div>
                    </div>
                    <div class="text-sm text-gray-600 mb-3">${escapeHtml(info.loai_hinh)} &bull; ${info.ngay_thi_dau} &bull; ${escapeHtml(info.chap_bong)}</div>
                    ${info.mo_ta ? `<div class="text-sm text-gray-700 italic bg-gray-50 p-2 rounded mb-3">"${escapeHtml(info.mo_ta)}"</div>` : ''}
                    <div class="flex gap-2">
                        ${info.link_video ? `<a href="${escapeHtml(info.link_video)}" target="_blank" rel="noopener noreferrer" class="text-xs bg-red-100 text-red-600 px-3 py-1.5 rounded font-medium"><i class="fab fa-youtube"></i> Xem Video</a>` : ''}
                        <button onclick="autoUpdateResult()" class="text-xs bg-gray-100 text-gray-700 px-3 py-1.5 rounded font-medium"><i class="fas fa-sync"></i> Tự tính tỷ số</button>
                    </div>
                </div>
                
                <div class="flex justify-between items-center mb-3 mt-6">
                    <h3 class="text-lg font-bold">Các game đấu (${games.length})</h3>
                    <button onclick="openGameModal()" class="bg-blue-600 text-white px-3 py-1.5 rounded text-sm font-medium"><i class="fas fa-plus"></i> Thêm Game</button>
                </div>
                <div class="space-y-3">
            `;
            
            if(games.length===0) {
                html += `<div class="text-center py-6 text-gray-500 bg-white rounded-xl border border-dashed border-gray-300">Chưa có game nào.</div>`;
            } else {
                games.forEach((g, i) => {
                    const isFinished = g.trang_thai === 'hoan_thanh';
                    html += `
                    <div class="bg-white rounded-xl shadow-sm border ${isFinished?'border-green-200':'border-blue-200'} p-3 flex justify-between items-center cursor-pointer transition hover:bg-gray-50" onclick="renderView('gameTimeline', {matchId: '${match.id_tran_dau}', gameIndex: ${i}})">
                        <div>
                            <div class="font-bold text-gray-800">Game ${g.game_so} <span class="text-xs font-normal text-gray-500 ml-2">(Bắt đầu: ${g.ty_so_bat_dau})</span></div>
                            <div class="text-xs text-gray-500 mt-1">Giao trước: <span class="font-semibold text-gray-700">${g.nguoi_giao_bong_truoc}</span></div>
                        </div>
                        <div class="flex items-center gap-4">
                            <div class="text-lg font-black ${isFinished?'text-green-600':'text-blue-600'}">${g.ty_so_chung_cuoc || 'Đang đấu'}</div>
                            <button onclick="event.stopPropagation(); openGameModal(${i})" class="text-gray-400 hover:text-blue-600 p-1"><i class="fas fa-cog"></i></button>
                        </div>
                    </div>`;
                });
            }
            html += `</div>`;
            container.innerHTML = html;
        }

        function openGameModal(editIdx = null) {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const games = match.chi_tiet_game || [];
            let g = { game_so: games.length + 1, ty_so_bat_dau: '0-0', nguoi_giao_bong_truoc: match.thong_tin.doi_thu_1 };
            if(editIdx !== null) g = games[editIdx];
            
            showModal(`
                <h3 class="text-lg font-bold mb-4">${editIdx !== null ? 'Sửa thông tin Game' : 'Thêm Game mới'}</h3>
                <form onsubmit="handleGameSubmit(event, ${editIdx})" class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold mb-1">Game số</label>
                        <input type="number" id="gm_so" value="${g.game_so}" class="w-full border rounded p-2" required>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold mb-1">Tỷ số bắt đầu (Mình - Địch)</label>
                        <input type="text" id="gm_batdau" value="${g.ty_so_bat_dau}" class="w-full border rounded p-2" required pattern="[0-9]+-[0-9]+" placeholder="VD: 0-0, 0-2">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold mb-1">Người giao bóng trước</label>
                        <select id="gm_giaotruoc" class="w-full border rounded p-2">
                            <option value="${match.thong_tin.doi_thu_1}" ${g.nguoi_giao_bong_truoc===match.thong_tin.doi_thu_1?'selected':''}>${match.thong_tin.doi_thu_1} (Mình)</option>
                            <option value="${match.thong_tin.doi_thu_2}" ${g.nguoi_giao_bong_truoc===match.thong_tin.doi_thu_2?'selected':''}>${match.thong_tin.doi_thu_2}</option>
                        </select>
                    </div>
                    <div class="flex gap-2 pt-2">
                        <button type="button" onclick="closeModal()" class="flex-1 bg-gray-200 py-2 rounded font-medium">Hủy</button>
                        <button type="submit" class="flex-1 bg-blue-600 text-white py-2 rounded font-medium">Lưu</button>
                    </div>
                    ${editIdx !== null ? `<div class="pt-4 border-t mt-4"><button type="button" onclick="deleteGame(${editIdx})" class="w-full text-red-600 py-2 border border-red-200 bg-red-50 rounded font-medium"><i class="fas fa-trash"></i> Xóa Game này</button></div>` : ''}
                </form>
            `);
        }
        async function handleGameSubmit(e, editIdx) {
            e.preventDefault();
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            if(!match.chi_tiet_game) match.chi_tiet_game = [];
            
            const g = {
                game_so: parseInt(document.getElementById('gm_so').value),
                ty_so_bat_dau: document.getElementById('gm_batdau').value,
                nguoi_giao_bong_truoc: document.getElementById('gm_giaotruoc').value
            };
            
            if(editIdx !== null) {
                const old = match.chi_tiet_game[editIdx];
                old.game_so = g.game_so;
                old.ty_so_bat_dau = g.ty_so_bat_dau;
                old.nguoi_giao_bong_truoc = g.nguoi_giao_bong_truoc;
                recalculateGameTimeline(old, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            } else {
                match.chi_tiet_game.push({
                    ...g,
                    ty_so_chung_cuoc: g.ty_so_bat_dau,
                    trang_thai: 'dang_dau',
                    danh_sach_diem: []
                });
            }
            await saveToGithub();
            closeModal();
            renderView('matchDetail', {matchId: appState.currentMatchId});
        }
        async function deleteGame(idx) {
            if(!confirm('Bạn có chắc chắn muốn xóa game này và toàn bộ điểm số của nó?')) return;
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            match.chi_tiet_game.splice(idx, 1);
            await saveToGithub();
            closeModal();
            renderView('matchDetail', {matchId: appState.currentMatchId});
        }

        // --- GAME LOGIC (SCORING & SERVING) ---
        function parseScore(str) { const p = (str||'0-0').split('-'); return { p1: parseInt(p[0])||0, p2: parseInt(p[1])||0 }; }
        function stringifyScore(p1, p2) { return `${p1}-${p2}`; }
        function calculateCurrentState(startScoreStr, ptsArray) {
            let {p1, p2} = parseScore(startScoreStr);
            for(let pt of ptsArray) { if(pt.loai_diem === 'thang') p1++; else p2++; }
            return {p1, p2, total: p1+p2};
        }
        function determineServer(startScore, pointsArray, firstServerAtStart, doiThu1, doiThu2) {
            let { p1, p2 } = parseScore(startScore);
            let tempP1 = p1, tempP2 = p2;
            let currentServer = firstServerAtStart;
            
            for (let i = 0; i < pointsArray.length; i++) {
                if (tempP1 >= 10 && tempP2 >= 10) {
                    currentServer = currentServer === doiThu1 ? doiThu2 : doiThu1;
                } else {
                    if ((p1 + p2 + i) % 2 === 1) {
                        currentServer = currentServer === doiThu1 ? doiThu2 : doiThu1;
                    }
                }
                let pt = pointsArray[i];
                if (pt.loai_diem === 'thang') tempP1++; else tempP2++;
            }
            return currentServer;
        }
        function recalculateGameTimeline(game, dt1, dt2) {
            let {p1, p2} = parseScore(game.ty_so_bat_dau);
            let tempPts = [];
            for(let i=0; i<game.danh_sach_diem.length; i++) {
                let pt = game.danh_sach_diem[i];
                let server = determineServer(game.ty_so_bat_dau, tempPts, game.nguoi_giao_bong_truoc, dt1, dt2);
                if(pt.loai_diem==='thang') p1++; else p2++;
                pt.thu_tu_diem = i+1;
                pt.nguoi_giao_bong = server;
                pt.ty_so_hien_tai = stringifyScore(p1, p2);
                tempPts.push(pt);
            }
            game.ty_so_chung_cuoc = stringifyScore(p1, p2);
        }
        function isGameFinished(p1, p2) { return ((p1>=11 && p1-p2>=2) || (p2>=11 && p2-p1>=2)); }

        // --- TIMELINE & POINT INPUT ---
        let inputTab = 'thang'; // thang, thua
        function renderGameTimeline(container) {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            const state = calculateCurrentState(game.ty_so_bat_dau, game.danh_sach_diem);
            const nextServer = determineServer(game.ty_so_bat_dau, game.danh_sach_diem, game.nguoi_giao_bong_truoc, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            const isFinished = isGameFinished(state.p1, state.p2);
            const isLocked = game.trang_thai === 'hoan_thanh';

            // Dictionay Arrays
            const techKeys = Object.keys(appState.dict.ky_thuat_rally);
            
            let html = `
                <div class="fixed top-14 left-0 right-0 z-20 bg-white shadow-sm border-b">
                    <div class="max-w-3xl mx-auto px-4 py-2 flex justify-between items-center">
                        <button onclick="renderView('matchDetail')" class="text-blue-600 p-2"><i class="fas fa-chevron-left"></i></button>
                        <div class="text-center flex-1">
                            <div class="text-xs text-gray-500 font-semibold uppercase tracking-widest">Game ${game.game_so}</div>
                            <div class="text-3xl font-black ${state.p1>state.p2?'text-blue-600':state.p1<state.p2?'text-yellow-600':'text-gray-800'} tracking-tighter">${state.p1} - ${state.p2}</div>
                        </div>
                        <div class="text-right text-xs">
                            <div class="text-gray-400">Giao bóng:</div>
                            <div class="font-bold text-blue-700 max-w-[80px] truncate" title="${nextServer}">${nextServer}</div>
                        </div>
                    </div>
                    ${isFinished && !isLocked ? `<div class="bg-green-100 text-green-800 text-xs text-center py-1 font-medium">Game đã đủ điều kiện kết thúc</div>` : ''}
                    
                    ${isLocked ? `
                        <div class="px-4 py-3 bg-gray-50 flex gap-2 justify-center border-t">
                            <button onclick="toggleGameLock()" class="bg-gray-200 text-gray-800 px-4 py-1.5 rounded-full text-sm font-medium hover:bg-gray-300 transition"><i class="fas fa-unlock"></i> Mở lại game</button>
                        </div>
                    ` : ''}
                </div>
                
                <div class="${isLocked ? 'mt-24' : 'mt-24'} mb-4">
            `;
            
            if(!isLocked) {
                html += `<div class="flex gap-4 mb-6">`;
                html += `<button onclick="openPointModal('thang')" class="flex-1 bg-blue-600 text-white rounded-xl p-4 font-bold text-lg hover:bg-blue-700 transition shadow-sm flex flex-col items-center justify-center gap-1"><i class="fas fa-plus-circle text-2xl mb-1"></i> ĐIỂM THẮNG</button>`;
                html += `<button onclick="openPointModal('thua')" class="flex-1 bg-yellow-500 text-white rounded-xl p-4 font-bold text-lg hover:bg-yellow-600 transition shadow-sm flex flex-col items-center justify-center gap-1"><i class="fas fa-minus-circle text-2xl mb-1"></i> ĐIỂM THUA</button>`;
                html += `</div>`;
            }

            // Timeline
            html += `
                <div class="flex justify-between items-center mb-3 border-b pb-2">
                    <h3 class="font-bold text-gray-700">Timeline</h3>
                    <div class="flex gap-2">
                        ${!isLocked && game.danh_sach_diem.length>0 ? `<button onclick="undoLastPoint()" class="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded hover:bg-gray-300"><i class="fas fa-undo"></i> Undo</button>`:''}
                        ${!isLocked ? `<button onclick="toggleGameLock()" class="text-xs bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700 shadow-sm"><i class="fas fa-check"></i> Hoàn thành</button>`:''}
                    </div>
                </div>
                <div class="space-y-2">
            `;
            
            const reversedPts = [...game.danh_sach_diem].reverse();
            if(reversedPts.length === 0) {
                html += `<div class="text-center text-gray-400 py-4 text-sm">Chưa có điểm nào.</div>`;
            } else {
                reversedPts.forEach(pt => {                    const isWin = pt.loai_diem === 'thang';
                    const name = pt.nhom === 'nhom_giao_bong' ? appState.dict.loai_giao_bong[pt.ky_thuat] : appState.dict.ky_thuat_rally[pt.ky_thuat];
                    const dictPT = { "toi_ghi_diem": "Tôi ghi điểm", "doi_thu_danh_hong": "Đối thủ đánh hỏng", "toi_danh_hong": "Tôi đánh hỏng", "doi_thu_ghi_diem": "Đối thủ ghi điểm" };
                    const ptName = pt.phuong_thuc ? dictPT[pt.phuong_thuc] : (isWin ? "Tôi ghi điểm" : "Tôi đánh hỏng");
                    const ptColor = pt.phuong_thuc === 'toi_ghi_diem' || pt.phuong_thuc === 'doi_thu_danh_hong' ? 'text-blue-600' : 'text-red-500';
                    html += `
                        <div class="bg-white p-3 rounded-lg border ${isWin?'border-blue-200 border-l-4 border-l-blue-500':'border-red-200 border-l-4 border-l-red-500'} shadow-sm flex items-center justify-between text-sm">
                            <div class="flex items-center gap-3">
                                <div class="font-black w-10 text-center ${isWin?'text-blue-600':'text-red-600'}">${pt.ty_so_hien_tai}</div>
                                <div>
                                    <div class="font-bold text-gray-800">${name} <span class="text-xs font-semibold px-1.5 py-0.5 rounded ml-1 bg-gray-100 ${ptColor}">${ptName}</span></div>
                                    <div class="text-xs text-gray-500 mt-0.5">Giao: ${pt.nguoi_giao_bong} &bull; #${pt.thu_tu_diem}</div>
                                </div>
                            </div>
                            ${!isLocked ? `
                            <div class="flex gap-1">
                                <button onclick="openEditPointModal(${pt.thu_tu_diem-1})" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-blue-600 bg-gray-50 rounded"><i class="fas fa-pencil-alt"></i></button>
                                <button onclick="deletePoint(${pt.thu_tu_diem-1})" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-red-600 bg-gray-50 rounded"><i class="fas fa-trash"></i></button>
                            </div>` : ''}
                        </div>
                    `;
                });
            }
            
            html += `</div></div>`;
            container.innerHTML = html;
        }
        function openPointModal(loai_diem) {
            const isWin = loai_diem === 'thang';
            const titleA = isWin ? "TÔI GHI ĐIỂM" : "TÔI ĐÁNH HỎNG";
            const methodA = isWin ? "toi_ghi_diem" : "toi_danh_hong";
            const titleB = isWin ? "ĐỐI THỦ ĐÁNH HỎNG" : "ĐỐI THỦ GHI ĐIỂM";
            const methodB = isWin ? "doi_thu_danh_hong" : "doi_thu_ghi_diem";

            const techKeys = Object.keys(appState.dict.ky_thuat_rally);
            const serveKeys = Object.keys(appState.dict.loai_giao_bong);
            
            const btnClassA = isWin ? "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100" : "bg-red-50 text-red-700 border-red-200 hover:bg-red-100";
            const btnClassB = isWin ? "bg-green-50 text-green-700 border-green-200 hover:bg-green-100" : "bg-orange-50 text-orange-700 border-orange-200 hover:bg-orange-100";
            
            let htmlA = `<h4 class="font-bold text-sm mb-3 text-center border-b pb-1">${titleA}</h4>`;
            htmlA += `<div class="font-semibold text-xs text-gray-500 mb-2 mt-3 uppercase">Giao bóng</div><div class="grid grid-cols-1 gap-2">`;
            serveKeys.forEach(k => {
                htmlA += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_giao_bong', '${methodA}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassA}">${appState.dict.loai_giao_bong[k]}</button>`;
            });
            htmlA += `</div><div class="font-semibold text-xs text-gray-500 mb-2 mt-4 uppercase">Kỹ thuật</div><div class="grid grid-cols-1 gap-2">`;
            techKeys.forEach(k => {
                htmlA += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_ky_thuat', '${methodA}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassA}">${appState.dict.ky_thuat_rally[k]}</button>`;
            });
            htmlA += `</div>`;

            let htmlB = `<h4 class="font-bold text-sm mb-3 text-center border-b pb-1">${titleB}</h4>`;
            htmlB += `<div class="font-semibold text-xs text-gray-500 mb-2 mt-3 uppercase">Giao bóng</div><div class="grid grid-cols-1 gap-2">`;
            serveKeys.forEach(k => {
                htmlB += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_giao_bong', '${methodB}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassB}">${appState.dict.loai_giao_bong[k]}</button>`;
            });
            htmlB += `</div><div class="font-semibold text-xs text-gray-500 mb-2 mt-4 uppercase">Kỹ thuật</div><div class="grid grid-cols-1 gap-2">`;
            techKeys.forEach(k => {
                htmlB += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_ky_thuat', '${methodB}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassB}">${appState.dict.ky_thuat_rally[k]}</button>`;
            });
            htmlB += `</div>`;

            let html = `
                <div class="flex justify-between items-center mb-4 border-b pb-2">
                    <h3 class="text-xl font-black ${isWin?'text-blue-600':'text-red-600'}">${isWin ? 'GHI ĐIỂM' : 'MẤT ĐIỂM'}</h3>
                    <button onclick="closeModal()" class="text-gray-400 hover:text-gray-800"><i class="fas fa-times text-xl"></i></button>
                </div>
                <div class="flex gap-4 max-h-[70vh] overflow-y-auto pb-4">
                    <div class="flex-1">${htmlA}</div>
                    <div class="flex-1 border-l pl-4">${htmlB}</div>
                </div>
            `;
            showModal(html);
        }

        async function addPoint(loai_diem, ky_thuat, nhom, phuong_thuc) {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            const state = calculateCurrentState(game.ty_so_bat_dau, game.danh_sach_diem);
            
            if(isGameFinished(state.p1, state.p2) && !confirm('Game đã đủ điều kiện kết thúc. Bạn có chắc chắn muốn nhập thêm điểm?')) return;
            
            game.danh_sach_diem.push({
                thu_tu_diem: game.danh_sach_diem.length + 1,
                ty_so_hien_tai: '', // calculated below
                loai_diem: loai_diem,
                nhom: nhom,
                ky_thuat: ky_thuat,
                phuong_thuc: phuong_thuc,
                nguoi_giao_bong: '' // calculated below
            });
            
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            renderView('gameTimeline');
        }

        async function undoLastPoint() {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            if(game.danh_sach_diem.length===0) return;
            game.danh_sach_diem.pop();
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            renderView('gameTimeline');
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
        function openEditPointModal(idx) {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            const pt = game.danh_sach_diem[idx];
            
            let techOptions = '';
            Object.keys(appState.dict.ky_thuat_rally).forEach(k => techOptions += `<option value="nhom_ky_thuat|${k}" ${pt.ky_thuat===k?'selected':''}>Kỹ thuật: ${appState.dict.ky_thuat_rally[k]}</option>`);
            Object.keys(appState.dict.loai_giao_bong).forEach(k => techOptions += `<option value="nhom_giao_bong|${k}" ${pt.ky_thuat===k?'selected':''}>Giao bóng: ${appState.dict.loai_giao_bong[k]}</option>`);
            
            showModal(`
                <h3 class="text-lg font-bold mb-4">Sửa điểm #${idx+1}</h3>
                <form onsubmit="handleEditPoint(event, ${idx})" class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold mb-1">Kết quả điểm</label>
                        <select id="ep_loai" class="w-full border rounded p-2" onchange="updateEditPhuongThuc(this.value)">
                            <option value="thang" ${pt.loai_diem==='thang'?'selected':''}>Điểm thắng</option>
                            <option value="thua" ${pt.loai_diem==='thua'?'selected':''}>Điểm thua</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold mb-1">Phương thức</label>
                        <select id="ep_phuongthuc" class="w-full border rounded p-2">
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold mb-1">Loại kỹ thuật / Giao bóng</label>
                        <select id="ep_kythuat" class="w-full border rounded p-2">
                            ${techOptions}
                        </select>
                    </div>
                    <div class="flex gap-2 pt-2">
                        <button type="button" onclick="closeModal()" class="flex-1 bg-gray-200 py-2 rounded font-medium">Hủy</button>
                        <button type="submit" class="flex-1 bg-blue-600 text-white py-2 rounded font-medium">Cập nhật</button>
                    </div>
                </form>
            `);
            window._tempPtPhuongThuc = pt.phuong_thuc;
            updateEditPhuongThuc(pt.loai_diem);
        }

        window.updateEditPhuongThuc = function(loai_diem) {
            const select = document.getElementById('ep_phuongthuc');
            if(!select) return;
            const current = window._tempPtPhuongThuc;
            if (loai_diem === 'thang') {
                select.innerHTML = `
                    <option value="toi_ghi_diem" ${current==='toi_ghi_diem'?'selected':''}>Tôi ghi điểm</option>
                    <option value="doi_thu_danh_hong" ${current==='doi_thu_danh_hong'?'selected':''}>Đối thủ đánh hỏng</option>
                `;
            } else {
                select.innerHTML = `
                    <option value="toi_danh_hong" ${current==='toi_danh_hong'?'selected':''}>Tôi đánh hỏng</option>
                    <option value="doi_thu_ghi_diem" ${current==='doi_thu_ghi_diem'?'selected':''}>Đối thủ ghi điểm</option>
                `;
            }
            window._tempPtPhuongThuc = null;
        }

        async function handleEditPoint(e, idx) {
            e.preventDefault();
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            const pt = game.danh_sach_diem[idx];
            
            const loai = document.getElementById('ep_loai').value;
            const ktVal = document.getElementById('ep_kythuat').value.split('|');
            const ptPhuongThuc = document.getElementById('ep_phuongthuc').value;
            
            pt.loai_diem = loai;
            pt.phuong_thuc = ptPhuongThuc;
            pt.nhom = ktVal[0];
            pt.ky_thuat = ktVal[1];
            
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            closeModal();
            renderView('gameTimeline');
        }

        // --- DASHBOARD ---
        function renderDashboard(container) {
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

window.updateDashboardFilter = function(key, value) {
    appState.dashboardFilter[key] = value;
    renderView('dashboard');
};

window.clearDashboardFilter = function() {
    appState.dashboardFilter = { matchId: 'all', fromDate: '', toDate: '', loai_hinh: 'all', doi_thu: 'all', _lastMatchId: 'all' };
    renderView('dashboard');
};

        // --- SETTINGS ---
        function renderSettings(container) {
            const { user, repo, branch, dataPath, dictPath, token } = appState.github;
            container.innerHTML = `
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
                    <h2 class="text-xl font-bold mb-2">Cài đặt GitHub</h2>
                    <p class="text-xs text-yellow-600 bg-yellow-50 p-2 rounded mb-4">
                        <i class="fas fa-exclamation-triangle"></i> Personal Access Token được lưu trong trình duyệt. Chỉ nên sử dụng fine-grained token có quyền giới hạn đối với đúng repository cần thiết. Không sử dụng ứng dụng trên thiết bị công cộng.
                    </p>
                    <form onsubmit="handleSettingsSubmit(event)" class="space-y-4">
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">GitHub Username / Organization</label>
                            <input type="text" id="st_user" value="${escapeHtml(user)}" class="w-full border rounded p-2 text-sm" required>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Repository Name</label>
                            <input type="text" id="st_repo" value="${escapeHtml(repo)}" class="w-full border rounded p-2 text-sm" required>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Branch</label>
                            <input type="text" id="st_branch" value="${escapeHtml(branch)}" class="w-full border rounded p-2 text-sm" required>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Data File Path</label>
                            <input type="text" id="st_data" value="${escapeHtml(dataPath)}" class="w-full border rounded p-2 text-sm" required>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Dictionary File Path</label>
                            <input type="text" id="st_dict" value="${escapeHtml(dictPath)}" class="w-full border rounded p-2 text-sm" required>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Personal Access Token</label>
                            <input type="password" id="st_token" value="${escapeHtml(token)}" class="w-full border rounded p-2 text-sm" placeholder="ghp_...">
                        </div>
                        <div class="flex gap-2 pt-4 flex-wrap">
                            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium shadow flex-1 whitespace-nowrap"><i class="fas fa-save"></i> Lưu & Kết nối</button>
                            <button type="button" onclick="clearSettings()" class="bg-red-50 text-red-600 border border-red-200 px-4 py-2 rounded-lg font-medium flex-1 whitespace-nowrap"><i class="fas fa-trash"></i> Xóa Token</button>
                            <button type="button" onclick="useMockData()" class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium w-full mt-2"><i class="fas fa-database"></i> Dùng Dữ Liệu Mẫu</button>
                        </div>
                    </form>
                </div>
            `;
        }
        async function handleSettingsSubmit(e) {
            e.preventDefault();
            saveGithubConfig({
                user: document.getElementById('st_user').value,
                repo: document.getElementById('st_repo').value,
                branch: document.getElementById('st_branch').value,
                dataPath: document.getElementById('st_data').value,
                dictPath: document.getElementById('st_dict').value,
                token: document.getElementById('st_token').value
            });
            await fetchGithubData();
        }
        function clearSettings() {
            saveGithubConfig({ token: '' });
            showToast('Đã xóa token.');
            renderView('settings');
        }

        // --- INIT ---
        document.addEventListener('DOMContentLoaded', () => {
            loadGithubConfig();
        });
