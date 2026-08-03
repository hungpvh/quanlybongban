import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace openPointModal
old_modal = r"\s*function openPointModal\(loai_diem\).*?let htmlB =.*?htmlB \+= `</div>`;\s*"

# I will use a more precise regex or simple string replacement.
