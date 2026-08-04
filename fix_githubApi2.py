import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_options = r"const options = \{ method, headers, cache: 'no-cache' \};"
new_options = """const options = { method, headers, cache: 'no-store' };"""

content = re.sub(old_options, new_options, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done fixing options")
