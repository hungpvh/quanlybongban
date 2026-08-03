import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_state = r"isLoading: false\s*\};"
new_state = """isLoading: false,
            isSyncing: false
        };"""

content = re.sub(old_state, new_state, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done fixing appstate")
