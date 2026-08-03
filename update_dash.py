import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_dash_loop = """                const phuong_thuc = pt.phuong_thuc || (isWin ? 'toi_ghi_diem' : 'toi_danh_hong');

                if(pt.nhom === 'nhom_ky_thuat' && rallyStats[pt.ky_thuat]) {
                    rallyStats[pt.ky_thuat].total++;
                    if (isWin) rallyStats[pt.ky_thuat].win++; else rallyStats[pt.ky_thuat].lose++;
                    if(rallyStats[pt.ky_thuat][phuong_thuc] !== undefined) rallyStats[pt.ky_thuat][phuong_thuc]++;
                }
                if(pt.nhom === 'nhom_giao_bong' && serveStats[pt.ky_thuat]) {
                    serveStats[pt.ky_thuat].total++;
                    if (isWin) serveStats[pt.ky_thuat].win++; else serveStats[pt.ky_thuat].lose++;
                    if(serveStats[pt.ky_thuat][phuong_thuc] !== undefined) serveStats[pt.ky_thuat][phuong_thuc]++;
                }"""

new_dash_loop = """                const { nhom, ky_thuat, phuong_thuc } = getOldProps(pt, m);

                if(nhom === 'nhom_ky_thuat' && rallyStats[ky_thuat]) {
                    rallyStats[ky_thuat].total++;
                    if (isWin) rallyStats[ky_thuat].win++; else rallyStats[ky_thuat].lose++;
                    if(rallyStats[ky_thuat][phuong_thuc] !== undefined) rallyStats[ky_thuat][phuong_thuc]++;
                }
                if(nhom === 'nhom_giao_bong' && serveStats[ky_thuat]) {
                    serveStats[ky_thuat].total++;
                    if (isWin) serveStats[ky_thuat].win++; else serveStats[ky_thuat].lose++;
                    if(serveStats[ky_thuat][phuong_thuc] !== undefined) serveStats[ky_thuat][phuong_thuc]++;
                }"""

content = content.replace(old_dash_loop, new_dash_loop)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
