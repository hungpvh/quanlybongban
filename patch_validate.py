import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_validate = """        function validatePoint(pt) {
            const chi_tiet = pt.chi_tiet_pha_bong;
            if (!chi_tiet) return;
            
            // Validate unused properties are null
            if (chi_tiet.tinh_chat === 'winner') {
                if(chi_tiet.dac_tinh) chi_tiet.dac_tinh.vi_tri_hong = null;
            }
            if (chi_tiet.tinh_chat === 'forced_error' && !chi_tiet.nguoi_kien_tao) {
                // Must have nguoi_kien_tao
                chi_tiet.nguoi_kien_tao = "Unknown";
            }
            if (chi_tiet.tinh_chat === 'unforced_error') {
                chi_tiet.nguoi_kien_tao = null;
                chi_tiet.ky_thuat_kien_tao = null;
            }
        }"""

new_validate = """        function validatePoint(pt) {
            const chi_tiet = pt.chi_tiet_pha_bong;
            if (!chi_tiet) return;
            
            if (chi_tiet.nguoi_ket_thuc === undefined) chi_tiet.nguoi_ket_thuc = null;
            if (chi_tiet.ky_thuat_ket_thuc === undefined) chi_tiet.ky_thuat_ket_thuc = null;
            if (chi_tiet.nguoi_kien_tao === undefined) chi_tiet.nguoi_kien_tao = null;
            if (chi_tiet.ky_thuat_kien_tao === undefined) chi_tiet.ky_thuat_kien_tao = null;
            
            if (!chi_tiet.dac_tinh) chi_tiet.dac_tinh = { diem_roi_ngang: null, do_dai: null, do_xoay: null, vi_tri_hong: null };
            if (chi_tiet.dac_tinh.diem_roi_ngang === undefined) chi_tiet.dac_tinh.diem_roi_ngang = null;
            if (chi_tiet.dac_tinh.do_dai === undefined) chi_tiet.dac_tinh.do_dai = null;
            if (chi_tiet.dac_tinh.do_xoay === undefined) chi_tiet.dac_tinh.do_xoay = null;
            if (chi_tiet.dac_tinh.vi_tri_hong === undefined) chi_tiet.dac_tinh.vi_tri_hong = null;

            // Validate unused properties are null
            if (chi_tiet.tinh_chat === 'winner') {
                chi_tiet.dac_tinh.vi_tri_hong = null;
            }
            if (chi_tiet.tinh_chat === 'forced_error' && !chi_tiet.nguoi_kien_tao) {
                // Must have nguoi_kien_tao
                chi_tiet.nguoi_kien_tao = "Unknown";
            }
            if (chi_tiet.tinh_chat === 'unforced_error') {
                chi_tiet.nguoi_kien_tao = null;
                chi_tiet.ky_thuat_kien_tao = null;
            }
        }"""

content = content.replace(old_validate, new_validate)

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
