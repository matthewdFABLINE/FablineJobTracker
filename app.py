import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="Fabline Job Tracker", page_icon="⚙️", layout="centered")

def check_password():
    if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
    if st.session_state["authenticated"]: return True
    st.markdown("## 🔒 Fabline Job Tracker\n### Secure Operations Portal Access")
    password_input = st.text_input("Enter Corporate Access Password:", type="password")
    if st.button("Authenticate"):
        if password_input == "fabline2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else: st.error("❌ Invalid credentials. System access denied.")
    return False

if not check_password(): st.stop()

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

with st.container(border=True):
    st.markdown("### ⚙️ FABLINE OPERATIONS PORTAL\n### MATERIALS LOG & HISTORICAL AUDIT ENGINE")
    total_rec = len(st.session_state.jobs)
    comp_cnt = sum(1 for j in st.session_state.jobs if j.get("status") == "Complete")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Jobs", total_rec)
    m2.metric("Completed", comp_cnt)
    m3.metric("Awaiting", total_rec - comp_cnt)

t1, t2, t3 = st.tabs(["📋 Database Inventory", "➕ Register New Record", "🤖 AI Operations Assistant"])

with t1:
    search_q = st.text_input("🔍 Search master registry (Job #, Site, Client, Staff, or Parts)...")
    filter_status = st.radio("Display Status:", ["All Statuses", "Expected", "Incomplete", "Complete"], horizontal=True)
    filtered = st.session_state.jobs
    if search_q: filtered = [j for j in filtered if search_q.lower() in str(j).lower()]
    if filter_status != "All Statuses": filtered = [j for j in filtered if j.get("status") == filter_status]
    
    if not filtered: st.info("No matching historical records located.")
    for idx, job in enumerate(filtered):
        emoji = {"Expected": "⏳", "Incomplete": "⚠️", "Complete": "✅"}.get(job['status'], "📦")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            c1.markdown(f"#### JOB REF: #{job['job_no']}")
            c2.markdown(f"**Status:** `{emoji} {job['status']}`")
            m1, m2 = st.columns(2)
            m1.markdown(f"🏢 **Client:** {job.get('client', 'N/A')}")
            m2.markdown(f"📍 **Site:** {job.get('site', 'N/A')}")
            st.caption("📦 RECEIVED MATERIALS & LINE ITEMS LOG")
            st.info(job.get('items_logged', 'No item logs detailed.'))
            f1, f2 = st.columns(2)
            f1.markdown(f"👤 **Staff:** `{job.get('operator', 'Unassigned')}`")
            f2.markdown(f"⏱️ `{job['updated']}`")
            
            with st.expander(f"⚙️ Action Menu - Update Job #{job['job_no']}"):
                with st.form(f"up_{idx}"):
                    new_st = st.selectbox("Update Status", ["Expected", "Incomplete", "Complete"], index=["Expected", "Incomplete", "Complete"].index(job['status']) if job['status'] in ["Expected", "Incomplete", "Complete"] else 0)
                    new_txt = st.text_area("Append new materials received:")
                    up_op = st.text_input("Staff Signature Verification")
                    if st.form_submit_button("Save Updates"):
                        if not up_op.strip(): st.error("Staff Signature required.")
                        else:
                            for r_job in st.session_state.jobs:
                                if r_job['job_no'] == job['job_no']:
                                    r_job['status'] = new_st
                                    r_job['operator'] = up_op.strip()
                                    r_job['updated'] = datetime.now().strftime("%d-%b-%Y %H:%M")
                                    if new_txt.strip():
                                        r_job['items_logged'] = r_job.get('items_logged', '') + f"\n[{datetime.now().strftime('%d-%b-%Y %H:%M')} by {up_op.strip()}]: " + new_txt.strip()
                                    break
                            save_data(st.session_state.jobs)
                            st.success("Updated successfully!")
                            st.rerun()

with t2:
    st.subheader("Log Formal Procurement Entry")
    with st.form("new_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        j_no = col1.text_input("Job / PO Number")
        clnt = col1.text_input("Client Designation")
        stloc = col2.text_input("Target Site Location")
        stch = col2.selectbox("Initial Status", ["Expected", "Incomplete", "Complete"])
        itm_log = st.text_area("Materials Log details (Items received)")
        op_name = st.text_input("Staff Signature / Name")
        if st.form_submit_button("Commit Entry to Database"):
            if j_no and clnt and op_name:
                new_entry = {
                    "job_no": j_no, "client": clnt, "site": stloc, "status": stch,
                    "items_logged": itm_log if itm_log.strip() else "No materials documented.",
                    "operator": op_name.strip(), "updated": datetime.now().strftime("%d-%b-%Y %H:%M")
                }
                st.session_state.jobs.insert(0, new_entry)
                save_data(st.session_state.jobs)
                st.success("✅ Entry committed successfully!")
                st.rerun()
            else: st.error("Please fill in Job Number, Client Name, and Staff Signature.")

with t3:
    st.subheader("📋 Operations Intelligence & Audit Engine")
    query = st.text_input("💬 Ask about an asset, part size, staff member, or timeline:")
    if query:
        matches = [j for j in st.session_state.jobs if query.lower() in str(j).lower()]
        if not matches: st.warning(f"No entry matching '{query}' found.")
        else:
            st.success(f"Found {len(matches)} historical references:")
            for item in matches:
                with st.chat_message("assistant"):
                    st.markdown(f"**Job #{item['job_no']}** ({item['status']})\nUpdate: {item['updated']} | Site: {item.get('site', 'N/A')}\n**Activity Log:**")
                    st.code(item.get('items_logged', ''))
                    st.caption(f"Sign-off Controller: {item.get('operator', 'Unassigned')}")
