import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_headers_regex = r"const headers = \{.*?'Expires': '0'\s*\};"
new_headers = """const headers = { 
                'Accept': 'application/vnd.github.v3+json', 
                'Authorization': `Bearer ${token}`
            };"""

content = re.sub(old_headers_regex, new_headers, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done fixing githubApi headers")
