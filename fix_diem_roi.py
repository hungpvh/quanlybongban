import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update renderDiemRoi in ptEntryForm to have "Dài" above "Ngắn"
old_render_diem_roi = """            const renderDiemRoi = () => {
                const isWin = s.loai_diem === 'thang';
                const cols = isWin ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
                return `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Điểm rơi & Độ dài (Góc nhìn của bạn)</label>
                    <div class="grid grid-cols-3 gap-2">
                        ${cols.map(col => `
                            <div class="flex flex-col gap-2">
                                <button onclick="updateDiemRoi('${col}', 'ngan')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='ngan')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Ngắn<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                                <button onclick="updateDiemRoi('${col}', 'dai')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='dai')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Dài<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `};"""

new_render_diem_roi = """            const renderDiemRoi = () => {
                const isWin = s.loai_diem === 'thang';
                const cols = isWin ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
                return `
                <div class="mb-5">
                    <label class="block text-sm font-black text-gray-800 mb-2">Điểm rơi & Độ dài (Góc nhìn của bạn)</label>
                    <div class="grid grid-cols-3 gap-2">
                        ${cols.map(col => `
                            <div class="flex flex-col gap-2">
                                <button onclick="updateDiemRoi('${col}', 'dai')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='dai')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Dài<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                                <button onclick="updateDiemRoi('${col}', 'ngan')" class="p-3 rounded-xl font-bold text-xs border transition ${(s.dac_tinh.diem_roi_ngang===col && s.dac_tinh.do_dai==='ngan')?'bg-blue-600 text-white border-blue-600 shadow-md':'bg-white text-gray-700 border-gray-300 shadow-sm'}">Ngắn<br>${col==='trai'?'Trái':col==='giua'?'Giữa':'Phải'}</button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `};"""

content = content.replace(old_render_diem_roi, new_render_diem_roi)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
