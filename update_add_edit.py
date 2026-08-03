import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update addPoint
old_add = """            game.danh_sach_diem.push({
                thu_tu_diem: game.danh_sach_diem.length + 1,
                ty_so_hien_tai: '', // calculated below
                loai_diem: loai_diem,
                nhom: nhom,
                ky_thuat: ky_thuat,
                phuong_thuc: phuong_thuc,
                nguoi_giao_bong: '' // calculated below
            });"""

new_add = """            const newPt = {
                thu_tu_diem: game.danh_sach_diem.length + 1,
                ty_so_hien_tai: '',
                loai_diem: loai_diem,
                nguoi_giao_bong: ''
            };
            setOldProps(newPt, loai_diem, ky_thuat, phuong_thuc, match);
            game.danh_sach_diem.push(newPt);"""

content = content.replace(old_add, new_add)

# Update handleEditPoint
old_edit = """            pt.loai_diem = loai;
            pt.phuong_thuc = ptPhuongThuc;
            pt.nhom = ktVal[0];
            pt.ky_thuat = ktVal[1];"""

new_edit = """            setOldProps(pt, loai, ktVal[1], ptPhuongThuc, match);"""

content = content.replace(old_edit, new_edit)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)

