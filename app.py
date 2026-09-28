import streamlit as st
import json
import os
from datetime import datetime

# Set up the mobile webpage layout
st.set_page_config(page_title="Fabline Job Tracker", page_icon="⚙️", layout="centered")

# --- PASSWORD PROTECTION LAYER ---
def check_password():
    """Returns True if the user entered the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    # Display clean login screen
    st.markdown("## 🔒 Fabline Job Tracker")
    st.markdown("### Restricted Corporate Access")
    
    password_input = st.text_input("Enter Company Password:", type="password")
    
    # Change "fabline2026" to whatever password you want your team to use
    if st.button("Log In"):
        if password_input == "fabline2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Incorrect password. Access denied.")
    return False

# Stop execution if password is wrong
if not check_password():
    st.stop()

# --- DATA STORAGE ENGINE ---
DB_FILE = "jobs_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load existing jobs
if "jobs" not in st.session_state:
    st.session_state.jobs = load_data()

# --- APP INTERFACE & LOGIC ---
st.markdown("# ⚙️ Fabline Job Tracker")
st.markdown("#### Live · Authenticated Staff")

# Navigation Tabs
tab1, tab2 = st.tabs(["📋 View Jobs", "➕ Log New Job"])

with tab1:
    # Filter controls matching your design
    search_q = st.text_input("🔍 Search job no., site, client...")
    filter_status = st.radio("Filter Status:", ["All", "Expected", "Incomplete", "Complete"], horizontal=True)
    
    filtered_jobs = st.session_state.jobs
    
    # Apply search filter
    if search_q:
        filtered_jobs = [j for j in filtered_jobs if search_q.lower() in str(j).lower()]
        
    # Apply status filter
    if filter_status != "All":
        filtered_jobs = [j for j in filtered_jobs if j.get("status") == filter_status]

    # Display Jobs List
    if not filtered_jobs:
        st.info("No matching jobs found.")
    else:
        for job in filtered_jobs:
            with st.container(border=True):
                st.markdown(f"### 🛠️ Job #{job['job_no']}")
                st.write(f"**Client:** {job['client']} | **Site:** {job['site']}")
                st.write(f"**Status:** `{job['status']}`")
                st.caption(f"Updated: {job['updated']}")

with tab2:
    st.subheader("Log a New Tracker Entry")
    with st.form("new_job_form", clear_on_submit=True):
        job_no = st.text_input("Job Number")
        client = st.text_input("Client Name")
        site = st.text_input("Site Location")
        status_choice = st.selectbox("Initial Status", ["Expected", "Incomplete", "Complete"])
        
        submitted = st.form_submit_button("Save Job Entry")
        if submitted:
            if job_no and client:
                new_entry = {
                    "job_no": job_no,
                    "client": client,
                    "site": site,
                    "status": status_choice,
                    "updated": datetime.now().strftime("%d-%b-%Y %H:%M")
                }
                st.session_state.jobs.insert(0, new_entry)
                save_data(st.session_state.jobs)
                st.success("✅ Job logged successfully!")
                st.rerun()
            else:
                st.error("Please fill in both the Job Number and Client Name.")
