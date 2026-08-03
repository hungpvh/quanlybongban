import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix spin initialization in calculateDashboardStats
old_spin_init = r"spin: \{ xuong: \{ total: 0, win: 0, forcedError: 0 \}, len: \{ total: 0, win: 0, forcedError: 0 \}, long: \{ total: 0, win: 0, forcedError: 0 \} \},"
new_spin_init = "spin: {},"
content = re.sub(old_spin_init, new_spin_init, content)

old_err_init = r"errorLocation: \{ ruc_luoi: 0, ra_ngoai_dai: 0, ra_ngoai_bien: 0, truot_bong: 0 \}"
new_err_init = "errorLocation: {}"
content = re.sub(old_err_init, new_err_init, content)

old_spin_check = r"if \(dac_tinh\.do_xoay && s\.spin\[dac_tinh\.do_xoay\]\) \{"
new_spin_check = """if (dac_tinh.do_xoay) {
                        if (!s.spin[dac_tinh.do_xoay]) s.spin[dac_tinh.do_xoay] = { total: 0, win: 0, forcedError: 0 };"""
content = re.sub(old_spin_check, new_spin_check, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
