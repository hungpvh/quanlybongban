import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("appState.matches = JSON.parse(b64DecodeUnicode(dataRes.content));", 
"""appState.matches = JSON.parse(b64DecodeUnicode(dataRes.content));
                    migrateOldSchema();""")

content = content.replace("appState.matches = JSON.parse(JSON.stringify(MOCK_MATCHES));",
"""appState.matches = JSON.parse(JSON.stringify(MOCK_MATCHES));
            migrateOldSchema();""")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
