import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace calculateDashboardStats
old_calc_func = r"function calculateDashboardStats\(filteredMatches\) \{(.*?)\s+if \(gWins > gLoses\) mWins\+\+; else if \(gLoses > gWins\) mLoses\+\+;"
match = re.search(old_calc_func, content, flags=re.DOTALL)
if not match:
    print("Could not find calculateDashboardStats")

