import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update renderGameTimeline loop
old_timeline_pts = """                    const isWin = pt.loai_diem === 'thang';
                    const name = pt.nhom === 'nhom_giao_bong' ? appState.dict.loai_giao_bong[pt.ky_thuat] : appState.dict.ky_thuat_rally[pt.ky_thuat];
                    const dictPT = { "toi_ghi_diem": "Tôi ghi điểm", "doi_thu_danh_hong": "Đối thủ đánh hỏng", "toi_danh_hong": "Tôi đánh hỏng", "doi_thu_ghi_diem": "Đối thủ ghi điểm" };
                    const ptName = pt.phuong_thuc ? dictPT[pt.phuong_thuc] : (isWin ? "Tôi ghi điểm" : "Tôi đánh hỏng");
                    const ptColor = pt.phuong_thuc === 'toi_ghi_diem' || pt.phuong_thuc === 'doi_thu_danh_hong' ? 'text-blue-600' : 'text-red-500';"""

new_timeline_pts = """                    const isWin = pt.loai_diem === 'thang';
                    const { nhom, ky_thuat, phuong_thuc } = getOldProps(pt, match);
                    const name = nhom === 'nhom_giao_bong' ? (appState.dict.loai_giao_bong[ky_thuat]||ky_thuat) : (appState.dict.ky_thuat_rally[ky_thuat]||ky_thuat);
                    const dictPT = { "toi_ghi_diem": "Tôi ghi điểm", "doi_thu_danh_hong": "Đối thủ đánh hỏng", "toi_danh_hong": "Tôi đánh hỏng", "doi_thu_ghi_diem": "Đối thủ ghi điểm" };
                    const ptName = phuong_thuc ? dictPT[phuong_thuc] : (isWin ? "Tôi ghi điểm" : "Tôi đánh hỏng");
                    const ptColor = phuong_thuc === 'toi_ghi_diem' || phuong_thuc === 'doi_thu_danh_hong' ? 'text-blue-600' : 'text-red-500';"""

content = content.replace(old_timeline_pts, new_timeline_pts)


# Update openEditPointModal
old_modal = """            let techOptions = '';
            Object.keys(appState.dict.ky_thuat_rally).forEach(k => techOptions += `<option value="nhom_ky_thuat|${k}" ${pt.ky_thuat===k?'selected':''}>Kỹ thuật: ${appState.dict.ky_thuat_rally[k]}</option>`);
            Object.keys(appState.dict.loai_giao_bong).forEach(k => techOptions += `<option value="nhom_giao_bong|${k}" ${pt.ky_thuat===k?'selected':''}>Giao bóng: ${appState.dict.loai_giao_bong[k]}</option>`);"""

new_modal = """            const { nhom, ky_thuat, phuong_thuc } = getOldProps(pt, match);
            let techOptions = '';
            Object.keys(appState.dict.ky_thuat_rally).forEach(k => techOptions += `<option value="nhom_ky_thuat|${k}" ${ky_thuat===k?'selected':''}>Kỹ thuật: ${appState.dict.ky_thuat_rally[k]}</option>`);
            Object.keys(appState.dict.loai_giao_bong).forEach(k => techOptions += `<option value="nhom_giao_bong|${k}" ${ky_thuat===k?'selected':''}>Giao bóng: ${appState.dict.loai_giao_bong[k]}</option>`);"""

content = content.replace(old_modal, new_modal)

content = content.replace("window._tempPtPhuongThuc = pt.phuong_thuc;", "window._tempPtPhuongThuc = phuong_thuc;")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
