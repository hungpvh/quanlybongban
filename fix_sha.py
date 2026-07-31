import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_func = """        async function saveToGithub() {
            if (appState.isMock) { showToast('Đã lưu cục bộ (Chế độ mẫu).', 'success'); renderView(appState.view); return; }
            try {
                showToast('Đang đồng bộ lên GitHub...', 'info');
                // Lấy sha mới nhất để tránh xung đột
                const currentRes = await githubApi('GET', appState.github.dataPath).catch(e => null);
                if (currentRes && currentRes.sha && currentRes.sha !== appState.github.sha) {
                    throw new Error('Dữ liệu trên GitHub đã bị thay đổi (xung đột SHA). Vui lòng tải lại trang!');
                }
                
                const content = b64EncodeUnicode(JSON.stringify(appState.matches, null, 2));
                const body = { message: 'Update matches', content, branch: appState.github.branch };
                if (currentRes && currentRes.sha) body.sha = currentRes.sha;
                
                const res = await githubApi('PUT', appState.github.dataPath, body);
                appState.github.sha = res.content.sha;
                showToast('Đã đồng bộ GitHub thành công!', 'success');
            } catch (e) {
                console.error(e);
                showToast('Lỗi đồng bộ: ' + (e.message || 'Unknown'), 'error');
                alert('Lỗi đồng bộ: ' + e.message);
            }
            renderView(appState.view);
        }"""

new_func = """        async function saveToGithub() {
            if (appState.isMock) { showToast('Đã lưu cục bộ (Chế độ mẫu).', 'success'); renderView(appState.view); return; }
            try {
                showToast('Đang đồng bộ lên GitHub...', 'info');
                
                // Luôn ngầm thực hiện một lệnh GET để xin lại mã SHA mới nhất từ GitHub
                const currentRes = await githubApi('GET', appState.github.dataPath).catch(e => null);
                let latestSha = appState.github.sha;
                if (currentRes && currentRes.sha) {
                    latestSha = currentRes.sha;
                }
                
                const content = b64EncodeUnicode(JSON.stringify(appState.matches, null, 2));
                const body = { message: 'Update matches', content, branch: appState.github.branch };
                if (latestSha) {
                    body.sha = latestSha;
                }
                
                const res = await githubApi('PUT', appState.github.dataPath, body);
                appState.github.sha = res.content.sha;
                showToast('Đã đồng bộ GitHub thành công!', 'success');
            } catch (e) {
                console.error(e);
                showToast('Lỗi đồng bộ: ' + (e.message || 'Unknown'), 'error');
                alert('Lỗi đồng bộ: ' + e.message);
            }
            renderView(appState.view);
        }"""

content = content.replace(old_func, new_func)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)

