import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("if (f.matchId === 'all' && appState.matches.length > 0) f = { ...f, matchId: appState.matches[0].id_tran_dau };", "")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
