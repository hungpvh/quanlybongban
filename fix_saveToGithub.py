import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_func = r"async function saveToGithub\(\) \{\s*if \(appState\.isMock\) \{ showToast\('Đã lưu cục bộ \(Chế độ mẫu\)\.', 'success'\); renderView\(appState\.view\); return; \}\s*try \{"
new_func = """async function saveToGithub() {
            if (appState.isMock) { showToast('Đã lưu cục bộ (Chế độ mẫu).', 'success'); renderView(appState.view); return; }
            if (appState.isSyncing) return;
            appState.isSyncing = true;
            try {"""

content = re.sub(old_func, new_func, content)

old_catch = r"\} catch \(e\) \{\s*console\.error\(e\);\s*showToast\('Lỗi đồng bộ: ' \+ \(e\.message \|\| 'Unknown'\), 'error'\);\s*alert\('Lỗi đồng bộ: ' \+ e\.message\);\s*\}\s*renderView\(appState\.view\);\s*\}"
new_catch = """} catch (e) {
                console.error(e);
                showToast('Lỗi đồng bộ: ' + (e.message || 'Unknown'), 'error');
                alert('Lỗi đồng bộ: ' + e.message);
            } finally {
                appState.isSyncing = false;
            }
            renderView(appState.view);
        }"""

content = re.sub(old_catch, new_catch, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done fixing saveToGithub")
