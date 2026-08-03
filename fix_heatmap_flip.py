import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace heatmap and spin section in calculateDashboardStats
old_block = """                const dac_tinh = c.dac_tinh;
                if (dac_tinh) {
                    if (dac_tinh.diem_roi_ngang && dac_tinh.do_dai) {
                        const key = `${dac_tinh.do_dai}_${dac_tinh.diem_roi_ngang}`;
                        if (isWin) s.heatmapWinner[key] = (s.heatmapWinner[key] || 0) + 1;
                        else s.heatmapLost[key] = (s.heatmapLost[key] || 0) + 1;
                    }"""

new_block = """                const dac_tinh = c.dac_tinh;
                if (dac_tinh) {
                    if (dac_tinh.diem_roi_ngang && dac_tinh.do_dai) {
                        let ngang = dac_tinh.diem_roi_ngang;
                        // Nếu góc nhìn là đối thủ 2, thì trái của người 1 là phải của người 2 và ngược lại.
                        if (perspective === 'doi_thu_2') {
                            if (ngang === 'trai') ngang = 'phai';
                            else if (ngang === 'phai') ngang = 'trai';
                        }
                        const key = `${dac_tinh.do_dai}_${ngang}`;
                        if (isWin) s.heatmapWinner[key] = (s.heatmapWinner[key] || 0) + 1;
                        else s.heatmapLost[key] = (s.heatmapLost[key] || 0) + 1;
                    }"""

content = content.replace(old_block, new_block)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
