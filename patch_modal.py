import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_modal = r"""\s*function openEditPointModal\(idx\) \{.*?\s*async function handleEditPoint\(e, idx\) \{.*?renderView\('gameTimeline'\);\s*\}"""

new_modal = """
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
        }"""

content = re.sub(old_modal, new_modal, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
