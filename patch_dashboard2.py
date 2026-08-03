import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the block starting with "// --- DASHBOARD ---" up to "// --- SETTINGS ---"
pattern = re.compile(r"        // --- DASHBOARD ---.*?// --- SETTINGS ---", re.DOTALL)

with open("new_dashboard_logic.js", "r", encoding="utf-8") as f:
    logic_code = f.read()

with open("comprehensive_dashboard.js", "r", encoding="utf-8") as f:
    ui_code = f.read()
    
# I need to keep updateDashboardFilter inside ui_code, it's already there
# But wait, comprehensive_dashboard.js has window.renderDashboard and window.updateDashboardFilter.
# I should just paste it as is.
replacement_ui = ui_code.replace("window.renderDashboard = function(container)", "function renderDashboard(container)")
replacement_ui = replacement_ui.replace("window.updateDashboardFilter = function()", "function updateDashboardFilter()")

replacement = "        // --- DASHBOARD ---\n" + logic_code + "\n" + replacement_ui + "\n\n        // --- SETTINGS ---"

# Need to inject Assist HTML before Heatmap
assist_html = """
    // Assist
    const allAssist = Object.keys(s.assistTech).sort((a,b)=>s.assistTech[b].totalAssist - s.assistTech[a].totalAssist).filter(k => s.assistTech[k].totalAssist > 0);
    html += `<div class="bg-white rounded-xl shadow-sm border p-4 mb-4"><h3 class="font-bold text-gray-800 border-b pb-2 mb-3">HIỆU QUẢ KIẾN TẠO (ASSIST)</h3>`;
    if(allAssist.length>0) {
        allAssist.forEach(k => {
            const obj = s.assistTech[k];
            html += `
                <div class="py-3 border-b last:border-0">
                    <div class="flex justify-between items-center mb-2">
                        <span class="font-bold text-sm text-gray-800">${getName(k)}</span>
                        <span class="text-xs text-gray-500">${obj.totalAssist} lần kiến tạo</span>
                    </div>
                    <div class="flex gap-2">
                        <div class="flex-1 bg-gray-50 border rounded p-2 text-center">
                            <div class="text-[10px] text-gray-500 uppercase font-bold mb-1">Chuyển hóa Winner</div>
                            <div class="font-black text-green-600">${toPct(obj.winner, obj.totalAssist)}%</div>
                        </div>
                        <div class="flex-1 bg-gray-50 border rounded p-2 text-center">
                            <div class="text-[10px] text-gray-500 uppercase font-bold mb-1">Tỷ lệ Ép lỗi</div>
                            <div class="font-black text-blue-600">${toPct(obj.forcedErrorOpponent, obj.totalAssist)}%</div>
                        </div>
                    </div>
                </div>
            `;
        });
    } else {
        html += `<div class="text-sm text-gray-500">Chưa có dữ liệu kiến tạo.</div>`;
    }
    html += `</div>`;

    // Heatmap
"""

replacement = replacement.replace("    // Heatmap\n", assist_html)


new_content = pattern.sub(replacement, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

