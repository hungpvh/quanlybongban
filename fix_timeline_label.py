import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# We need to replace the timeline item label part.
# I will use a regex to find the section and replace it.
target = r"""\$\{pt\.chi_tiet_pha_bong && pt\.chi_tiet_pha_bong\.dac_tinh && \(pt\.chi_tiet_pha_bong\.dac_tinh\.do_xoay \|\| pt\.chi_tiet_pha_bong\.dac_tinh\.diem_roi_ngang \|\| pt\.chi_tiet_pha_bong\.dac_tinh\.do_dai\) \? \s*`\<br\>\<span class="text-blue-500"\>` \+\s*\["""

replacement = """${pt.chi_tiet_pha_bong && pt.chi_tiet_pha_bong.dac_tinh && (pt.chi_tiet_pha_bong.dac_tinh.do_xoay || pt.chi_tiet_pha_bong.dac_tinh.diem_roi_ngang || pt.chi_tiet_pha_bong.dac_tinh.do_dai) ? 
                                            `<br><span class="text-blue-500 font-medium">` + (pt.chi_tiet_pha_bong.tinh_chat === 'winner' ? 'Thông số đường bóng ghi điểm: ' : 'Thông số đường bóng trước khi đánh hỏng: ') + `</span><span class="text-blue-500">` + 
                                            ["""

new_content = re.sub(target, replacement, content)

if new_content == content:
    print("Failed to replace label!")
else:
    with open("/app/applet/index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Done replacing label!")

