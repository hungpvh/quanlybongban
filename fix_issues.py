import re

with open("/app/applet/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update initPtState to preserve isEdit and editIdx
init_pt_state_pattern = re.compile(r"window\.initPtState = function\(loai_diem, tinh_chat, defaultNguoiKetThuc\) \{(.*?)\}", re.DOTALL)
def replace_init(m):
    old_body = m.group(1)
    new_body = """
            const isEdit = window.ptEntryState ? window.ptEntryState.isEdit : false;
            const editIdx = window.ptEntryState ? window.ptEntryState.editIdx : undefined;
            window.ptEntryState = {
                isEdit,
                editIdx,
                loai_diem: loai_diem,
                tinh_chat: tinh_chat,
                nguoi_ket_thuc: defaultNguoiKetThuc,
                ky_thuat_ket_thuc: '',
                nguoi_kien_tao: '',
                ky_thuat_kien_tao: '',
                dac_tinh: { do_xoay: '', diem_roi_ngang: '', do_dai: '', vi_tri_hong: '' }
            };
            renderPtEntryForm();
    """
    return f"window.initPtState = function(loai_diem, tinh_chat, defaultNguoiKetThuc) {{{new_body}}}"
content = init_pt_state_pattern.sub(replace_init, content)


# 2. Update renderPtEntryForm to preserve scroll position
# find: let html = `<div class="max-h-[70vh] overflow-y-auto no-scrollbar pb-6 px-1">
# replace with let html = `<div id="pt-entry-scroll" class="max-h-[70vh] overflow-y-auto no-scrollbar pb-6 px-1">
content = content.replace('let html = `<div class="max-h-[70vh] overflow-y-auto no-scrollbar pb-6 px-1">', 'let html = `<div id="pt-entry-scroll" class="max-h-[70vh] overflow-y-auto no-scrollbar pb-6 px-1">')

# inject scroll saving at start of renderPtEntryForm
render_pt_entry_pattern = re.compile(r"window\.renderPtEntryForm = function\(\) \{\s*const s = window\.ptEntryState;")
content = render_pt_entry_pattern.sub("window.renderPtEntryForm = function() { let currentScroll = 0; const scrollEl = document.getElementById('pt-entry-scroll'); if (scrollEl) currentScroll = scrollEl.scrollTop; const s = window.ptEntryState;", content)

# inject scroll restoring after showModal(html);
content = content.replace("showModal(html);\n        }", """showModal(html);
            setTimeout(() => {
                const newScrollEl = document.getElementById('pt-entry-scroll');
                if (newScrollEl) newScrollEl.scrollTop = currentScroll;
            }, 0);
        }""")


# 3. Update savePtEntry to handle editing
save_pt_entry_pattern = re.compile(r"window\.savePtEntry = async function\(\) \{(.*?)game\.danh_sach_diem\.push\(newPt\);(.*?)\}", re.DOTALL)
def replace_save(m):
    first_part = m.group(1)
    # The first part contains validation and `const newPt = ... validatePoint(newPt);`
    # We will just rewrite this section completely.
    return m.group(0) # We won't use regex for this, too complex
content = content # no-op here


with open("/app/applet/index.html", "w", encoding="utf-8") as f:
    f.write(content)
