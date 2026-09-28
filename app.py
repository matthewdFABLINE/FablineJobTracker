import streamlit as st
import json
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Fabline Hub - Cyber Procurement", 
    page_icon="⚙️", 
    layout="centered"
)

# 2. Cyberpunk Accent Styling Layer
st.html("""
<style>
    :root {
        --bg-deep: #000000;
        --card-bg: #1F2421;
        --brand-red: #C51F2A;
        --neon-orange: #ff6a00;
        --text-bright: #ffffff;
        --text-mute: #a4b3a9;
    }
    
    .stApp {
        background-color: var(--bg-deep) !important;
        color: var(--text-bright) !important;
        font-size: 19px !important;
        border: 2px solid var(--neon-orange);
        box-shadow: inset 0 0 30px rgba(255, 106, 0, 0.15);
        margin: 5px;
        border-radius: 12px;
    }
    
    p, label, li, span, div, caption {
        font-size: 19px !important;
    }
    
    input, select, textarea, div[data-baseweb="select"] {
        font-size: 22px !important;
        background-color: var(--bg-deep) !important;
        color: var(--text-bright) !important;
        border: 2px solid var(--brand-red) !important;
        border-radius: 8px !important;
    }
    
    button, div[data-testid="stFormSubmitButton"] button {
        font-size: 22px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        background: linear-gradient(135deg, var(--brand-red), #801016) !important;
        color: #ffffff !important;
        border: 1px solid var(--neon-orange) !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        box-shadow: 0 0 15px rgba(197, 31, 42, 0.4) !important;
        width: 100% !important;
    }
    
    .cyber-card {
        background-color: var(--card-bg);
        border-left: 6px solid var(--brand-red);
        border-top: 1px solid #343d38;
        border-right: 1px solid #343d38;
        border-bottom: 1px solid #343d38;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    h1 { font-size: 42px !important; font-weight: 900 !important; color: var(--text-bright) !important; text-transform: uppercase; letter-spacing: 2px; }
    h2 { font-size: 32px !important; font-weight: 800 !important; color: var(--text-bright) !important; }
    h3 { font-size: 26px !important; font-weight: 700 !important; color: var(--neon-orange) !important; }
    h4 { font-size: 23px !important; font-weight: 700 !important; color: var(--text-bright) !important; margin: 0; }
    
    .status-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 4px;
        font-size: 16px !important;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .st-expected { background-color: #2b2b1a; color: #ffcc00; border: 1px solid #ffcc00; }
    .st-incomplete { background-color: #3a1618; color: #ff4d4d; border: 1px solid #ff4d4d; }
    .st-complete { background-color: #122b18; color: #33cc66; border: 1px solid #33cc66; }
    
    button[data-baseweb="tab"] {
        font-size: 20px !important;
        color: var(--text-mute) !important;
    }
    button[aria-selected="true"] {
        color: var(--neon-orange) !important;
        font-weight: bold !important;
    }
</style>
""")

# 3. Secure Password Layer with Fixed Indentation & Spacing
def check_password():
    if "authenticated" not in st.session_state: 
        st.session_state["authenticated"] = False
    if st.session_state["authenticated"]: 
        return True
    
    st.title("🔒 SYSTEM LOCK")
    st.caption("RESTRICTED FABLINE INTERFACE")
    password_input = st.text_input("ENTER ACCESS KEY PASSCODE:", type="password")
    
    if st.button("INITIALIZE INTERFACE"):
        if password_input == "fabline2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else: 
            st.error("ACCESS DENIED: INVALID DATA ENTRY TOKEN")
    return False

if not check_password(): 
    st.stop()

# 4. Flat-File Data Storage Management
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

# 5. Core Interface Heading & Statistics Panel
st.title("⚙️ FABLINE CORE")
st.html("<p style='color: #ff6a00; font-weight: bold; letter-spacing: 1.5px; margin-top:-15px;'>PROCUREMENT MONITOR & OPERATIONS TERMINAL</p>")

total_rec = len(st.session_state.jobs)
comp_cnt = sum(1 for j in st.session_state.jobs if j.get("status") == "Complete")
incomp_cnt = sum(1 for j in st.session_state.jobs if j.get("status") == "Incomplete")
expected_cnt = sum(1 for j in st.session_state.jobs if j.get("status") == "Expected")

st.html("<div style='margin-bottom: 20px;'></div>")
m1, m2, m3, m4 = st.columns(4)
m1.metric("TOTAL REGISTRY", total_rec)
m2.metric("READY / SECURED", comp_cnt)
m3.metric("SHORTFALLS", incomp_cnt)
m4.metric("EXPECTED", expected_cnt)

st.markdown("---")

t1, t2, t3 = st.tabs(["📋 MANIFEST REGISTRY", "➕ INITIALIZE RECORD", "🤖 COGNITIVE AUDIT ASSISTANT"])

# --- TAB 1: REGISTRY VIEW WITH DYNAMIC UPDATE PANEL ---
with t1:
    search_q = st.text_input("🔍 SCAN REGISTRY KEYS (Job #, Location, Client Name, Components)...")
    filter_status = st.radio("SORT DATASET VIA OPERATIONS LAYER:", ["All Statuses", "Expected", "Incomplete", "Complete"], horizontal=True)
    
    filtered = st.session_state.jobs
    if search_q: 
        filtered = [j for j in filtered if search_q.lower() in str(j).lower()]
    if filter_status != "All Statuses": 
        filtered = [j for j in filtered if j.get("status") == filter_status]
    
    if not filtered: 
        st.info("No matching records cataloged within database memory.")
        
    for idx, job in enumerate(filtered):
        status_lower = str(job['status']).lower()
        st.markdown(f"""
        <div class="cyber-card">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #343d38; padding-bottom: 10px; margin-bottom: 15px;">
                <span style="font-size: 24px !important; font-weight: 900; color: #ffffff;">JOB OVERLAY: #{job['job_no']}</span>
                <span class="status-pill st-{status_lower}">{job['status']}</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px;">
                <div>
                    <span style="font-size: 13px !important; color: #a4b3a9; display: block; font-weight: bold;">ACCOUNT CLIENT</span>
                    <span style="font-size: 20px !important; font-weight: bold; color: #ffffff;">{job.get('client', 'N/A')}</span>
                </div>
                <div>
                    <span style="font-size: 13px !important; color: #a4b3a9; display: block; font-weight: bold;">FIELD DESTINATION SITE</span>
                    <span style="font-size: 20px !important; font-weight: bold; color: #ffffff;">{job.get('site', 'N/A')}</span>
                </div>
            </div>
            <div style="margin-bottom: 15px;">
                <span style="font-size: 13px !important; color: #a4b3a9; display: block; font-weight: bold; margin-bottom: 5px;">VERIFIED MATERIALS LEDGER MANIFEST</span>
                <div style="background-color: #000000; padding: 15px; border-radius: 6px; border: 1px solid #343d38; font-family: monospace; font-size: 17px !important; white-space: pre-wrap; color: #33cc66;">{job.get('items_logged', 'No cargo logs documented.')}</div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 14px !important; color: #a4b3a9; border-top: 1px dashed #343d38; padding-top: 10px;">
                <span>OPERATOR IN CHARGE: <b style="color:#ffffff;">{job.get('operator', 'System Default')}</b></span>
                <span>SYSTEM TRACK STAMP: {job['updated']}</span>
            </div>
        </div>
        """, unsafe_html=True)
        
        with st.expander(f"🛠️ OPEN TACTICAL ACTION PANEL - MODIFY LOG #{job['job_no']}"):
            with st.form(f"up_{idx}"):
                st.markdown("### UPDATE OPERATIONAL DATA LAYER")
                new_st = st.selectbox("SET RUNTIME STATUS OVERRIDE:", ["Expected", "Incomplete", "Complete"], index=["Expected", "Incomplete", "Complete"].index(job['status']) if job['status'] in ["Expected", "Incomplete", "Complete"] else 0)
                new_txt = st.text_area("APPEND INVENTORY ENTRY LINE (Adds directly below existing data):", placeholder="e.g., [Delivered]: 4x 150mm gate valves secured.")
                up_op = st.text_input("OPERATOR INITIALS / SIGNATURE MATCH:")
                
                if st.form_submit_button("COMMIT MODIFICATIONS"):
                    if not up_op.strip(): 
                        st.error("VERIFICATION FAILURE: Operator signature token missing.")
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
                        save_data(st.session_state.jobs)
                        st.success("CORE MATRIX UPDATED: Refreshing display layers...")
                        st.rerun()
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_html=True)

# --- TAB 2: LOG RECORD ENTRY PANEL ---
with t2:
    st.markdown("<h2>➕ REGISTER INITIAL PROCURED RECORD</h2>", unsafe_html=True)
    st.markdown("Ensure warehouse cargo slips match tracking inputs exactly before committing entries.")
    
    with st.form("new_form", clear_on_submit=True):
        j_no = st.text_input("JOB IDENTIFICATION / PURCHASE ORDER REF:")
        clnt = st.text_input("CLIENT ENTITY NAME:")
        stloc = st.text_input("TARGET SITE DROP LOCATION:")
        stch = st.selectbox("INITIAL TRACKING STATUS BASE:", ["Expected", "Incomplete", "Complete"])
        itm_log = st.text_area("INVENTORY MANIFEST LOG DETAILS (List arriving hardware line items):", placeholder="e.g., 10x 100mm grooved elbows\n2x butterfly valves")
        op_name = st.text_input("AUTHORIZING OPERATOR SIGNATURE:")
        
        if st.form_submit_button("COMMIT ENTRY TO PERSISTENT DATABASE"):
            if j_no and clnt and op_name:
                new_entry = {
                    "job_no": j_no, 
                    "client": clnt, 
                    "site": stloc, 
                    "status": stch,
                    "items_logged": itm_log if itm_log.strip() else "No hardware documented at entry.",
                    "operator": op_name.strip(), 
                    "updated": datetime.now().strftime("%d-%b-%Y %H:%M")
                }
                st.session_state.jobs.insert(0, new_entry)
                save_data(st.session_state.jobs)
                st.success("⚡ REGISTER SUCCESSFUL: Record loaded into database index.")
                st.rerun()
            else: 
                st.error("TRANSACTION HALTED: Job Ref, Client, and Authorizing Operator fields must contain text values.")

# --- TAB 3: COGNITIVE SEARCH ENGINE ---
with t3:
    st.markdown("<h2>🤖 COGNITIVE AUDIT INTERACTION CENTER</h2>", unsafe_html=True)
    st.markdown("Query the operational processor about historical cargo trends, materials history, or workforce sign-offs.")
    
    query = st.text_input("💬 COMMAND INPUT (e.g., '100mm grooved elbows' or 'John'):")
    
    if query:
        matches = [j for j in st.session_state.jobs if query.lower() in str(j).lower()]
        
        with st.chat_message("assistant"):
            st.markdown("### 📡 INTERFACE COGNITIVE READOUT RESPONSE")
            
            if not matches:
                st.markdown(f"Search Analysis Status: Completed.\n\nNo records matching the term '{query}' exist in our database file. Please verify parameters or check alternative job references.")
            else:
                st.markdown(f"#### STATUS: {len(matches)} HISTORICAL ARCHIVES PARSED FOR '{query.upper()}'")
                st.markdown("---")
                
                total_matches = len(matches)
                completed_matches = sum(1 for m in matches if m['status'] == 'Complete')
                pending_matches = total_matches - completed_matches
                
                st.markdown(f"""
                Operational Intelligence Brief Summary:
                * Discovered Records: Found {total_matches} entries containing match patterns.
                * Status Split: {completed_matches} are verified as fully Complete, while {pending_matches} are flagged as Awaiting Action / Incomplete.
                """)
                
                st.markdown("#### DETAILED TRANSACTION BREAKDOWNS:")
                
                for index, item in enumerate(matches):
                    st.markdown(f"""
                    ---
                    ### 📂 TRANSACTION {index + 1}: JOB RECORD #{item['job_no']}
                    * Log State Profile: {item['status']}
                    * Account Client Profile: {item.get('client', 'N/A')}
                    * Deployment Site: {item.get('site', 'N/A')}
                    * Operational Log History Stamp: Updated on {item['updated']} by Engineer {item.get('operator', 'Unassigned')}
                    
                    Hardware Line Manifest History:
                    """)
                    st.code(item.get('items_logged', 'No log items saved.'))
