import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_headers = r"const headers = \{ 'Accept': 'application/vnd\.github\.v3\+json', 'Authorization': `Bearer \$\{token\}` \};"
new_headers = """const headers = { 
                'Accept': 'application/vnd.github.v3+json', 
                'Authorization': `Bearer ${token}`,
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            };"""

content = re.sub(old_headers, new_headers, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done headers")
