import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

helpers_code = """
        function getOldProps(pt, m) {
            if (!pt.chi_tiet_pha_bong) return { phuong_thuc: pt.phuong_thuc, nhom: pt.nhom, ky_thuat: pt.ky_thuat };
            const c = pt.chi_tiet_pha_bong;
            const me = m.thong_tin.doi_thu_1 || 'Hungpv';
            const opp = m.thong_tin.doi_thu_2 || 'Doi_thu';
            
            let phuong_thuc = '';
            if (c.tinh_chat === 'winner') {
                phuong_thuc = (c.nguoi_ket_thuc === me) ? 'toi_ghi_diem' : 'doi_thu_ghi_diem';
            } else {
                phuong_thuc = (c.nguoi_ket_thuc === me) ? 'toi_danh_hong' : 'doi_thu_danh_hong';
            }
            
            let ky_thuat = c.ky_thuat_ket_thuc || '';
            let nhom = 'nhom_ky_thuat';
            if (appState.dict && appState.dict.loai_giao_bong && appState.dict.loai_giao_bong[ky_thuat]) {
                nhom = 'nhom_giao_bong';
            }
            return { phuong_thuc, nhom, ky_thuat };
        }

        function setOldProps(pt, loai_diem, ky_thuat, phuong_thuc, m) {
            const me = m.thong_tin.doi_thu_1 || 'Hungpv';
            const opp = m.thong_tin.doi_thu_2 || 'Doi_thu';
            
            let tinh_chat = loai_diem === 'thang' ? 'winner' : 'unforced_error';
            let nguoi_ket_thuc = me;
            
            if (phuong_thuc === 'toi_ghi_diem') {
                tinh_chat = 'winner';
                nguoi_ket_thuc = me;
            } else if (phuong_thuc === 'doi_thu_danh_hong') {
                tinh_chat = 'unforced_error';
                nguoi_ket_thuc = opp;
            } else if (phuong_thuc === 'toi_danh_hong') {
                tinh_chat = 'unforced_error';
                nguoi_ket_thuc = me;
            } else if (phuong_thuc === 'doi_thu_ghi_diem') {
                tinh_chat = 'winner';
                nguoi_ket_thuc = opp;
            }
            
            pt.loai_diem = loai_diem;
            pt.chi_tiet_pha_bong = {
                tinh_chat: tinh_chat,
                nguoi_ket_thuc: nguoi_ket_thuc,
                ky_thuat_ket_thuc: ky_thuat,
                nguoi_kien_tao: null,
                ky_thuat_kien_tao: null,
                dac_tinh: {
                    diem_roi_ngang: null,
                    do_dai: null,
                    do_xoay: null,
                    vi_tri_hong: null
                }
            };
            delete pt.nhom;
            delete pt.ky_thuat;
            delete pt.phuong_thuc;
            
            validatePoint(pt);
        }
"""

content = content.replace("function validatePoint(pt) {", helpers_code + "\n        function validatePoint(pt) {")

with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)

