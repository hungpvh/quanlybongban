with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("async function handleEditPoint(e, idx) {")
end_idx = content.find("        }", start_idx) + 9

new_func = """async function handleEditPoint(e, idx) {
            e.preventDefault();
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            const pt = game.danh_sach_diem[idx];
            
            const loai = document.getElementById('ep_loai').value;
            const ktVal = document.getElementById('ep_kythuat').value.split('|');
            
            if (pt.loai_diem !== loai) {
                // If changing win/lose, reset phuong_thuc to default
                pt.phuong_thuc = loai === 'thang' ? 'toi_ghi_diem' : 'toi_danh_hong';
            }
            
            pt.loai_diem = loai;
            pt.nhom = ktVal[0];
            pt.ky_thuat = ktVal[1];
            
            recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
            await saveToGithub();
            closeModal();
            renderView('gameTimeline');
        }"""

new_content = content[:start_idx] + new_func + content[end_idx:]

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
