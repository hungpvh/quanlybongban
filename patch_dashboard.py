import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# I will find the block to replace using regex
pattern = re.compile(r"        // --- DASHBOARD ---.*?window\.updateDashboardFilter = function\(\) \{.*?\};\n", re.DOTALL)

with open("new_dashboard_logic.js", "r", encoding="utf-8") as f:
    logic_code = f.read()

with open("new_dashboard_ui.js", "r", encoding="utf-8") as f:
    ui_code = f.read()
    
replacement = "        // --- DASHBOARD ---\n" + logic_code + "\n" + ui_code

new_content = pattern.sub(replacement, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

