with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_str = "function renderMatchForm(container, editId = null) {"
end_str = "// --- MATCH DETAIL (GAMES LIST) ---"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    new_block = """function renderMatchForm(container, editId = null) {
            let match = { thong_tin: { ngay_thi_dau: new Date().toISOString().split('T')[0], loai_hinh: 'Giao hữu', doi_thu_1: 'Tôi' } };
            if (editId) match = appState.matches.find(m => m.id_tran_dau === editId) || match;
            const info = match.thong_tin || {};
            const schema = appState.dict.thong_tin_tran_dau || {};
            
            let formHtml = '';
            Object.keys(schema).forEach(key => {
                const label = schema[key];
                const value = info[key] || '';
                
                if (key === 'ngay_thi_dau') {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="date" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm" required></div>`;
                } else if (key === 'mo_ta') {
                    formHtml += `<div class="col-span-1 md:col-span-2"><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><textarea id="mf_${key}" rows="2" class="w-full border rounded p-2 text-sm">${escapeHtml(value)}</textarea></div>`;
                } else if (key.startsWith('link_')) {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="url" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm"></div>`;
                } else if (key === 'loai_hinh') {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="text" id="mf_${key}" list="loai_hinh_list" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm" required><datalist id="loai_hinh_list"><option value="Giao hữu"></option><option value="Đánh bia"></option><option value="Thi đấu giải"></option></datalist></div>`;
                } else if (key === 'doi_thu_1' || key === 'doi_thu_2' || key === 'ket_qua') {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="text" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm" required></div>`;
                } else {
                    formHtml += `<div><label class="block text-xs font-semibold text-gray-600 mb-1">${label}</label><input type="text" id="mf_${key}" value="${escapeHtml(value)}" class="w-full border rounded p-2 text-sm"></div>`;
                }
            });

            container.innerHTML = `
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4">
                    <h2 class="text-xl font-bold mb-4">${editId ? 'Sửa trận đấu' : 'Thêm trận đấu mới'}</h2>
                    <form id="match-form" class="space-y-4" onsubmit="handleMatchSubmit(event, '${editId}')">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            ${formHtml}
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
            const schema = appState.dict.thong_tin_tran_dau || {};
            const info = {};
            Object.keys(schema).forEach(key => {
                const el = document.getElementById(`mf_${key}`);
                if (el) {
                    info[key] = el.value;
                }
            });
            if (editId && editId !== 'null') {
                const match = appState.matches.find(m => m.id_tran_dau === editId);
                if(match) match.thong_tin = info;
            } else {
                appState.matches.unshift({ id_tran_dau: `match_${Date.now()}`, thong_tin: info, chi_tiet_game: [] });
            }
            await saveToGithub();
        }

        """
    content = content[:start_idx] + new_block + content[end_idx:]
    with open("/app/applet/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Could not find blocks")
