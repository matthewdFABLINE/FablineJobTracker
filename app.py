import streamlit as st
import json
import os
from datetime import datetime

# 1. Page Configuration for Structured Layout
st.set_page_config(
    page_title="Fabline Registry - Engineering Archive", 
    page_icon="⚙️", 
    layout="centered"
)

# 2. Engineering Archive Design System (Light Grid Architecture)
st.html("""
<style>
    :root {
        --bg-grid: #f8fafc;
        --panel-white: #ffffff;
        --navy-primary: #1e293b;
        --slate-gray: #475569;
        --border-line: #cbd5e1;
        --highlight-red: #c51f2a;
        
        --status-exp-bg: #f1f5f9;
        --status-exp-txt: #475569;
        --status-inc-bg: #fef2f2;
        --status-inc-txt: #991b1b;
        --status-com-bg: #f0fdf4;
        --status-com-txt: #166534;
    }
    
    /* Main Layout - Engineering Blueprint Paper Background Style */
    .stApp {
        background-color: var(--bg-grid) !important;
        color: var(--navy-primary) !important;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
        font-size: 19px !important;
        background-image: linear-gradient(rgba(71, 85, 105, 0.04) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(71, 85, 105, 0.04) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
    }
    
    /* Font Sizing Accessibility for On-Site Personnel */
    p, label, li, span, div, caption {
        font-size: 19px !important;
    }
    
    /* High-Contrast Formal Input Fields */
    input, select, textarea, div[data-baseweb="select"] {
        font-size: 21px !important;
        background-color: var(--panel-white) !important;
        color: var(--navy-primary) !important;
        border: 2px solid var(--slate-gray) !important;
        border-radius: 6px !important;
    }
    
    /* Formal Engineering Submission Buttons */
    button, div[data-testid="stFormSubmitButton"] button {
        font-size: 21px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        background: linear-gradient(135deg, var(--navy-primary), var(--slate-gray)) !important;
        color: #ffffff !important;
        border: 1px solid var(--navy-primary) !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    button:hover, div[data-testid="stFormSubmitButton"] button:hover {
        filter: brightness(1.1) !important;
    }
    
    /* Structural Blueprint Cards */
    .archive-card {
        background-color: var(--panel-white);
        border: 1px solid var(--border-line);
        border-top: 4px solid var(--navy-primary);
        padding: 22px;
        border-radius: 6px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    /* Clean Title Frameworks */
    h1 { font-size: 38px !important; font-weight: 800 !important; color: var(--navy-primary) !important; letter-spacing: -0.5px; }
    h2 { font-size: 28px !important; font-weight: 700 !important; color: var(--navy-primary) !important; }
    h3 { font-size: 24px !important; font-weight: 700 !important; color: var(--slate-gray) !important; }
    h4 { font-size: 22px !important; font-weight: 700 !important; color: var(--navy-primary) !important; margin: 0; }
    
    /* Technical Status Labels */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 15px !important;
        font-weight: 700;
        text-transform: uppercase;
        border: 1px solid var(--border-line);
    }
    .st-expected { background-color: var(--status-exp-bg); color: var(--status-exp-txt); }
    .st-incomplete { background-color: var(--status-inc-bg); color: var(--status-inc-txt); border-color: #fca5a5; }
    .st-complete { background-color: var(--status-com-bg); color: var(--status-com-txt); border-color: #bbf7d0; }
    
    /* Clean Form Tabs */
    button[data-baseweb="tab"] {
        font-size: 19px !important;
        color: var(--slate-gray) !important;
    }
    button[aria-selected="true"] {
        color: var(--navy-primary) !important;
        font-weight: 700 !important;
    }
</style>
""")

# 3. Secure Verification Layer
def check_password():
    if "authenticated" not in st.session_state: 
        st.session_state["authenticated"] = False
    if st.session_state["authenticated"]: 
        return True
    
    st.title("🔒 SECURITY GATEWAY")
    st.caption("FABLINE CENTRAL ENGINEERING ARCHIVE")
    password_input = st.text_input("ENTER REGISTERED SYSTEM ACCESS CODE:", type="password")
    
    if st.button("INITIALIZE TERMINAL LINK"):
        if password_input == "fabline2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else: 
            st.error("VERIFICATION REJECTED: INVALID KEY ENTRY")
    return False

if not check_password(): 
    st.stop()

# 4. Storage Engine Setup
DB_FILE = "jobs_data.json"
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

if "jobs" not in st.session_state: 
    st.session_state.jobs = load_data()

# 5. Formal System Layout Header & Operational Metrics
st.title("⚙️ FABLINE TECHNICAL REGISTRY")
st.caption("PROCUREMENT ARCHIVE • DATA LOGS ENGINE")

total_rec = len(st.session_state.jobs)
comp_cnt = sum(1 for j in st.session_state.jobs if j.get("status") == "Complete")
incomp_cnt = sum(1 for j in st.session_state.jobs if j.get("status") == "Incomplete")
expected_cnt = sum(1 for j in st.session_state.jobs if j.get("status") == "Expected")

st.html("<div style='margin-bottom: 25px;'></div>")
m1, m2, m3, m4 = st.columns(4)
m1.metric("TOTAL LEDGER", total_rec)
m2.metric("SECURED / COMPLET", comp_cnt)
m3.metric("SHORTFALL BACKLOG", incomp_cnt)
m4.metric("EXPECTED FREIGHT", expected_cnt)

st.markdown("---")

t1, t2, t3 = st.tabs(["📋 MASTER LOG REGISTRY", "➕ ARCHIVE NEW RECORD", "🔬 HISTORICAL INVENTORY ASSISTANT"])

# --- TAB 1: FORMAL DATA REGISTRY VIEW ---
with t1:
    search_q = st.text_input("🔍 FILTERS: Search via Job ID, Site, Client or Component Specifications...")
    filter_status = st.radio("ARCHIVE STATUS SUBSET FILTER:", ["All Statuses", "Expected", "Incomplete", "Complete"], horizontal=True)
    
    filtered = st.session_state.jobs
    if search_q: 
        filtered = [j for j in filtered if search_q.lower() in str(j).lower()]
    if filter_status != "All Statuses": 
        filtered = [j for j in filtered if j.get("status") == filter_status]
    
    if not filtered: 
        st.info("No matching engineering records cataloged within repository memory.")
        
    for idx, job in enumerate(filtered):
        status_lower = str(job['status']).lower()
        st.html(f"""
        <div class="archive-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-line); padding-bottom: 8px; margin-bottom: 14px;">
                <span style="font-size: 22px !important; font-weight: 700; color: var(--navy-primary);">RECORD DEPLOYMENT: #{job['job_no']}</span>
                <span class="status-badge st-{status_lower}">{job['status']}</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 14px;">
                <div>
                    <span style="font-size: 12px !important; color: var(--slate-gray); display: block; font-weight: 700; text-transform: uppercase;">Corporate Account</span>
                    <span style="font-size: 18px !important; font-weight: 600; color: var(--navy-primary);">{job.get('client', 'N/A')}</span>
                </div>
                <div>
                    <span style="font-size: 12px !important; color: var(--slate-gray); display: block; font-weight: 700; text-transform: uppercase;">Target Drop Location</span>
                    <span style="font-size: 18px !important; font-weight: 600; color: var(--navy-primary);">{job.get('site', 'N/A')}</span>
                </div>
            </div>
            <div style="margin-bottom: 14px;">
                <span style="font-size: 12px !important; color: var(--slate-gray); display: block; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Verified Hardware Inventory Sheet</span>
                <div style="background-color: #f8fafc; padding: 12px; border-radius: 4px; border: 1px solid var(--border-line); font-family: monospace; font-size: 16px !important; white-space: pre-wrap; color: var(--navy-primary);">{job.get('items_logged', 'No cargo logs documented.')}</div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 13px !important; color: var(--slate-gray); border-top: 1px dashed var(--border-line); padding-top: 8px;">
                <span>LOG CONTROLLER: <b style="color: var(--navy-primary);">{job.get('operator', 'Default System')}</b></span>
                <span>REGISTRY STAMP: {job['updated']}</span>
            </div>
        </div>
        """)
        
        with st.expander(f"📝 APPEND PROCUREMENT UPDATE - RECORD #{job['job_no']}"):
            with st.form(f"up_{idx}"):
                st.markdown("**LOG COMPONENT FREIGHT UPDATES**")
                new_st = st.selectbox("RE-ASSIGN LOG VALUE MATCH:", ["Expected", "Incomplete", "Complete"], index=["Expected", "Incomplete", "Complete"].index(job['status']) if job['status'] in ["Expected", "Incomplete", "Complete"] else 0)
                new_txt = st.text_area("APPEND MANIFEST LINE (Will index chronologically below):", placeholder="e.g., [Freight Update]: 4x 150mm gate valves arrived.")
                if st.form_submit_button("COMMIT MODIFICATIONS TO LOG"):
                    if not up_op.strip(): 
                        st.error("CRITICAL AUDIT ERROR: Logging officer signature token required.")
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
                        st.success("ARCHIVE SYNCHRONIZED: Refreshing tracking ledger...")
                        st.rerun()
        st.html("<div style='margin-bottom: 20px;'></div>")

# --- TAB 2: ARCHIVE NEW RECORD PANEL ---
with t2:
    st.subheader("➕ COMMIT INITIAL REQUISITION INDEX ENTRY")
    st.markdown("Ensure freight bills and loading slips line items tally fully before submitting entry points.")
    
    with st.form("new_form", clear_on_submit=True):
        j_no = st.text_input("JOB ACCESSION ID / PURCHASE ORDER MANIFEST KEY:")
        clnt = st.text_input("CLIENT BUSINESS DESIGNATION:")
        stloc = st.text_input("TARGET FIELD SITE DESTINATION:")
        stch = st.selectbox("INITIAL FREIGHT TRACK PROFILE:", ["Expected", "Incomplete", "Complete"])
        itm_log = st.text_area("INVENTORY RECEIPT LINE ITEMS MANIFEST:", placeholder="e.g., 10x 100mm grooved elbows\n2x butterfly valves")
        op_name = st.text_input("AUTHORIZING OFFICER AUDIT SIGNATURE:")
        
        if st.form_submit_button("SAVE REQUISITION RECORD TO PERMANENT REGISTRY"):
            if j_no and clnt and op_name:
                new_entry = {
                    "job_no": j_no, 
                    "client": clnt, 
                    "site": stloc, 
                    "status": stch,
                    "items_logged": itm_log if itm_log.strip() else "No hardware documented at registry entry.",
                    "operator": op_name.strip(), 
                    "updated": datetime.now().strftime("%d-%b-%Y %H:%M")
                }
                st.session_state.jobs.insert(0, new_entry)
                save_data(st.session_state.jobs)
                st.success("⚡ DATA ACCESSION INTEGRATION COMPLETE: File mapped onto core database grid.")
                st.rerun()
            else: 
                st.error("REGISTRATION TERMINATED: Requisition ID, Client Profile, and Authorizing Officer signature string are mandatory.")

# --- TAB 3: STRUCTURED TECHNICAL LOOKUP ---
with t3:
    st.subheader("🔬 SYSTEM ACCESSION LOOKUP & HISTORICAL INVENTORY SEARCH")
    st.markdown("Query the processing index to track movement data history, component deployment times, and logistics signatures.")
    
    query = st.text_input("🔍 INPUT INVENTORY QUERY PARAMETERS (e.g., '100mm grooved' or worker initials):")
    
    if query:
        matches = [j for j in st.session_state.jobs if query.lower() in str(j).lower()]
        
        with st.chat_message("assistant"):
            st.markdown("### 📡 TECHNICAL INDEX RETRIEVAL STATUS REPORT")
            
            if not matches:
                st.warning(f"No records containing match criteria for tracking string '{query}' were identified inside this system archive file.")
            else:
                total_matches = len(matches)
                completed_matches = sum(1 for m in matches if m['status'] == 'Complete')
                pending_matches = total_matches - completed_matches
                
                st.success(f"Parsing Complete. Located {total_matches} tracking entries matching target criteria string.")
                
                st.markdown(f"""
                **Accession Data Summary Profile:**
                * **Discovered System Matches:** {total_matches} documents pulled.
                * **Verification Profile Split:** {completed_matches} records validated as **Complete / Delivered**, {pending_matches} items currently remain **Incomplete / Awaiting Actions**.
                """)
                
                st.markdown("#### DETAILED ENTRY MANIFEST HISTORY RECORDS:")
                
                for index, item in enumerate(matches):
                    st.markdown(f"""
                    ---
                    ### 📂 TRANSACTION ARCHIVE FILE {index + 1}: LOG FILE #{item['job_no']}
                    * **Tracking State Code:** `{item['status']}`
                    * **Corporate Client Account:** **{item.get('client', 'N/A')}**
                    * **Deployment Site Destination Location:** *{item.get('site', 'N/A')}*
                    * **Transaction Registry Stamping:** Updated on **{item['updated']}** by Logging Officer **{item.get('operator', 'Unassigned')}**
                    
                    **Hardware Line Manifest History:**
                    """)
                    st.code(item.get('items_logged', 'No manifest data cataloged.'))
