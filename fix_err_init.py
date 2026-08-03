import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_err_check = r"if \(s\.errorLocation\[dac_tinh\.vi_tri_hong\] !== undefined\) \{"
new_err_check = """if (s.errorLocation[dac_tinh.vi_tri_hong] === undefined) s.errorLocation[dac_tinh.vi_tri_hong] = 0;
                        if (true) {"""
content = re.sub(old_err_check, new_err_check, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
