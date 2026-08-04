import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

target = "        function recalculateGameTimeline(game, dt1, dt2) {"

replacement = """        window.undoLastPoint = async function() {
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            if(game.danh_sach_diem.length > 0) {
                game.danh_sach_diem.pop();
                recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
                await saveToGithub();
                renderView(appState.view);
            }
        };

        window.deletePoint = async function(idx) {
            if(!confirm('Bạn có chắc chắn muốn xóa điểm này?')) return;
            const match = appState.matches.find(m => m.id_tran_dau === appState.currentMatchId);
            const game = match.chi_tiet_game[appState.currentGameIndex];
            if(idx >= 0 && idx < game.danh_sach_diem.length) {
                game.danh_sach_diem.splice(idx, 1);
                recalculateGameTimeline(game, match.thong_tin.doi_thu_1, match.thong_tin.doi_thu_2);
                await saveToGithub();
                renderView(appState.view);
            }
        };

        function recalculateGameTimeline(game, dt1, dt2) {"""

new_content = content.replace(target, replacement)

if new_content == content:
    print("Failed to replace undo_delete!")
else:
    with open("/app/applet/index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Done replacing undo_delete!")

