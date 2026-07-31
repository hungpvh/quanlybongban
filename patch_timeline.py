import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove let inputTab = 'thang';
content = re.sub(r"let inputTab = 'thang';\n", "", content)

# Rewrite renderGameTimeline's UI
old_timeline_ui = r"""\$\{isLocked \? `\s*<div class="px-4 py-3 bg-gray-50 flex gap-2 justify-center border-t">.*?` \: `\s*<div class="flex border-t">.*?</div>\s*`\}\s*</div>\s*<div class="\$\{isLocked \? 'mt-24' : 'mt-44'\} mb-4">\s*`;\s*if\(!isLocked\) \{\s*html \+= `<div class="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-6">`;\s*// Nút giao bóng 2 lớp\s*if\(inputTab==='thang'\) \{.*?\}\s*// Nút Kỹ thuật\s*techKeys\.forEach\(k => \{.*?\s*\}\);\s*html \+= `</div>`;\s*\}"""

new_timeline_ui = """${isLocked ? `
                        <div class="px-4 py-3 bg-gray-50 flex gap-2 justify-center border-t">
                            <button onclick="toggleGameLock()" class="bg-gray-200 text-gray-800 px-4 py-1.5 rounded-full text-sm font-medium hover:bg-gray-300 transition"><i class="fas fa-unlock"></i> Mở lại game</button>
                        </div>
                    ` : ''}
                </div>
                
                <div class="${isLocked ? 'mt-24' : 'mt-24'} mb-4">
            `;
            
            if(!isLocked) {
                html += `<div class="flex gap-4 mb-6">`;
                html += `<button onclick="openPointModal('thang')" class="flex-1 bg-blue-600 text-white rounded-xl p-4 font-bold text-lg hover:bg-blue-700 transition shadow-sm flex flex-col items-center justify-center gap-1"><i class="fas fa-plus-circle text-2xl mb-1"></i> ĐIỂM THẮNG</button>`;
                html += `<button onclick="openPointModal('thua')" class="flex-1 bg-yellow-500 text-white rounded-xl p-4 font-bold text-lg hover:bg-yellow-600 transition shadow-sm flex flex-col items-center justify-center gap-1"><i class="fas fa-minus-circle text-2xl mb-1"></i> ĐIỂM THUA</button>`;
                html += `</div>`;
            }"""

content = re.sub(old_timeline_ui, new_timeline_ui, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
