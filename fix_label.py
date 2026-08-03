import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("Điểm rơi & Độ dài (Góc nhìn của bạn)", "Điểm rơi & Độ dài (Góc nhìn của người đỡ bóng)")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
