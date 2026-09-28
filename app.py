import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="Fabline Hub", page_icon="⚙️", layout="centered")

# FIXED: Explicitly declared the string content variable to prevent Streamlit TypeError layout crashes
css_style = """<style>
:root{--bg:#000;--card:#1F2421;--red:#C51F2A;--orange:#ff6a00;--txt:#fff;}
.stApp{background:var(--bg)!important;color:var(--txt)!important;font-size:19px!important;border:2px solid var(--orange);box-shadow:inset 0 0 30px rgba(255,106,0,.15);margin:5px;border-radius:12px;}
p,label,li,span,div{font-size:19px!important;}
input,select,textarea,div[data-baseweb='select']{font-size:22px!important;background:var(--bg)!important;color:var(--txt)!important;border:2px solid var(--red)!important;border-radius:8px!important;}
button,div[data-testid='stFormSubmitButton'] button{font-size:22px!important;font-weight:800!important;text-transform:uppercase!important;background:linear-gradient(135deg,var(--red),#801016)!important;color:#fff!important;border:1px solid var(--orange)!important;border-radius:8px!important;padding:14px 28px!important;width:100%!important;}
.cyber-card{background:var(--card);border-left:6px solid var(--red);padding:24px;border-radius:8px;margin-bottom:20px;}
h1{font-size:42px!important;font-weight:900!important;color:var(--txt)!important;text-transform:uppercase;}
h2{font-size:32px!important;}h3{font-size:26px!important;color:var(--orange)!important;}h4{font-size:23px!important;margin:0;}
.status-pill{display:inline-block;padding:6px 16px;border-radius:4px;font-size:16px!important;font-weight:900;text-transform:uppercase;}
.st-expected{background:#2b2b1a;color:#ffcc00;border:1px solid #ffcc00;}
.st-incomplete{background:#3a1618;color:#ff4d4d;border:1px solid #ff4d4d;}
.st-complete{background:#122b18;color:#33cc66;border:1px solid #33cc66;}
button[data-baseweb='tab']{font-size:20px!important;color:#a4b3a9!important;}
button[aria-selected='true']{color:var(--orange)!important;}
</style>"""
st.markdown(css_style, unsafe_html=True)

if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if not st.session_state["authenticated"]:
    st.markdown("<h1>🔒 SYSTEM LOCK</h1>", unsafe_html=True)
    password_input = st.text_input("ENTER ACCESS KEY:", type="password")
    if st.button("INITIALIZE INTERFACE"):
        if password_input == "fabline2026": 
            st.session_state["authenticated"] = True
            st.rerun()
        else: st.error("ACCESS DENIED")
    st.stop()

DB_FILE = "jobs_data.json"
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

if "jobs" not in st.session_state: st.session_state.jobs = load_data()

st.markdown("<h1>⚙️ FABLINE CORE</h1><p style='color:#ff6a00;font-weight:bold;letter-spacing:1.5px;margin-top:-15px;'>PROCUREMENT MONITOR</p>", unsafe_html=True)
total_rec = len(st.session_state.jobs)

m1, m2, m3, m4 = st.columns(4)
m1.metric("TOTAL REGISTRY", total_rec)
m2.metric("READY", sum(1 for j in st.session_state.jobs if j.get("status") == "Complete"))
m3.metric("SHORTFALLS", sum(1 for j in st.session_state.jobs if j.get("status") == "Incomplete"))
m4.metric("EXPECTED", sum(1 for j in st.session_state.jobs if j.get("status") == "Expected"))

t1, t2, t3 = st.tabs(["📋 MANIFEST REGISTRY", "➕ INITIALIZE RECORD", "🤖 COGNITIVE AUDIT ASSISTANT"])

with t1:
    search_q = st.text_input("🔍 SCAN REGISTRY KEYS...")
    filter_status = st.radio("SORT DATASET:", ["All Statuses", "Expected", "Incomplete", "Complete"], horizontal=True)
    filtered = st.session_state.jobs
    if search_q: filtered = [j for j in filtered if search_q.lower() in str(j).lower()]
    if filter_status != "All Statuses": filtered = [j for j in filtered if j.get("status") == filter_status]
    
    for idx, job in enumerate(filtered):
        st.markdown(f"<div class='cyber-card'><div style='display:flex;justify-content:space-between;'><span><b>JOB: #{job['job_no']}</b></span><span class='status-pill st-{str(job['status']).lower()}'>{job['status']}</span></div><br><div>🏢 <b>Client:</b> {job.get('client','N/A')} | 📍 <b>Site:</b> {job.get('site','N/A')}</div><br><div style='background:#000;padding:10px;color:#33cc66;font-family:monospace;'>{job.get('items_logged','No logs.')}</div><br><small>👤 {job.get('operator','System')} | ⏱️ {job['updated']}</small></div>", unsafe_html=True)
        with st.expander(f"🛠️ ACTION PANEL #{job['job_no']}"):
            with st.form(f"up_{idx}"):
                new_st = st.selectbox("STATUS OVERRIDE:", ["Expected", "Incomplete", "Complete"], index=["Expected", "Incomplete", "Complete"].index(job['status']) if job['status'] in ["Expected", "Incomplete", "Complete"] else 0)
                new_txt = st.text_area("APPEND INVENTORY LINE:")
                up_op = st.text_input("OPERATOR INITIALS:")
                if st.form_submit_button("COMMIT MODIFICATIONS"):
                    if not up_op.strip(): st.error("Operator signature missing.")
                    else:
                        for r_job in st.session_state.jobs:
                            if r_job['job_no'] == job['job_no']:
                                r_job['status'] = new_st
                                r_job['operator'] = up_op.strip()
                                r_job['updated'] = datetime.now().strftime("%d-%b-%Y %H:%M")
                                if new_txt.strip(): r_job['items_logged'] = r_job.get('items_logged', '') + f"\n[{datetime.now().strftime('%d-%b-%Y %H:%M')} by {up_op.strip()}]: " + new_txt.strip()
                        save_data(st.session_state.jobs)
                        st.success("UPDATED")
                        st.rerun()

with t2:
    st.markdown("<h2>➕ REGISTER RECORD</h2>", unsafe_html=True)
    with st.form("new_form", clear_on_submit=True):
        j_no, clnt = st.text_input("JOB / PO REF:"), st.text_input("CLIENT NAME:")
        stloc, stch = st.text_input("TARGET SITE LOCATION:"), st.selectbox("INITIAL STATUS:", ["Expected", "Incomplete", "Complete"])
        itm_log, op_name = st.text_area("INVENTORY MANIFEST DETAILS:"), st.text_input("AUTHORIZING OPERATOR:")
        if st.form_submit_button("COMMIT ENTRY TO DATABASE"):
            if j_no and clnt and op_name:
                st.session_state.jobs.insert(0, {"job_no": j_no, "client": clnt, "site": stloc, "status": stch, "items_logged": itm_log if itm_log.strip() else "No hardware documented.", "operator": op_name.strip(), "updated": datetime.now().strftime("%d-%b-%Y %H:%M")})
                save_data(st.session_state.jobs)
                st.success("⚡ REGISTERED")
                st.rerun()
            else: st.error("Missing required fields.")

with t3:
    st.markdown("<h2>🤖 COGNITIVE AUDIT CENTER</h2>", unsafe_html=True)
    query = st.text_input("💬 COMMAND INPUT:")
    if query:
        matches = [j for j in st.session_state.jobs if query.lower() in str(j).lower()]
        with st.chat_message("assistant"):
            if not matches: st.markdown(f"No records matching **'{query}'** exist.")
            else:
                st.markdown(f"#### STATUS: {len(matches)} MEMORY LOGS PARSED FOR '{query.upper()}'\n* Total Matches: {len(matches)}\n* Completed: {sum(1 for m in matches if m['status'] == 'Complete')}")
                for index, item in enumerate(matches):
                    st.markdown(f"---\n### 📂 TRANSACTION {index + 1}: JOB #{item['job_no']} (`{item['status']}`)\n* Client: **{item.get('client','N/A')}** | Site: *{item.get('site','N/A')}*\n* Verified by: **{item.get('operator','System')}** on {item['updated']}\n**Manifest:**")
                    st.code(item.get('items_logged', ''))
