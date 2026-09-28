import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Set up the mobile-responsive webpage layout
st.set_page_config(page_title="Fabline Job Tracker", page_icon="⚙️", layout="centered")

# --- CUSTOM CSS (Keeps your exact design style) ---
st.markdown("""
<style>
    body { background-color: #eff0f2; color: #1c2026; }
    .main-title { font-size: 24px; font-weight: 700; color: #292e35; margin-bottom: 2px; }
    .subtitle { font-size: 14px; color: #666a6e; margin-bottom: 20px; }
    .card { background: white; padding: 16px; border-radius: 14px; border: 1px solid #d8dadd; margin-bottom: 14px; box-shadow: 0 2px 10px rgba(41,46,53,.1); }
    .status-tag { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: 12px; font-weight: 700; }
    .status-expected { background: #e3e5e8; color: #3a4049; }
    .status-complete { background: #d5efe0; color: #1f7a4d; }
    .status-incomplete { background: #f8dcd9; color: #b3261e; }
</style>
""", unsafe_allow_value=True)

# --- PASSWORD PROTECTION LAYER ---
def check_password():
    """Returns True if the user entered the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    # Display clean login screen
    st.markdown("<div class='main-title'>🔒 Fabline Job Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Restricted Corporate Access</div>", unsafe_allow_html=True)
    
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
st.markdown("<div class='main-title'>⚙️ Fabline Job Tracker</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Live · Authenticated Staff</div>", unsafe_allow_html=True)

# Navigation Navigation Tabs
tab1, tab2 = st.tabs(["📋 View Jobs", "➕ Log New Job"])

with tab1:
    # Filter controls matching your design
    search_q = st.text_input("🔍 Search job no., site, client, pipe/valve...")
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
        for index, job in enumerate(filtered_jobs):
            status_class = f"status-{job['status'].lower()}"
            st.markdown(f"""
            <div class='card'>
                <h3>🛠️ Job #{job['job_no']}</h3>
                <p><b>Client:</b> {job['client']} | <b>Site:</b> {job['site']}</p>
                <span class='status-tag {status_class}'>{job['status']}</span>
                <p style='font-size:12px; color:gray; margin-top:8px;'>Updated: {job['updated']}</p>
            </div>
            """, unsafe_allow_html=True)

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
