import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(">Forced Error<", ">Ép đối thủ đánh hỏng<")
content = content.replace(">Unforced Error<", ">Bị ép nên tự đánh hỏng<")
content = content.replace(">Forced<", ">Ép hỏng<")
content = content.replace(">Unforced<", ">Tự hỏng<")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
