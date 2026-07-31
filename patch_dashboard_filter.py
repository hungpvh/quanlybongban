import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_code = """function renderDashboard(container) {
    let f = appState.dashboardFilter;
    if (f.matchId === 'all') f = { ...f, matchId: appState.matches[0]?.id_tran_dau || 'all' };"""

new_code = """function renderDashboard(container) {
    if(appState.matches.length === 0) {
        container.innerHTML = `<div class="text-center py-10 text-gray-500">Chưa có dữ liệu thống kê.</div>`;
        return;
    }
    
    if (!appState.dashboardFilter) {
        appState.dashboardFilter = { matchId: appState.currentMatchId || 'all', fromDate: '', toDate: '', loai_hinh: 'all', doi_thu: 'all', _lastMatchId: appState.currentMatchId };
    } else if (appState.currentMatchId !== appState.dashboardFilter._lastMatchId) {
        appState.dashboardFilter.matchId = appState.currentMatchId || 'all';
        appState.dashboardFilter._lastMatchId = appState.currentMatchId;
    }

    let f = appState.dashboardFilter;
    if (f.matchId === 'all' && appState.matches.length > 0) f = { ...f, matchId: appState.matches[0].id_tran_dau };"""

content = content.replace(old_code, new_code)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
