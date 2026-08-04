import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

target = """    html += `<div class="grid grid-cols-2 gap-4 mb-4">
        <div class="bg-white rounded-xl shadow-sm border p-3">
            <h3 class="text-xs font-bold text-gray-800 text-center mb-2">ĐIỂM RƠI GHI ĐIỂM (THẮNG)</h3>
            <div class="grid grid-cols-3 gap-1 relative bg-blue-100 p-1 border-2 border-blue-300">
                <div class="absolute inset-0 border-b-2 border-dashed border-blue-300 pointer-events-none" style="top: 50%"></div>
                <div class="bg-blue-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Trái</div><div class="font-black text-blue-800">${s.heatmapWinner['ngan_trai']||0}</div></div>
                <div class="bg-blue-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Giữa</div><div class="font-black text-blue-800">${s.heatmapWinner['ngan_giua']||0}</div></div>
                <div class="bg-blue-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Phải</div><div class="font-black text-blue-800">${s.heatmapWinner['ngan_phai']||0}</div></div>
                <div class="bg-blue-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Trái</div><div class="font-black text-blue-900">${s.heatmapWinner['dai_trai']||0}</div></div>
                <div class="bg-blue-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Giữa</div><div class="font-black text-blue-900">${s.heatmapWinner['dai_giua']||0}</div></div>
                <div class="bg-blue-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Phải</div><div class="font-black text-blue-900">${s.heatmapWinner['dai_phai']||0}</div></div>
            </div>
        </div>
        <div class="bg-white rounded-xl shadow-sm border p-3">
            <h3 class="text-xs font-bold text-gray-800 text-center mb-2">ĐIỂM RƠI BỊ MẤT ĐIỂM (THUA)</h3>
            <div class="grid grid-cols-3 gap-1 relative bg-red-100 p-1 border-2 border-red-300">
                <div class="absolute inset-0 border-b-2 border-dashed border-red-300 pointer-events-none" style="top: 50%"></div>
                <div class="bg-red-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Trái</div><div class="font-black text-red-800">${s.heatmapLost['ngan_trai']||0}</div></div>
                <div class="bg-red-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Giữa</div><div class="font-black text-red-800">${s.heatmapLost['ngan_giua']||0}</div></div>
                <div class="bg-red-50/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Ngắn Phải</div><div class="font-black text-red-800">${s.heatmapLost['ngan_phai']||0}</div></div>
                <div class="bg-red-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Trái</div><div class="font-black text-red-900">${s.heatmapLost['dai_trai']||0}</div></div>
                <div class="bg-red-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Giữa</div><div class="font-black text-red-900">${s.heatmapLost['dai_giua']||0}</div></div>
                <div class="bg-red-200/80 p-2 text-center relative z-10"><div class="text-[10px] text-gray-500 mb-1">Dài Phải</div><div class="font-black text-red-900">${s.heatmapLost['dai_phai']||0}</div></div>
            </div>
        </div>
    </div>`;"""

replacement = """
    const getHeatmapCell = (val, total, label, colorType) => {
        const pct = total > 0 ? Math.round((val / total) * 100) : 0;
        let bgStyle = '';
        let textClass = 'text-gray-800';
        if (pct > 0) {
            if (colorType === 'win') {
                // green
                bgStyle = `background-color: rgba(34, 197, 94, ${pct/100 * 0.8 + 0.1});`;
                if (pct > 40) textClass = 'text-white';
            } else {
                // red
                bgStyle = `background-color: rgba(239, 68, 68, ${pct/100 * 0.8 + 0.1});`;
                if (pct > 40) textClass = 'text-white';
            }
        } else {
            bgStyle = `background-color: white;`;
        }
        
        return `<div class="p-2 text-center relative z-10" style="${bgStyle}">
            <div class="text-[10px] opacity-90 mb-1 font-semibold ${textClass}">${label}</div>
            <div class="font-black ${textClass} leading-tight">${val} <span class="text-[10px] font-normal block">(${pct}%)</span></div>
        </div>`;
    };

    html += `<div class="grid grid-cols-2 gap-4 mb-4">
        <div class="bg-white rounded-xl shadow-sm border p-3">
            <h3 class="text-xs font-bold text-gray-800 text-center mb-2 uppercase text-green-700">ĐIỂM RƠI GHI ĐIỂM (THẮNG)</h3>
            <div class="grid grid-cols-3 gap-0.5 relative bg-gray-200 p-0.5 border-2 border-green-300">
                <div class="absolute inset-0 border-b-2 border-dashed border-green-400 pointer-events-none z-20" style="top: 50%"></div>
                ${getHeatmapCell(s.heatmapWinner['dai_phai'] || 0, s.points.win, 'Dài Phải', 'win')}
                ${getHeatmapCell(s.heatmapWinner['dai_giua'] || 0, s.points.win, 'Dài Giữa', 'win')}
                ${getHeatmapCell(s.heatmapWinner['dai_trai'] || 0, s.points.win, 'Dài Trái', 'win')}
                ${getHeatmapCell(s.heatmapWinner['ngan_phai'] || 0, s.points.win, 'Ngắn Phải', 'win')}
                ${getHeatmapCell(s.heatmapWinner['ngan_giua'] || 0, s.points.win, 'Ngắn Giữa', 'win')}
                ${getHeatmapCell(s.heatmapWinner['ngan_trai'] || 0, s.points.win, 'Ngắn Trái', 'win')}
            </div>
        </div>
        <div class="bg-white rounded-xl shadow-sm border p-3">
            <h3 class="text-xs font-bold text-gray-800 text-center mb-2 uppercase text-red-700">ĐIỂM RƠI MẤT ĐIỂM (THUA)</h3>
            <div class="grid grid-cols-3 gap-0.5 relative bg-gray-200 p-0.5 border-2 border-red-300">
                <div class="absolute inset-0 border-b-2 border-dashed border-red-400 pointer-events-none z-20" style="top: 50%"></div>
                ${getHeatmapCell(s.heatmapLost['ngan_trai'] || 0, s.points.lose, 'Ngắn Trái', 'lose')}
                ${getHeatmapCell(s.heatmapLost['ngan_giua'] || 0, s.points.lose, 'Ngắn Giữa', 'lose')}
                ${getHeatmapCell(s.heatmapLost['ngan_phai'] || 0, s.points.lose, 'Ngắn Phải', 'lose')}
                ${getHeatmapCell(s.heatmapLost['dai_trai'] || 0, s.points.lose, 'Dài Trái', 'lose')}
                ${getHeatmapCell(s.heatmapLost['dai_giua'] || 0, s.points.lose, 'Dài Giữa', 'lose')}
                ${getHeatmapCell(s.heatmapLost['dai_phai'] || 0, s.points.lose, 'Dài Phải', 'lose')}
            </div>
        </div>
    </div>`;"""

new_content = content.replace(target, replacement)

if new_content == content:
    print("Failed to replace!")
else:
    with open("/app/applet/index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Success!")

