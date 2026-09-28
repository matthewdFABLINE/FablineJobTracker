import json
import os
from datetime import datetime
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Fabline Technical Registry",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Design System: Refined Modern Dark Theme (Warm Accents & Soft Contrast)
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-main: #0c1017;
        --bg-surface: #161e2e;
        --bg-card: #1f293d;
        --bg-subtle: #2d3748;

        --text-primary: #f3f4f6;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;

        --border-subtle: rgba(255, 255, 255, 0.1);
        --border-focus: #3b82f6;

        --accent-blue: #3b82f6;
        --accent-amber: #f59e0b;

        --badge-expected-bg: rgba(245, 158, 11, 0.15);
        --badge-expected-txt: #fbbf24;
        --badge-expected-border: rgba(245, 158, 11, 0.3);

        --badge-soon-bg: rgba(168, 85, 247, 0.15);
        --badge-soon-txt: #c084fc;
        --badge-soon-border: rgba(168, 85, 247, 0.3);

        --badge-incomplete-bg: rgba(239, 68, 68, 0.15);
        --badge-incomplete-txt: #f87171;
        --badge-incomplete-border: rgba(239, 68, 68, 0.3);

        --badge-complete-bg: rgba(34, 197, 94, 0.15);
        --badge-complete-txt: #4ade80;
        --badge-complete-border: rgba(34, 197, 94, 0.3);
    }

    * {
        box-sizing: border-box !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    .main .block-container {
        max-width: 1140px !important;
        padding-top: 2.5rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    h1 {
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.2rem !important;
    }

    /* Welcome Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1.75rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .hero-text-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.4rem;
    }

    .hero-text-subtitle {
        font-size: 0.925rem;
        color: var(--text-secondary);
        line-height: 1.5;
        max-width: 650px;
    }

    .brand-chip {
        display: inline-flex;
        align-items: center;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(59, 130, 246, 0.25);
        color: #60a5fa;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        margin-top: 0.75rem;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        padding: 1.1rem 1.25rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-secondary) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
    }

    /* Form Fields */
    input, textarea, select, div[data-baseweb="select"] {
        background-color: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
    }

    input:focus, textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25) !important;
    }

    /* Tab Headers */
    div[data-baseweb="tab-list"] {
        background-color: var(--bg-surface) !important;
        padding: 5px !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-subtle) !important;
        gap: 6px !important;
    }

    button[data-baseweb="tab"] {
        height: 40px !important;
        border-radius: 7px !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        border: none !important;
        background: transparent !important;
        padding: 0 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    button[aria-selected="true"] {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }

    /* Buttons */
    button[kind="primary"], div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.2rem !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
        width: 100% !important;
        transition: transform 0.1s ease, filter 0.15s ease !important;
    }

    button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] button:hover {
        filter: brightness(1.1) !important;
    }

    /* Custom Record Display Cards */
    .archive-card {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
        transition: border-color 0.2s ease;
    }

    .archive-card:hover {
        border-color: rgba(255, 255, 255, 0.2);
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
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.7rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        border: 1px solid transparent;
    }

    .st-expected { background: var(--badge-expected-bg); color: var(--badge-expected-txt); border-color: var(--badge-expected-border); }
    .st-soon-to-come { background: var(--badge-soon-bg); color: var(--badge-soon-txt); border-color: var(--badge-soon-border); }
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
        color: var(--text-secondary);
        margin-bottom: 0.2rem;
    }

    .meta-value {
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--text-primary);
        word-break: break-word;
    }

    .inventory-block {
        background-color: var(--bg-main);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 0.9rem 1rem;
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

    div[data-testid="stExpander"] {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. Security Gateway
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if st.session_state["authenticated"]:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            """
            <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
                <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.25rem;">🔒 Fabline Access Portal</div>
                <div style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;">Enter authorization code to view hardware registry.</div>
            """,
            unsafe_allow_html=True,
        )

        password_input = st.text_input(
            "Access Key", type="password", placeholder="Enter key..."
        )

        expected_pass = st.secrets.get("ACCESS_KEY", "fabline2026")

        if st.button("Unlock Terminal"):
            if password_input == expected_pass:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Security Key")

        st.markdown("</div>", unsafe_allow_html=True)

    return False


if not check_password():
    st.stop()

# 4. Data Layer & Automatic Schema Migration
DB_FILE = "jobs_data.json"


def migrate_record(job):
    """Automatically maps legacy database keys to current standard keys."""
    return {
        "job_no": job.get("job_no", "N/A"),
        "pipe_sizes": job.get("pipe_sizes") or job.get("client", "N/A"),
        "arrival_datetime": job.get("arrival_datetime") or job.get("site", "N/A"),
        "delivery_status": job.get("delivery_status") or job.get("status", "Expected"),
        "items_logged": job.get("items_logged", "No hardware inventory recorded."),
        "operator": job.get("operator", "System Operator"),
        "updated": job.get("updated", "N/A"),
    }


def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                raw_data = json.load(f)
                return [migrate_record(item) for item in raw_data]
        except Exception:
            return []
    return []


def save_data(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Save failed: {e}")


if "jobs" not in st.session_state:
    st.session_state.jobs = load_data()


def get_status_slug(status_str):
    return str(status_str).lower().replace(" ", "-")


# 5. Header Section & Formal Welcome Greeting
st.markdown(
    """
    <div class="hero-banner">
        <div>
            <div class="hero-text-title">Hello & Welcome to Fabline</div>
            <div class="hero-text-subtitle">
                Welcome to Fabline’s primary online registry for material tracking and orders.
                Log site deliveries, verify pipe fitting requisitions, and audit inventory movements seamlessly across projects.
            </div>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                <span class="brand-chip">⚙️ High-Purity Piping</span>
                <span class="brand-chip">🛠️ Precision Fabrication</span>
                <span class="brand-chip">📋 Quality Assured</span>
            </div>
        </div>
        <div>
            <img src="https://fabline.ie/wp-content/uploads/2021/04/fabline-logo.png" 
                 alt="Fabline Engineering Logo" 
                 style="max-height: 55px; width: auto; opacity: 0.95; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));"
                 onerror="this.style.display='none'">
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Dashboard Metrics
total_rec = len(st.session_state.jobs)
comp_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Complete")
incomp_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Incomplete")
expected_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Expected")
soon_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Soon to come")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Records", total_rec)
m2.metric("Complete & Verified", comp_cnt)
m3.metric("Incomplete Orders", incomp_cnt)
m4.metric("Expected Deliveries", expected_cnt)
m5.metric("Soon to Come", soon_cnt)

st.markdown("<br>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs([
    "📋 Master Registry",
    "➕ Archive New Record",
    "🔍 Historical Assistant",
    "🏢 About Fabline",
])

STATUS_OPTIONS = ["Expected", "Soon to come", "Incomplete", "Complete"]

# --- TAB 1: MASTER REGISTRY VIEW ---
with t1:
    col_search, col_filter = st.columns([3, 2])
    with col_search:
        search_q = st.text_input(
            "Search Archive",
            placeholder="Search Job No., Sizes, Date, or Materials...",
            label_visibility="collapsed",
        )
    with col_filter:
        filter_status = st.selectbox(
            "Filter Status",
            ["All Statuses"] + STATUS_OPTIONS,
            label_visibility="collapsed",
        )

    filtered = st.session_state.jobs
    if search_q:
        filtered = [j for j in filtered if search_q.lower() in str(j).lower()]
    if filter_status != "All Statuses":
        filtered = [j for j in filtered if j.get("delivery_status") == filter_status]

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.info("No matching records found in the database.")

    for job in filtered:
        job_no = job.get("job_no", "N/A")
        status = job.get("delivery_status", "Expected")
        status_slug = get_status_slug(status)

        st.markdown(
            f"""
        <div class="archive-card">
            <div class="card-header">
                <div class="card-title">Job No. #{job_no}</div>
                <span class="status-badge st-{status_slug}">{status}</span>
            </div>
            <div class="card-grid">
                <div>
                    <div class="meta-label">Pipe / Fitting / Valve Sizes</div>
                    <div class="meta-value">{job.get('pipe_sizes', 'N/A')}</div>
                </div>
                <div>
                    <div class="meta-label">Date / Time Of Arrival</div>
                    <div class="meta-value">{job.get('arrival_datetime', 'N/A')}</div>
                </div>
            </div>
            <div>
                <div class="meta-label" style="margin-bottom: 0.35rem;">Inventory Manifest</div>
                <div class="inventory-block">{job.get('items_logged', 'No cargo logs documented.')}</div>
            </div>
            <div class="card-footer">
                <div>Authorized By: <strong style="color: var(--text-primary);">{job.get('operator', 'Unassigned')}</strong></div>
                <div>Last Updated: {job.get('updated', 'N/A')}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.expander(f"Append Record Note or Update Status — #{job_no}"):
            with st.form(f"form_update_{job_no}"):
                default_index = (
                    STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0
                )

                new_st = st.selectbox(
                    "Update Delivery Status", STATUS_OPTIONS, index=default_index
                )
                new_txt = st.text_area(
                    "Append Additional Notes",
                    placeholder="e.g., Arrived with 2 missing 150mm gaskets.",
                )
                up_op = st.text_input("Your Name / Signature")

                if st.form_submit_button("Save Changes"):
                    if not up_op.strip():
                        st.error("Please enter your name or signature to verify this update.")
                    else:
                        for r_job in st.session_state.jobs:
                            if r_job.get("job_no") == job_no:
                                r_job["delivery_status"] = new_st
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
                                        + f"\n[{timestamp} - {up_op.strip()}]: "
                                        + new_txt.strip()
                                    )
                                break
                        save_data(st.session_state.jobs)
                        st.success("Record updated successfully.")
                        st.rerun()

# --- TAB 2: ARCHIVE NEW RECORD ---
with t2:
    st.markdown("### Create New Requisition Record")
    st.markdown(
        "<div style='font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;'>Enter arrival details and material manifests below.</div>",
        unsafe_allow_html=True,
    )

    now_str = datetime.now().strftime("%d-%b-%Y %H:%M")

    with st.form("new_form", clear_on_submit=True):
        c_a, c_b = st.columns(2)
        with c_a:
            j_no = st.text_input("Job No.", placeholder="e.g. 84920")
            pipe_sz = st.text_input(
                "Pipe/Fitting/Valve Sizes", placeholder='e.g. 4" / 6" Grooved'
            )
        with c_b:
            arr_dt = st.text_input(
                "Date/Time Of Arrival", value=now_str
            )
            del_stat = st.selectbox(
                "Delivery Status",
                STATUS_OPTIONS,
            )

        itm_log = st.text_area(
            "Hardware Inventory Manifest",
            placeholder="e.g.,\n- 12x 100mm Grooved Elbows\n- 4x Butterfly Valves",
        )
        op_name = st.text_input("Authorizing Officer / Inspector Signature")

        if st.form_submit_button("Submit Record"):
            if j_no and pipe_sz and op_name:
                if any(j.get("job_no") == j_no.strip() for j in st.session_state.jobs):
                    st.error(f"Entry duplicate: Job No. '{j_no}' is already logged.")
                else:
                    new_entry = {
                        "job_no": j_no.strip(),
                        "pipe_sizes": pipe_sz.strip(),
                        "arrival_datetime": arr_dt.strip(),
                        "delivery_status": del_stat,
                        "items_logged": (
                            itm_log.strip()
                            if itm_log.strip()
                            else "No hardware items listed upon entry."
                        ),
                        "operator": op_name.strip(),
                        "updated": datetime.now().strftime("%d-%b-%Y %H:%M"),
                    }
                    st.session_state.jobs.insert(0, new_entry)
                    save_data(st.session_state.jobs)
                    st.success("Record successfully logged to registry!")
                    st.rerun()
            else:
                st.error(
                    "Please fill out Job No., Pipe/Fitting/Valve Sizes, and Inspector Signature."
                )

# --- TAB 3: HISTORICAL ASSISTANT ---
with t3:
    st.markdown("### Search Material Archives")
    st.markdown(
        "<div style='font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;'>Lookup hardware items, movement logs, and inspector tokens.</div>",
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "Search Keyword",
        placeholder="Type a component (e.g. 'butterfly valve') or inspector name...",
    )

    if query:
        matches = [
            j
            for j in st.session_state.jobs
            if query.lower() in str(j).lower()
        ]

        if not matches:
            st.warning(f"No archive records found containing '{query}'.")
        else:
            total_matches = len(matches)
            completed_matches = sum(
                1 for m in matches if m.get("delivery_status") == "Complete"
            )
            pending_matches = total_matches - completed_matches

            st.markdown(
                f"""
            <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem 1.25rem; margin-top: 1rem; margin-bottom: 1.5rem;">
                <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">Archive Search Results</div>
                <div style="font-size: 0.875rem; color: var(--text-secondary);">Found {total_matches} entries matching "<strong>{query}</strong>" ({completed_matches} Complete, {pending_matches} Pending).</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            for item in matches:
                status_slug = get_status_slug(item.get('delivery_status', 'Expected'))
                st.markdown(
                    f"""
                <div class="archive-card">
                    <div class="card-header">
                        <div class="card-title">Job No. #{item.get('job_no', 'N/A')}</div>
                        <span class="status-badge st-{status_slug}">{item.get('delivery_status', 'N/A')}</span>
                    </div>
                    <div class="card-grid">
                        <div>
                            <div class="meta-label">Pipe/Fitting/Valve Sizes</div>
                            <div class="meta-value">{item.get('pipe_sizes', 'N/A')}</div>
                        </div>
                        <div>
                            <div class="meta-label">Date/Time Of Arrival</div>
                            <div class="meta-value">{item.get('arrival_datetime', 'N/A')}</div>
                        </div>
                    </div>
                    <div>
                        <div class="meta-label" style="margin-bottom: 0.35rem;">Inventory Manifest</div>
                        <div class="inventory-block">{item.get('items_logged', 'No manifest data recorded.')}</div>
                    </div>
                    <div class="card-footer">
                        <div>Authorized By: {item.get('operator', 'Unassigned')}</div>
                        <div>Last Updated: {item.get('updated', 'N/A')}</div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

# --- TAB 4: ABOUT FABLINE ---
with t4:
    st.markdown("### About Fabline Engineering")
    st.markdown(
        """
    Fabline Engineering specializes in high-purity mechanical piping, stainless steel fabrication, and modular skid manufacturing for pharmaceutical, microelectronics, and heavy industrial sectors.

    #### Key Capabilities & Standards
    - **High-Purity Process Piping:** Orbital welding and certified cleanroom assembly.
    - **Modular Skid Fabrication:** Off-site prefabrication reduces installation risk and downtime.
    - **Quality Assurance & Traceability:** Material certifications, heat numbers, and inspection records logged to this registry.
    
    *For full corporate details or official project inquiries, visit [fabline.ie](https://fabline.ie).*
    """
    )
