import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_func = """        async function githubApi(method, path, body = null) {
            const { user, repo, branch, token } = appState.github;
            const url = `https://api.github.com/repos/${user}/${repo}/contents/${path}${method==='GET'?`?ref=${branch}`:''}`;
            const headers = { 'Accept': 'application/vnd.github.v3+json', 'Authorization': `Bearer ${token}` };
            const options = { method, headers };
            if (body) options.body = JSON.stringify(body);
            const res = await fetch(url, options);
            if (!res.ok) throw new Error(await res.text());
            return res.json();
        }"""

new_func = """        async function githubApi(method, path, body = null) {
            const { user, repo, branch, token } = appState.github;
            // Thêm timestamp để tránh cache từ trình duyệt (hoặc dùng cache: 'no-store')
            const cacheBuster = method === 'GET' ? `&t=${Date.now()}` : '';
            const url = `https://api.github.com/repos/${user}/${repo}/contents/${path}${method==='GET'?`?ref=${branch}${cacheBuster}`:''}`;
            const headers = { 'Accept': 'application/vnd.github.v3+json', 'Authorization': `Bearer ${token}` };
            const options = { method, headers, cache: 'no-store' };
            if (body) options.body = JSON.stringify(body);
            const res = await fetch(url, options);
            if (!res.ok) throw new Error(await res.text());
            return res.json();
        }"""

content = content.replace(old_func, new_func)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
