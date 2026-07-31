import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_add_point = r"""async function addPoint\(ky_thuat, nhom\) \{.*?loai_diem: inputTab,.*?nguoi_giao_bong: '' // calculated below\s*\}\);"""
new_add_point = """async function addPoint(loai_diem, ky_thuat, nhom, phuong_thuc) {
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
            });"""

content = re.sub(old_add_point, new_add_point, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
