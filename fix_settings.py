import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

settings_code = """        // --- SETTINGS ---
        function renderSettings(container) {
            const { user, repo, codeBranch, dataBranch, dataPath, dictPath, token } = appState.github;
            container.innerHTML = `
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
                    <h2 class="text-xl font-bold mb-2">Cài đặt GitHub</h2>
                    <p class="text-xs text-yellow-600 bg-yellow-50 p-2 rounded mb-4">
                        <i class="fas fa-exclamation-triangle"></i> Personal Access Token được lưu trong trình duyệt.
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
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Nhánh Mã Nguồn (Code Branch)</label>
                            <input type="text" id="st_codeBranch" value="${escapeHtml(codeBranch || 'main')}" class="w-full border rounded p-2 text-sm" required>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-gray-600 mb-1">Nhánh Dữ Liệu (Data Branch)</label>
                            <input type="text" id="st_dataBranch" value="${escapeHtml(dataBranch || 'data')}" class="w-full border rounded p-2 text-sm" required>
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
                            <button type="button" onclick="testGithubConnection()" class="bg-green-100 text-green-700 border border-green-200 px-4 py-2 rounded-lg font-medium flex-1 whitespace-nowrap"><i class="fas fa-check-circle"></i> Kiểm tra kết nối</button>
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
                codeBranch: document.getElementById('st_codeBranch').value,
                dataBranch: document.getElementById('st_dataBranch').value,
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
        
        async function testGithubConnection() {
            const btn = event.currentTarget;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang kiểm tra...';
            btn.disabled = true;
            try {
                const { user, repo, dataBranch, token, dataPath, dictPath } = appState.github;
                const branchToUse = dataBranch || 'data';
                const headers = { 'Accept': 'application/vnd.github.v3+json', 'Authorization': `Bearer ${token}` };
                
                const checkFile = async (path) => {
                    const url = `https://api.github.com/repos/${user}/${repo}/contents/${path}?ref=${branchToUse}&t=${Date.now()}`;
                    const res = await fetch(url, { headers, cache: 'no-store' });
                    if (!res.ok) throw new Error(`Không tìm thấy file ${path} trên nhánh ${branchToUse}`);
                    return true;
                };
                
                await checkFile(dataPath);
                await checkFile(dictPath);
                
                showToast(`Kết nối thành công với nhánh dữ liệu: ${branchToUse}`, 'success');
            } catch (err) {
                showToast(`Lỗi: ${err.message}`, 'error');
            } finally {
                btn.innerHTML = '<i class="fas fa-check-circle"></i> Kiểm tra kết nối';
                btn.disabled = false;
            }
        }

        // --- INIT ---"""

content = content.replace("        // --- INIT ---", settings_code)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Settings UI added.")
