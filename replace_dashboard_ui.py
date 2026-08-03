import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r"        window\.renderDashboard = function\(container\) \{.*?window\.updateDashboardFilter = function\(\) \{.*?\};", re.DOTALL)

with open("comprehensive_dashboard.js", "r", encoding="utf-8") as f:
    ui_code = f.read()
    
# I need to keep window.updateDashboardFilter
update_filter_code = """
        window.updateDashboardFilter = function() {
            if(!appState.dashboardFilter) return;
            appState.dashboardFilter.matchId = document.getElementById('dbFilterMatch').value;
            appState.dashboardFilter.fromDate = document.getElementById('dbFilterFrom').value;
            appState.dashboardFilter.toDate = document.getElementById('dbFilterTo').value;
            appState.dashboardFilter.loai_hinh = document.getElementById('dbFilterType').value;
            appState.dashboardFilter.doi_thu = document.getElementById('dbFilterOpp').value;
            renderView('dashboard');
        };"""

replacement = ui_code + "\n" + update_filter_code

new_content = pattern.sub(replacement, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

