import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace githubApi function
old_block_regex = r"async function githubApi\(method, path, body = null\) \{.*?return res\.json\(\);\s*\}"

new_block = """async function githubApi(method, path, body = null) {
            const { user, repo, branch, token } = appState.github;
            const url = new URL(`https://api.github.com/repos/${user}/${repo}/contents/${path}`);
            if (method === 'GET') {
                if (branch) url.searchParams.append('ref', branch);
            }
            // Add cache buster for all requests just to be safe
            url.searchParams.append('t', Date.now());

            const headers = { 
                'Accept': 'application/vnd.github.v3+json', 
                'Authorization': `Bearer ${token}`,
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            };
            const options = { method, headers, cache: 'no-cache' };
            if (body) options.body = JSON.stringify(body);
            const res = await fetch(url.toString(), options);
            if (!res.ok) throw new Error(await res.text());
            return res.json();
        }"""

content = re.sub(old_block_regex, new_block, content, flags=re.DOTALL)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done fixing githubApi")
