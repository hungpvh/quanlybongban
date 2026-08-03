import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('"link_video": ""', '"link_youtube": "", "link_facebook": "", "link_khac": ""')

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done mock")
