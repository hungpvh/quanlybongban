import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_html = "html += `</div>`;"
new_html = """html += `<div class="col-span-1 sm:col-span-2 text-xs text-gray-400 italic text-right mt-2">* Nếu có nhiều chuỗi dài bằng nhau, chuỗi xuất hiện sớm nhất sẽ được hiển thị.</div></div>`;"""

# Need to make sure we replace the correct one.
# It is just after the if(globalMaxLoseStreakObj) else block.
target_str = """    } else {
        html += `<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 text-center text-gray-400 text-sm flex items-center justify-center">Chưa có chuỗi thua</div>`;
    }
    html += `</div>`;"""

target_repl = """    } else {
        html += `<div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 text-center text-gray-400 text-sm flex items-center justify-center">Chưa có chuỗi thua</div>`;
    }
    html += `<div class="col-span-1 sm:col-span-2 text-xs text-gray-400 italic text-right -mt-2">* Nếu có nhiều chuỗi dài bằng nhau, chuỗi xuất hiện sớm nhất sẽ được hiển thị.</div>`;
    html += `</div>`;"""

content = content.replace(target_str, target_repl)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
