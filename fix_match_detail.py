import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_detail = r"\$\{info\.link_video \? `<a href=\"\$\{escapeHtml\(info\.link_video\)\}\" target=\"_blank\" rel=\"noopener noreferrer\" class=\"text-xs bg-red-100 text-red-600 px-3 py-1\.5 rounded font-medium\"><i class=\"fab fa-youtube\"></i> Xem Video</a>` : ''\}"

new_detail = """${info.link_youtube ? `<a href="${escapeHtml(info.link_youtube)}" target="_blank" rel="noopener noreferrer" class="text-xs bg-red-100 text-red-600 px-3 py-1.5 rounded font-medium"><i class="fab fa-youtube"></i> YouTube</a>` : ''}
                        ${info.link_facebook ? `<a href="${escapeHtml(info.link_facebook)}" target="_blank" rel="noopener noreferrer" class="text-xs bg-blue-100 text-blue-600 px-3 py-1.5 rounded font-medium"><i class="fab fa-facebook"></i> Facebook</a>` : ''}
                        ${info.link_khac ? `<a href="${escapeHtml(info.link_khac)}" target="_blank" rel="noopener noreferrer" class="text-xs bg-gray-100 text-gray-700 px-3 py-1.5 rounded font-medium"><i class="fas fa-link"></i> Link Khác</a>` : ''}"""

content = re.sub(old_detail, new_detail, content)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done detail links")
