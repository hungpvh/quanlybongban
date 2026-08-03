import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update calculateDashboardStats to take perspective
old_calc_func = r"function calculateDashboardStats\(filteredMatches\) \{(.*?)\s+if \(gWins > gLoses\) mWins\+\+; else if \(gLoses > gWins\) mLoses\+\+;\s*s\.gameSummary\.push\(\{"
match = re.search(old_calc_func, content, flags=re.DOTALL)
if not match:
    print("Could not find calculateDashboardStats")
    exit(1)

body = match.group(1)
# modify body:
# const me = m.thong_tin.doi_thu_1; 
# to
# const me = perspective === 'doi_thu_1' ? m.thong_tin.doi_thu_1 : m.thong_tin.doi_thu_2;
# const isWin = pt.loai_diem === 'thang';
# to
# const isWin = perspective === 'doi_thu_1' ? pt.loai_diem === 'thang' : pt.loai_diem === 'thua';

new_body = body.replace(
    "const me = m.thong_tin.doi_thu_1;",
    "const me = perspective === 'doi_thu_1' ? m.thong_tin.doi_thu_1 : m.thong_tin.doi_thu_2;"
)
new_body = new_body.replace(
    "const isWin = pt.loai_diem === 'thang';",
    "const isWin = perspective === 'doi_thu_1' ? pt.loai_diem === 'thang' : pt.loai_diem === 'thua';"
)

new_calc_func = f"function calculateDashboardStats(filteredMatches, perspective = 'doi_thu_1') {{{new_body}\n            if (gWins > gLoses) mWins++; else if (gLoses > gWins) mLoses++;\n            \n            s.gameSummary.push({{"

content = content.replace(match.group(0), new_calc_func)


# 2. Update renderDashboard to use perspective
# We need to add a segmented control.
# And also add a default perspective logic.

old_render_dash = """    if(appState.matches.length === 0) {
        container.innerHTML = `<div class="text-center py-10 text-gray-500">Chưa có dữ liệu thống kê.</div>`;
        return;
    }
    
    if (!appState.dashboardFilter) {"""

new_render_dash = """    if(appState.matches.length === 0) {
        container.innerHTML = `<div class="text-center py-10 text-gray-500">Chưa có dữ liệu thống kê.</div>`;
        return;
    }
    
    if (!appState.dashboardPerspective) {
        appState.dashboardPerspective = 'doi_thu_1';
    }
    
    if (!appState.dashboardFilter) {"""

content = content.replace(old_render_dash, new_render_dash)

# 3. Add segmented control to html
old_html_start = """    let oppOpts = `<option value="all">Tất cả</option>`;
    [...new Set(appState.matches.map(m=>m.thong_tin.doi_thu_2))].forEach(o => oppOpts += `<option value="${o}" ${f.doi_thu===o?'selected':''}>${o}</option>`);

    let html = `
        <div class="fixed top-14 left-0 right-0 z-10 bg-white border-b px-4 py-3 shadow-sm">
            <div class="max-w-3xl mx-auto flex gap-2 overflow-x-auto no-scrollbar items-center">
                <select id="dbFilterMatch" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[120px]">${matchOpts}</select>"""

# Find current names for perspective labels
# We can get names based on filtered match, or just use generic. The prompt says: "Trên đầu Dashboard hiển thị rõ: Đang phân tích theo góc nhìn: Đối thủ 1 (Hungpv) hoặc Đối thủ 2 (Nguyễn Văn A) Tên lấy từ thông tin trận đấu."
# So let's get the names from the first filtered match, or from all matches if no specific match is selected. Wait, if matchId == 'all', what name to show?
# We can use "Mình" and "Đối thủ" if matchId is all, or get from the first match.
# Let's extract the names.
new_html_start = """    let oppOpts = `<option value="all">Tất cả</option>`;
    [...new Set(appState.matches.map(m=>m.thong_tin.doi_thu_2))].forEach(o => oppOpts += `<option value="${o}" ${f.doi_thu===o?'selected':''}>${o}</option>`);
    
    let name1 = 'Đối thủ 1';
    let name2 = 'Đối thủ 2';
    if (filteredMatches.length > 0) {
        name1 = filteredMatches[0].thong_tin.doi_thu_1 || 'Đối thủ 1';
        // If filtering by specific opponent, use that opponent's name, otherwise use the first one's opponent
        name2 = f.doi_thu !== 'all' ? f.doi_thu : (filteredMatches[0].thong_tin.doi_thu_2 || 'Đối thủ 2');
    }

    let html = `
        <div class="fixed top-14 left-0 right-0 z-10 bg-white border-b px-4 py-3 shadow-sm flex flex-col gap-3">
            <div class="max-w-3xl mx-auto flex gap-2 w-full">
                <button onclick="updateDashboardPerspective('doi_thu_1')" class="flex-1 py-1.5 text-sm font-bold rounded-lg transition ${appState.dashboardPerspective === 'doi_thu_1' ? 'bg-blue-600 text-white shadow-sm' : 'bg-gray-100 text-gray-600'}">Đối thủ 1</button>
                <button onclick="updateDashboardPerspective('doi_thu_2')" class="flex-1 py-1.5 text-sm font-bold rounded-lg transition ${appState.dashboardPerspective === 'doi_thu_2' ? 'bg-blue-600 text-white shadow-sm' : 'bg-gray-100 text-gray-600'}">Đối thủ 2</button>
            </div>
            <div class="text-center text-xs font-semibold text-gray-700">Đang phân tích theo góc nhìn: <span class="text-blue-600">${appState.dashboardPerspective === 'doi_thu_1' ? name1 : name2}</span></div>
            <div class="max-w-3xl mx-auto flex gap-2 overflow-x-auto no-scrollbar items-center">
                <select id="dbFilterMatch" onchange="updateDashboardFilter()" class="border rounded p-1.5 text-xs bg-gray-50 min-w-[120px]">${matchOpts}</select>"""

content = content.replace(old_html_start, new_html_start)

# 4. update margin top in renderDashboard
# From `<div class="mt-32 px-4 max-w-3xl mx-auto space-y-6 pb-20">` to `<div class="mt-40 px-4 max-w-3xl mx-auto space-y-6 pb-20">`
content = content.replace('<div class="mt-32 px-4 max-w-3xl mx-auto space-y-6 pb-20">', '<div class="mt-44 px-4 max-w-3xl mx-auto space-y-6 pb-20">')

# 5. Update call to calculateDashboardStats
content = content.replace("const s = calculateDashboardStats(filteredMatches);", "const s = calculateDashboardStats(filteredMatches, appState.dashboardPerspective);")

# 6. Global function updateDashboardPerspective
new_func = """        window.updateDashboardPerspective = function(pers) {
            appState.dashboardPerspective = pers;
            renderView('dashboard');
        };
        
        window.updateDashboardFilter = function() {"""

content = content.replace("window.updateDashboardFilter = function() {", new_func)
if "window.updateDashboardPerspective" not in content:
    # If updateDashboardFilter is not defined as window.updateDashboardFilter, let's inject it before loadGithubConfig
    inj = """
        window.updateDashboardPerspective = function(pers) {
            appState.dashboardPerspective = pers;
            renderView('dashboard');
        };
        
        window.updateDashboardFilter = function() {
            appState.dashboardFilter = {
                matchId: document.getElementById('dbFilterMatch').value,
                fromDate: document.getElementById('dbFilterFrom').value,
                toDate: document.getElementById('dbFilterTo').value,
                loai_hinh: document.getElementById('dbFilterType').value,
                doi_thu: document.getElementById('dbFilterOpp').value,
                _lastMatchId: document.getElementById('dbFilterMatch').value
            };
            appState.currentMatchId = appState.dashboardFilter.matchId === 'all' ? null : appState.dashboardFilter.matchId;
            renderView('dashboard');
        };
"""
    content = content.replace("// --- INIT ---", inj + "\n        // --- INIT ---")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
