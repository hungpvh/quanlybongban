import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_heatmap = r"""    const rHeatmap = \(data, title, colClass\) => \{
        const total = Object.values\(data\).reduce\(\(a,b\)=>a\+b,0\) \|\| 1;
        const cell = \(k\) => \{
            const c = data\[k\]\|\|0; const pct = Math.round\(c/total\*100\);
            return `<div class="border p-2 flex flex-col items-center justify-center h-20 \$\{c>0\?colClass:'bg-gray-50'\} relative"><div class="absolute inset-0 bg-current opacity-\$\{Math.min\(pct\*2, 100\)\}"></div><span class="relative z-10 font-bold text-lg">\$\{c\}</span><span class="relative z-10 text-\[10px\] font-semibold">\$\{pct\}%</span></div>`;
        \};"""

new_heatmap = """    const rHeatmap = (data, title, overlayColorClass) => {
        const total = Object.values(data).reduce((a,b)=>a+b,0) || 1;
        const cell = (k) => {
            const c = data[k]||0; const pct = Math.round(c/total*100);
            const textColor = c > 0 ? (pct > 40 ? 'text-white' : 'text-gray-900') : 'text-gray-400';
            const overlayOp = c > 0 ? (pct / 100).toFixed(2) : '0';
            return `<div class="border p-2 flex flex-col items-center justify-center h-20 bg-gray-50 relative overflow-hidden"><div class="absolute inset-0 ${overlayColorClass}" style="opacity: ${overlayOp}"></div><span class="relative z-10 font-bold text-lg ${textColor}">${c}</span><span class="relative z-10 text-[10px] font-semibold ${textColor}">${pct}%</span></div>`;
        };"""

content = re.sub(old_heatmap, new_heatmap, content)

# I need to change how rHeatmap is called
# old: ${rHeatmap(s.heatmapWinner, 'GHI ĐIỂM (WINNER)', 'bg-blue-200 text-blue-900')}
# old: ${rHeatmap(s.heatmapLost, 'MẤT ĐIỂM (LỖI)', 'bg-red-200 text-red-900')}
# new: ${rHeatmap(s.heatmapWinner, 'GHI ĐIỂM (WINNER)', 'bg-blue-600')}
# new: ${rHeatmap(s.heatmapLost, 'MẤT ĐIỂM (LỖI)', 'bg-red-600')}
content = content.replace("'bg-blue-200 text-blue-900'", "'bg-blue-600'")
content = content.replace("'bg-red-200 text-red-900'", "'bg-red-600'")


with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
