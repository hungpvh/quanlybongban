import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update appState.github
state_target = "github: { user: '', repo: '', branch: 'main', dataPath: 'dulieubongban.json', dictPath: 'tu_dien_bong_ban.json', token: '', sha: null, dictSha: null },"
state_replacement = "github: { user: '', repo: '', codeBranch: 'main', dataBranch: 'data', dataPath: 'dulieubongban.json', dictPath: 'tu_dien_bong_ban.json', token: '', sha: null, dictSha: null },"
content = content.replace(state_target, state_replacement)

# 2. Update loadGithubConfig
load_target = """        async function loadGithubConfig() {
            const stored = localStorage.getItem('bongban_gh_config');
            if (stored) {
                appState.github = { ...appState.github, ...JSON.parse(stored) };
                if (appState.github.token && appState.github.user && appState.github.repo) {
                    await fetchGithubData();
                    return;
                }
            }
            useMockData();
        }"""
load_replacement = """        async function loadGithubConfig() {
            const stored = localStorage.getItem('bongban_gh_config');
            if (stored) {
                const parsed = JSON.parse(stored);
                parsed.codeBranch = parsed.codeBranch || parsed.branch || 'main';
                parsed.dataBranch = parsed.dataBranch || 'data';
                appState.github = { ...appState.github, ...parsed };
                if (appState.github.token && appState.github.user && appState.github.repo) {
                    await fetchGithubData();
                    return;
                }
            }
            useMockData();
        }"""
content = content.replace(load_target, load_replacement)

# 3. Update githubApi
api_target = """        async function githubApi(method, path, body = null) {
            const { user, repo, branch, token } = appState.github;
            const url = new URL(`https://api.github.com/repos/${user}/${repo}/contents/${path}`);
            if (method === 'GET') {
                if (branch) url.searchParams.append('ref', branch);
            }"""
api_replacement = """        async function githubApi(method, path, body = null) {
            const { user, repo, dataBranch, token } = appState.github;
            const branchToUse = dataBranch || 'data';
            const url = new URL(`https://api.github.com/repos/${user}/${repo}/contents/${path}`);
            if (method === 'GET') {
                url.searchParams.append('ref', branchToUse);
            }"""
content = content.replace(api_target, api_replacement)

# 4. Update saveToGithub
save_target = """                const body = { message: 'Update matches', content, branch: appState.github.branch };"""
save_replacement = """                const body = { message: 'Update matches', content, branch: appState.github.dataBranch || 'data' };"""
content = content.replace(save_target, save_replacement)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Config and API updated.")
