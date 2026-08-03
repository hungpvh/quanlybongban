import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_rheatmap = """    const rHeatmap = (data, title, overlayColorClass, reverseCols = false, reverseRows = false) => {
        const total = Object.values(data).reduce((a,b)=>a+b,0) || 1;
        const cell = (k) => {
            const c = data[k]||0; const pct = Math.round(c/total*100);
            const textColor = c > 0 ? (pct > 40 ? 'text-white' : 'text-gray-900') : 'text-gray-400';
            const overlayOp = c > 0 ? (pct / 100).toFixed(2) : '0';
            return `<div class="border p-2 flex flex-col items-center justify-center h-20 bg-gray-50 relative overflow-hidden"><div class="absolute inset-0 ${overlayColorClass}" style="opacity: ${overlayOp}"></div><span class="relative z-10 font-bold text-lg ${textColor}">${c}</span><span class="relative z-10 text-[10px] font-semibold ${textColor}">${pct}%</span></div>`;
        };
        const cols = reverseCols ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
        const row1 = reverseRows ? `${cell('ngan_' + cols[0])}${cell('ngan_' + cols[1])}${cell('ngan_' + cols[2])}` : `${cell('dai_' + cols[0])}${cell('dai_' + cols[1])}${cell('dai_' + cols[2])}`;
        const row2 = reverseRows ? `${cell('dai_' + cols[0])}${cell('dai_' + cols[1])}${cell('dai_' + cols[2])}` : `${cell('ngan_' + cols[0])}${cell('ngan_' + cols[1])}${cell('ngan_' + cols[2])}`;
        return `
            <div class="flex-1">
                <div class="text-xs font-bold text-center mb-2 uppercase text-gray-600">${title}</div>
                <div class="grid grid-cols-3 gap-0.5 border bg-gray-200">
                    ${row1}
                    ${row2}
                </div>
                <div class="flex justify-between text-[10px] text-gray-500 mt-1 px-1">
                    <span>${cols[0]==='trai'?'Trái':'Phải'}</span>
                    <span>Giữa</span>
                    <span>${cols[2]==='trai'?'Trái':'Phải'}</span>
                </div>
            </div>
        `;
    };"""

new_rheatmap = """    const rHeatmap = (data, title, overlayColorClass, reverseCols = false, reverseRows = false) => {
        const total = Object.values(data).reduce((a,b)=>a+b,0) || 1;
        const cell = (k) => {
            const c = data[k]||0; const pct = Math.round(c/total*100);
            const textColor = c > 0 ? (pct > 40 ? 'text-white' : 'text-gray-900') : 'text-gray-400';
            const overlayOp = c > 0 ? (pct / 100).toFixed(2) : '0';
            return `<div class="border p-2 flex flex-col items-center justify-center h-20 bg-gray-50 relative overflow-hidden"><div class="absolute inset-0 ${overlayColorClass}" style="opacity: ${overlayOp}"></div><span class="relative z-10 font-bold text-lg ${textColor}">${c}</span><span class="relative z-10 text-[10px] font-semibold ${textColor}">${pct}%</span></div>`;
        };
        const cols = reverseCols ? ['phai', 'giua', 'trai'] : ['trai', 'giua', 'phai'];
        const row1 = reverseRows ? `${cell('ngan_' + cols[0])}${cell('ngan_' + cols[1])}${cell('ngan_' + cols[2])}` : `${cell('dai_' + cols[0])}${cell('dai_' + cols[1])}${cell('dai_' + cols[2])}`;
        const row2 = reverseRows ? `${cell('dai_' + cols[0])}${cell('dai_' + cols[1])}${cell('dai_' + cols[2])}` : `${cell('ngan_' + cols[0])}${cell('ngan_' + cols[1])}${cell('ngan_' + cols[2])}`;
        
        const labelRow1 = reverseRows ? 'Ngắn' : 'Dài';
        const labelRow2 = reverseRows ? 'Dài' : 'Ngắn';
        
        return `
            <div class="flex-1 flex flex-col items-center">
                <div class="text-xs font-bold text-center mb-2 uppercase text-gray-600">${title}</div>
                <div class="flex items-stretch">
                    <div class="flex flex-col justify-around text-[10px] text-gray-500 font-bold mr-1">
                        <div style="writing-mode: vertical-rl; transform: rotate(180deg);" class="flex-1 flex items-center justify-center">${labelRow1}</div>
                        <div style="writing-mode: vertical-rl; transform: rotate(180deg);" class="flex-1 flex items-center justify-center">${labelRow2}</div>
                    </div>
                    <div class="flex-1">
                        <div class="grid grid-cols-3 gap-0.5 border bg-gray-200">
                            ${row1}
                            ${row2}
                        </div>
                        <div class="flex justify-between text-[10px] text-gray-500 mt-1 px-1 font-bold">
                            <span>${cols[0]==='trai'?'Trái':'Phải'}</span>
                            <span>Giữa</span>
                            <span>${cols[2]==='trai'?'Trái':'Phải'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    };"""

content = content.replace(old_rheatmap, new_rheatmap)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
