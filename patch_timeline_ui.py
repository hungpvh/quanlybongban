import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update timeline UI
old_timeline_pts = r"""\s*const isWin = pt\.loai_diem === 'thang';\s*const name = pt\.nhom === 'nhom_giao_bong' \? appState\.dict\.loai_giao_bong\[pt\.ky_thuat\] : appState\.dict\.ky_thuat_rally\[pt\.ky_thuat\];\s*html \+= `\s*<div class="bg-white p-3 rounded-lg border \$\{isWin\?'border-blue-200 border-l-4 border-l-blue-500':'border-yellow-300 border-l-4 border-l-yellow-500'\} shadow-sm flex items-center justify-between text-sm">\s*<div class="flex items-center gap-3">\s*<div class="font-black w-10 text-center \$\{isWin\?'text-blue-600':'text-yellow-600'\}">\$\{pt\.ty_so_hien_tai\}</div>\s*<div>\s*<div class="font-bold text-gray-800">\$\{name\}</div>\s*<div class="text-xs text-gray-500">Giao: \$\{pt\.nguoi_giao_bong\} &bull; #\$\{pt\.thu_tu_diem\}</div>\s*</div>\s*</div>"""

new_timeline_pts = """                    const isWin = pt.loai_diem === 'thang';
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
                            </div>"""

content = re.sub(old_timeline_pts, new_timeline_pts, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
