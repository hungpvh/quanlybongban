import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace switchInputTab and openServeModal with openPointModal
old_funcs = r"""\s*function switchInputTab\(tab\) \{.*?\s*\}\s*function openServeModal\(type\) \{.*?\s*\}"""

new_func = """
        function openPointModal(loai_diem) {
            const isWin = loai_diem === 'thang';
            const titleA = isWin ? "TÔI GHI ĐIỂM" : "TÔI ĐÁNH HỎNG";
            const methodA = isWin ? "toi_ghi_diem" : "toi_danh_hong";
            const titleB = isWin ? "ĐỐI THỦ ĐÁNH HỎNG" : "ĐỐI THỦ GHI ĐIỂM";
            const methodB = isWin ? "doi_thu_danh_hong" : "doi_thu_ghi_diem";

            const techKeys = Object.keys(appState.dict.ky_thuat_rally);
            const serveKeys = Object.keys(appState.dict.loai_giao_bong);
            
            const btnClassA = isWin ? "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100" : "bg-red-50 text-red-700 border-red-200 hover:bg-red-100";
            const btnClassB = isWin ? "bg-green-50 text-green-700 border-green-200 hover:bg-green-100" : "bg-orange-50 text-orange-700 border-orange-200 hover:bg-orange-100";
            
            let htmlA = `<h4 class="font-bold text-sm mb-3 text-center border-b pb-1">${titleA}</h4>`;
            htmlA += `<div class="font-semibold text-xs text-gray-500 mb-2 mt-3 uppercase">Giao bóng</div><div class="grid grid-cols-1 gap-2">`;
            serveKeys.forEach(k => {
                htmlA += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_giao_bong', '${methodA}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassA}">${appState.dict.loai_giao_bong[k]}</button>`;
            });
            htmlA += `</div><div class="font-semibold text-xs text-gray-500 mb-2 mt-4 uppercase">Kỹ thuật</div><div class="grid grid-cols-1 gap-2">`;
            techKeys.forEach(k => {
                htmlA += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_ky_thuat', '${methodA}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassA}">${appState.dict.ky_thuat_rally[k]}</button>`;
            });
            htmlA += `</div>`;

            let htmlB = `<h4 class="font-bold text-sm mb-3 text-center border-b pb-1">${titleB}</h4>`;
            htmlB += `<div class="font-semibold text-xs text-gray-500 mb-2 mt-3 uppercase">Giao bóng</div><div class="grid grid-cols-1 gap-2">`;
            serveKeys.forEach(k => {
                htmlB += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_giao_bong', '${methodB}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassB}">${appState.dict.loai_giao_bong[k]}</button>`;
            });
            htmlB += `</div><div class="font-semibold text-xs text-gray-500 mb-2 mt-4 uppercase">Kỹ thuật</div><div class="grid grid-cols-1 gap-2">`;
            techKeys.forEach(k => {
                htmlB += `<button onclick="addPoint('${loai_diem}', '${k}', 'nhom_ky_thuat', '${methodB}'); closeModal();" class="border rounded-lg p-2 text-xs font-semibold shadow-sm transition ${btnClassB}">${appState.dict.ky_thuat_rally[k]}</button>`;
            });
            htmlB += `</div>`;

            let html = `
                <div class="flex justify-between items-center mb-4 border-b pb-2">
                    <h3 class="text-xl font-black ${isWin?'text-blue-600':'text-red-600'}">${isWin ? 'GHI ĐIỂM' : 'MẤT ĐIỂM'}</h3>
                    <button onclick="closeModal()" class="text-gray-400 hover:text-gray-800"><i class="fas fa-times text-xl"></i></button>
                </div>
                <div class="flex gap-4 max-h-[70vh] overflow-y-auto pb-4">
                    <div class="flex-1">${htmlA}</div>
                    <div class="flex-1 border-l pl-4">${htmlB}</div>
                </div>
            `;
            showModal(html);
        }
"""

content = re.sub(old_funcs, new_func, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
