import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_xoay = r"\$\{\['xuong', 'long', 'len'\]\.map\(x =>"
new_xoay = "${Object.keys(appState.dict.thuoc_tinh_bong.do_xoay).map(x =>"
content = re.sub(old_xoay, new_xoay, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
