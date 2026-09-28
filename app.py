import json
import os
from datetime import datetime
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Fabline Registry - Technical Archive",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Design System: Linear / Stripe / Vercel Modern Dark Aesthetic
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        /* Vercel / Linear Dark Palette */
        --bg-main: #090d16;
        --bg-surface: #111827;
        --bg-card: #1f2937;
        --bg-subtle: #374151;

        --text-primary: #f9fafb;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;

        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-focus: #3b82f6;

        --accent-blue: #3b82f6;
        --accent-indigo: #6366f1;

        /* Badge Status Themes */
        --badge-expected-bg: rgba(59, 130, 246, 0.12);
        --badge-expected-txt: #60a5fa;
        --badge-expected-border: rgba(59, 130, 246, 0.3);

        --badge-incomplete-bg: rgba(239, 68, 68, 0.12);
        --badge-incomplete-txt: #f87171;
        --badge-incomplete-border: rgba(239, 68, 68, 0.3);

        --badge-complete-bg: rgba(34, 197, 94, 0.12);
        --badge-complete-txt: #4ade80;
        --badge-complete-border: rgba(34, 197, 94, 0.3);
    }

    /* Global Resets & Layout Safety */
    * {
        box-sizing: border-box !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Main Container Padding */
    .main .block-container {
        max-width: 1200px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* Clean Enterprise Header Components */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
        line-height: 1.25 !important;
        margin-bottom: 0.25rem !important;
    }

    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        color: var(--text-primary) !important;
        line-height: 1.3 !important;
    }

    h2 { font-size: 1.35rem !important; }
    h3 { font-size: 1.15rem !important; color: var(--text-secondary) !important; }

    p, span, label, div {
        font-family: 'Inter', sans-serif !important;
        line-height: 1.5 !important;
    }

    /* Streamlit Metrics Refinement */
    [data-testid="stMetric"] {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-muted) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
    }

    /* Input Fields & Modern Focus States */
    input, textarea, select, div[data-baseweb="select"] {
        background-color: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    input:focus, textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25) !important;
    }

    /* Tabs Styling (Linear Segmented Control Style) */
    div[data-baseweb="tab-list"] {
        background-color: var(--bg-surface) !important;
        padding: 4px !important;
        border-radius: 8px !important;
        border: 1px solid var(--border-subtle) !important;
        gap: 4px !important;
    }

    button[data-baseweb="tab"] {
        height: 38px !important;
        border-radius: 6px !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        border: none !important;
        background: transparent !important;
        padding: 0 1rem !important;
        transition: all 0.15s ease !important;
    }

    button[aria-selected="true"] {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }

    /* Buttons (Stripe Minimal Action Button) */
    button[kind="primary"], div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        transition: filter 0.15s ease, transform 0.05s ease !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.4) !important;
        width: 100% !important;
    }

    button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] button:hover {
        filter: brightness(1.1) !important;
    }

    /* Card Layout Architecture (Flex/Grid Safe) */
    .archive-card {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        transition: border-color 0.15s ease;
    }

    .archive-card:hover {
        border-color: rgba(255, 255, 255, 0.16);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.75rem;
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border-subtle);
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
    }

    /* Micro Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        border: 1px solid transparent;
        white-space: nowrap;
    }

    .st-expected { background: var(--badge-expected-bg); color: var(--badge-expected-txt); border-color: var(--badge-expected-border); }
    .st-incomplete { background: var(--badge-incomplete-bg); color: var(--badge-incomplete-txt); border-color: var(--badge-incomplete-border); }
    .st-complete { background: var(--badge-complete-bg); color: var(--badge-complete-txt); border-color: var(--badge-complete-border); }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .meta-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-muted);
        margin-bottom: 0.2rem;
    }

    .meta-value {
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--text-primary);
        word-break: break-word;
    }

    /* Code & Terminal Blocks (Vercel Style) */
    .inventory-block {
        background-color: var(--bg-main);
        border: 1px solid var(--border-subtle);
        border-radius: 6px;
        padding: 0.85rem;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        color: #e5e7eb;
        white-space: pre-wrap;
        word-break: break-word;
        line-height: 1.5;
    }

    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        font-size: 0.8rem;
        color: var(--text-muted);
        padding-top: 0.75rem;
        border-top: 1px solid var(--border-subtle);
        margin-top: 1rem;
    }

    /* Expanders Reset */
    div[data-testid="stExpander"] {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }

    /* Prevent horizontal overflow on mobile */
    .stAppViewBlockContainer {
        overflow-x: hidden;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 3. Security Check Layer
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if st.session_state["authenticated"]:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            """
            <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
                <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.25rem;">Security Gateway</div>
                <div style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1.5rem;">Fabline Technical Registry & Enterprise Archive</div>
            """,
            unsafe_allow_html=True,
        )

        password_input = st.text_input(
            "Enter Security Access Code", type="password"
        )

        if st.button("Authenticate Terminal Link"):
            if password_input == "fabline2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Verification Rejected: Invalid System Key")

        st.markdown("</div>", unsafe_allow_html=True)

    return False


if not check_password():
    st.stop()

# 4. Storage Engine Setup
DB_FILE = "jobs_data.json"


def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


if "jobs" not in st.session_state:
    st.session_state.jobs = load_data()

# 5. Header Section & High-Density Metrics Grid
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
        <div>
            <h1>Fabline Technical Registry</h1>
            <div style="font-size: 0.9rem; color: var(--text-muted);">Procurement Archive & Data Log Infrastructure</div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

total_rec = len(st.session_state.jobs)
comp_cnt = sum(
    1 for j in st.session_state.jobs if j.get("status") == "Complete"
)
incomp_cnt = sum(
    1 for j in st.session_state.jobs if j.get("status") == "Incomplete"
)
expected_cnt = sum(
    1 for j in st.session_state.jobs if j.get("status") == "Expected"
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Ledger Entries", total_rec)
m2.metric("Secured / Complete", comp_cnt)
m3.metric("Shortfall Backlog", incomp_cnt)
m4.metric("Expected Freight", expected_cnt)

st.markdown("<br>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs([
    "📋 Master Log Registry",
    "➕ Archive New Record",
    "🔬 Historical Inventory Assistant",
])

# --- TAB 1: MASTER REGISTRY VIEW ---
with t1:
    col_search, col_filter = st.columns([3, 2])
    with col_search:
        search_q = st.text_input(
            "Filter Registry",
            placeholder="Search Job ID, Site, Client, or Component...",
            label_visibility="collapsed",
        )
    with col_filter:
        filter_status = st.selectbox(
            "Filter Status",
            ["All Statuses", "Expected", "Incomplete", "Complete"],
            label_visibility="collapsed",
        )

    filtered = st.session_state.jobs
    if search_q:
        filtered = [j for j in filtered if search_q.lower() in str(j).lower()]
    if filter_status != "All Statuses":
        filtered = [j for j in filtered if j.get("status") == filter_status]

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.info("No matching records cataloged in repository memory.")

    for idx, job in enumerate(filtered):
        status = job.get("status", "Expected")
        status_slug = str(status).lower()

        st.markdown(
            f"""
        <div class="archive-card">
            <div class="card-header">
                <div class="card-title">Record Deployment #{job.get('job_no', 'N/A')}</div>
                <span class="status-badge st-{status_slug}">{status}</span>
            </div>
            <div class="card-grid">
                <div>
                    <div class="meta-label">Corporate Account</div>
                    <div class="meta-value">{job.get('client', 'N/A')}</div>
                </div>
                <div>
                    <div class="meta-label">Target Drop Location</div>
                    <div class="meta-value">{job.get('site', 'N/A')}</div>
                </div>
            </div>
            <div>
                <div class="meta-label" style="margin-bottom: 0.35rem;">Verified Hardware Inventory Sheet</div>
                <div class="inventory-block">{job.get('items_logged', 'No cargo logs documented.')}</div>
            </div>
            <div class="card-footer">
                <div>Log Controller: <strong style="color: var(--text-primary);">{job.get('operator', 'Default System')}</strong></div>
                <div>Registry Stamp: {job.get('updated', 'N/A')}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.expander(f"Append Procurement Update — #{job.get('job_no')}"):
            with st.form(f"up_{idx}"):
                st.markdown(
                    "<div style='font-size: 0.875rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.75rem;'>Log Component Freight Updates</div>",
                    unsafe_allow_html=True,
                )

                status_options = ["Expected", "Incomplete", "Complete"]
                default_index = (
                    status_options.index(status)
                    if status in status_options
                    else 0
                )

                new_st = st.selectbox(
                    "Re-assign Status", status_options, index=default_index
                )
                new_txt = st.text_area(
                    "Append Manifest Line",
                    placeholder="e.g., [Freight Update]: 4x 150mm gate valves arrived.",
                )
                up_op = st.text_input(
                    "Logging Officer Initials / Signature Token"
                )

                if st.form_submit_button("Commit Modifications"):
                    if not up_op.strip():
                        st.error("Audit Error: Logging officer signature token required.")
                    else:
                        for r_job in st.session_state.jobs:
                            if r_job.get("job_no") == job.get("job_no"):
                                r_job["status"] = new_st
                                r_job["operator"] = up_op.strip()
                                r_job["updated"] = datetime.now().strftime(
                                    "%d-%b-%Y %H:%M"
                                )
                                if new_txt.strip():
                                    timestamp = datetime.now().strftime(
                                        "%d-%b-%Y %H:%M"
                                    )
                                    r_job["items_logged"] = (
                                        r_job.get("items_logged", "")
                                        + f"\n[{timestamp} by {up_op.strip()}]: "
                                        + new_txt.strip()
                                    )
                                break
                        save_data(st.session_state.jobs)
                        st.success("Archive Synchronized")
                        st.rerun()

# --- TAB 2: ARCHIVE NEW RECORD ---
with t2:
    st.markdown("### Commit Initial Requisition Index Entry")
    st.markdown(
        "<div style='font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1.5rem;'>Ensure freight bills and loading slip line items tally fully prior to submission.</div>",
        unsafe_allow_html=True,
    )

    with st.form("new_form", clear_on_submit=True):
        c_a, c_b = st.columns(2)
        with c_a:
            j_no = st.text_input("Job Accession ID / Manifest Key")
            clnt = st.text_input("Client Business Designation")
        with c_b:
            stloc = st.text_input("Target Field Site Destination")
            stch = st.selectbox(
                "Initial Freight Track Profile",
                ["Expected", "Incomplete", "Complete"],
            )

        itm_log = st.text_area(
            "Inventory Receipt Line Items Manifest",
            placeholder="e.g., 10x 100mm grooved elbows\n2x butterfly valves",
        )
        op_name = st.text_input("Authorizing Officer Audit Signature")

        if st.form_submit_button("Save Requisition Record"):
            if j_no and clnt and op_name:
                new_entry = {
                    "job_no": j_no,
                    "client": clnt,
                    "site": stloc,
                    "status": stch,
                    "items_logged": (
                        itm_log
                        if itm_log.strip()
                        else "No hardware documented at registry entry."
                    ),
                    "operator": op_name.strip(),
                    "updated": datetime.now().strftime("%d-%b-%Y %H:%M"),
                }
                st.session_state.jobs.insert(0, new_entry)
                save_data(st.session_state.jobs)
                st.success("Data Accession Integration Complete")
                st.rerun()
            else:
                st.error(
                    "Registration Terminated: Requisition ID, Client Profile, and Authorizing Officer signature required."
                )

# --- TAB 3: HISTORICAL ASSISTANT ---
with t3:
    st.markdown("### Historical Inventory Search & Technical Lookup")
    st.markdown(
        "<div style='font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1.5rem;'>Query processing index to track movement history, component deployment times, and logistics signatures.</div>",
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "Input Inventory Query Parameters",
        placeholder="e.g., '100mm grooved' or worker initials",
    )

    if query:
        matches = [
            j
            for j in st.session_state.jobs
            if query.lower() in str(j).lower()
        ]

        if not matches:
            st.warning(
                f"No records containing match criteria for tracking string '{query}' were identified."
            )
        else:
            total_matches = len(matches)
            completed_matches = sum(
                1 for m in matches if m.get("status") == "Complete"
            )
            pending_matches = total_matches - completed_matches

            st.markdown(
                f"""
            <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem 1.25rem; margin-top: 1rem; margin-bottom: 1.5rem;">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">Query Analysis Report</div>
                <div style="font-size: 0.875rem; color: var(--text-muted);">Located {total_matches} documents matching target string "{query}". Split: <strong style="color: var(--badge-complete-txt);">{completed_matches} Complete</strong>, <strong style="color: var(--badge-incomplete-txt);">{pending_matches} Pending</strong>.</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            for index, item in enumerate(matches):
                st.markdown(
                    f"""
                <div class="archive-card">
                    <div class="card-header">
                        <div class="card-title">Archive File #{item.get('job_no', 'N/A')}</div>
                        <span class="status-badge st-{str(item.get('status', 'Expected')).lower()}">{item.get('status', 'N/A')}</span>
                    </div>
                    <div class="card-grid">
                        <div>
                            <div class="meta-label">Corporate Account</div>
                            <div class="meta-value">{item.get('client', 'N/A')}</div>
                        </div>
                        <div>
                            <div class="meta-label">Deployment Site</div>
                            <div class="meta-value">{item.get('site', 'N/A')}</div>
                        </div>
                    </div>
                    <div>
                        <div class="meta-label" style="margin-bottom: 0.35rem;">Hardware Line Manifest History</div>
                        <div class="inventory-block">{item.get('items_logged', 'No manifest data cataloged.')}</div>
                    </div>
                    <div class="card-footer">
                        <div>Updated on: {item.get('updated', 'N/A')}</div>
                        <div>Officer Token: {item.get('operator', 'Unassigned')}</div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
