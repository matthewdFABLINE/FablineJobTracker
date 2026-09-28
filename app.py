import csv
import hmac
import io
import json
import math
import os
import re
import tempfile
from datetime import datetime
import streamlit as st

# Optional OCR library import for image reading
try:
    import PIL.Image
    import easyocr
    import numpy as np
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

# 1. Page Configuration
st.set_page_config(
    page_title="Fabline Technical Registry",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Design System: Aesthetic Flowing Rainbow Neon Theme
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-main: #06080c;
        --bg-surface: #0f141f;
        --bg-card: #172030;
        --bg-subtle: #232f45;

        --text-primary: #f3f4f6;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;

        --border-subtle: rgba(255, 255, 255, 0.1);
        --accent-blue: #3b82f6;

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

    * { box-sizing: border-box !important; }

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

    /* 🌈 ANIMATED RAINBOW GLOW WRAPPER */
    .rainbow-wrapper {
        position: relative;
        border-radius: 20px;
        padding: 3px;
        background: linear-gradient(
            90deg,
            #ff0055,
            #ff5000,
            #ffea00,
            #00ff66,
            #00e5ff,
            #7a00ff,
            #ff0055
        );
        background-size: 400% 400%;
        animation: flowRainbow 8s linear infinite;
        margin-bottom: 2rem;
    }

    /* Ambient Glow Behind Frame */
    .rainbow-wrapper::before {
        content: '';
        position: absolute;
        inset: -10px;
        border-radius: 26px;
        background: inherit;
        background-size: inherit;
        filter: blur(24px);
        opacity: 0.6;
        z-index: 0;
        animation: flowRainbow 8s linear infinite;
    }

    @keyframes flowRainbow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .hero-banner {
        position: relative;
        z-index: 1;
        background: var(--bg-surface);
        border-radius: 17px;
        padding: 1.75rem 2rem;
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

    .ocr-box {
        background: rgba(59, 130, 246, 0.08);
        border: 1px dashed rgba(59, 130, 246, 0.4);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
    }

    .alert-banner {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .alert-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #f87171;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .alert-body {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

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

    .archive-card {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
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

    .category-tag {
        display: inline-flex;
        align-items: center;
        background: rgba(59, 130, 246, 0.15);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }

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

    .timeline-item {
        border-left: 2px solid var(--accent-blue);
        padding-left: 0.85rem;
        margin-bottom: 0.75rem;
        position: relative;
    }

    .timeline-date {
        font-size: 0.75rem;
        color: var(--text-muted);
        font-weight: 600;
    }

    .timeline-actor {
        font-size: 0.825rem;
        color: #60a5fa;
        font-weight: 600;
    }

    .timeline-note {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.2rem;
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
            if hmac.compare_digest(password_input, expected_pass):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Security Key")

        st.markdown("</div>", unsafe_allow_html=True)

    return False


if not check_password():
    st.stop()

# 4. Constants & Data Management
DB_FILE = "jobs_data.json"
STATUS_OPTIONS = ["Expected", "Soon to come", "Incomplete", "Complete"]
CATEGORY_OPTIONS = [
    "Piping & Tubing",
    "Valves & Actuators",
    "Fittings & Flanges",
    "Structural & Support Steel",
    "Fasteners, Gaskets & Seals",
    "Consumables & Welding Supplies",
    "Instruments & Electrical",
    "Custom / Modular Skid / Equipment",
    "General Site Deliveries"
]
VALVE_OPTIONS = ["None / Standard Fitting", "Wet Pipe", "Dry Pipe", "Pre-Action", "Deluge"]


def parse_docket_image(image_bytes):
    extracted_text = ""
    if HAS_OCR:
        try:
            image = PIL.Image.open(io.BytesIO(image_bytes))
            reader = easyocr.Reader(['en'], gpu=False)
            results = reader.readtext(np.array(image), detail=0)
            extracted_text = "\n".join(results)
        except Exception:
            extracted_text = ""
    
    job_no = ""
    job_match = re.search(r'(?:Job|Order|Docket|PO)\s*#?\s*([A-Za-z0-9\-]+)', extracted_text, re.IGNORECASE)
    if job_match:
        job_no = job_match.group(1)

    lines = [line.strip() for line in extracted_text.split("\n") if line.strip()]
    formatted_items = []
    
    for line in lines:
        if any(char.isdigit() for char in line) and len(line) > 3:
            formatted_items.append(f"- {line}")
            
    manifest = "\n".join(formatted_items) if formatted_items else extracted_text

    return job_no, manifest


def migrate_record(job):
    now_time = datetime.now().strftime("%d-%b-%Y %H:%M")
    audit_trail = job.get("audit_trail", [])
    if not audit_trail:
        initial_op = job.get("operator", "System Operator")
        audit_trail = [
            {
                "timestamp": job.get("updated", now_time),
                "operator": initial_op,
                "action": "Record Created / Migrated",
                "status": job.get("delivery_status") or job.get("status", "Expected"),
                "note": "Initial logging into Fabline database.",
            }
        ]

    return {
        "job_no": job.get("job_no", "N/A"),
        "category": job.get("category", "Piping & Tubing"),
        "pipe_sizes": job.get("pipe_sizes") or job.get("client", "N/A"),
        "arrival_datetime": job.get("arrival_datetime") or job.get("site", "N/A"),
        "delivery_status": job.get("delivery_status") or job.get("status", "Expected"),
        "valve_type": job.get("valve_type", "None / Standard Fitting"),
        "items_logged": job.get("items_logged", "No inventory recorded."),
        "operator": job.get("operator", "System Operator"),
        "updated": job.get("updated", now_time),
        "audit_trail": audit_trail,
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
        dir_name = os.path.dirname(DB_FILE) or "."
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
            json.dump(data, tf, indent=4)
            temp_path = tf.name
        os.replace(temp_path, DB_FILE)
    except Exception as e:
        st.error(f"Save failed: {e}")


def generate_csv(records):
    output = io.StringIO()
    if not records:
        return ""
    
    fieldnames = ["job_no", "category", "pipe_sizes", "arrival_datetime", "delivery_status", "valve_type", "items_logged", "operator", "updated"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in records:
        writer.writerow({k: row.get(k, "") for k in fieldnames})
    
    return output.getvalue()


if "jobs" not in st.session_state:
    st.session_state.jobs = load_data()

if "item_count" not in st.session_state:
    st.session_state.item_count = 1


def get_status_slug(status_str):
    return str(status_str).lower().replace(" ", "-")


# 5. Animated Rainbow Header Section
st.markdown(
    """
    <div class="rainbow-wrapper">
        <div class="hero-banner">
            <div>
                <div class="hero-text-title">Hello & Welcome to Fabline</div>
                <div class="hero-text-subtitle">
                    Welcome to Fabline’s primary online registry for material tracking and orders.
                    Log site deliveries, verify fittings, structural steel, and specialized equipment requisitions seamlessly across projects.
                </div>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="brand-chip">⚙️ High-Purity Piping</span>
                    <span class="brand-chip">🛠️ Precision Fabrication</span>
                    <span class="brand-chip">📋 Quality Assured</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; justify-content: center;">
                <svg width="220" height="60" viewBox="0 0 220 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="220" height="60" rx="8" fill="#1e293b"/>
                    <path d="M15 18H35V24H23V30H33V36H23V46H15V18Z" fill="#3b82f6"/>
                    <text x="45" y="38" font-family="'Inter', sans-serif" font-weight="800" font-size="24" fill="#ffffff" letter-spacing="1">FABLINE</text>
                    <text x="45" y="48" font-family="'Inter', sans-serif" font-weight="600" font-size="8" fill="#9ca3af" letter-spacing="2">ENGINEERING LTD</text>
                </svg>
            </div>
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

t1, t2, t3, t4, t5 = st.tabs([
    "📋 Master Registry",
    "➕ Archive New Record",
    "𝜟 Technical Calculator",
    "🔍 Historical Assistant",
    "🏢 About Fabline & Valve Specs",
])

# --- TAB 1: MASTER REGISTRY VIEW ---
with t1:
    pending_total = incomp_cnt + expected_cnt + soon_cnt
    if pending_total > 0:
        st.markdown(
            f"""
            <div class="alert-banner">
                <div>
                    <div class="alert-title">⚠️ Attention Required: Active Supply Chain Action Items</div>
                    <div class="alert-body">
                        There are currently <strong>{incomp_cnt} incomplete orders</strong> needing verification and 
                        <strong>{expected_cnt + soon_cnt} pending shipments</strong> scheduled for arrival.
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <span class="status-badge st-incomplete">{incomp_cnt} Incomplete</span>
                    <span class="status-badge st-expected">{expected_cnt} Expected</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col_search, col_cat, col_status, col_export = st.columns([2.5, 1.5, 1.5, 1.2])
    with col_search:
        search_q = st.text_input(
            "Search Archive",
            placeholder="Search Job No., Category, Sizes, Date, or Materials...",
            label_visibility="collapsed",
        )
    with col_cat:
        filter_cat = st.selectbox(
            "Filter Category",
            ["All Categories"] + CATEGORY_OPTIONS,
            label_visibility="collapsed",
        )
    with col_status:
        filter_status = st.selectbox(
            "Filter Status",
            ["All Statuses"] + STATUS_OPTIONS,
            label_visibility="collapsed",
        )

    filtered = st.session_state.jobs
    if search_q:
        filtered = [j for j in filtered if search_q.lower() in str(j).lower()]
    if filter_cat != "All Categories":
        filtered = [j for j in filtered if j.get("category") == filter_cat]
    if filter_status != "All Statuses":
        filtered = [j for j in filtered if j.get("delivery_status") == filter_status]

    with col_export:
        csv_data = generate_csv(filtered)
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name=f"fabline_registry_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.info("No matching records found in the database.")

    for job in filtered:
        job_no = job.get("job_no", "N/A")
        cat = job.get("category", "General Site Deliveries")
        status = job.get("delivery_status", "Expected")
        v_type = job.get("valve_type", "None / Standard Fitting")
        status_slug = get_status_slug(status)

        category_badge = f'<span class="category-tag">📦 {cat}</span>'
        valve_badge = f'<span class="category-tag">🏷️ {v_type}</span>' if v_type and v_type != "None / Standard Fitting" else ""

        st.markdown(
            f"""
        <div class="archive-card">
            <div class="card-header">
                <div>
                    <span class="card-title">Job No. #{job_no}</span>
                    {category_badge}
                    {valve_badge}
                </div>
                <span class="status-badge st-{status_slug}">{status}</span>
            </div>
            <div class="card-grid">
                <div>
                    <div class="meta-label">Specification / Dimensions / Tag</div>
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

        with st.expander(f"Manage Record & View Full Audit Trail — #{job_no}"):
            st.markdown("##### 📜 Audit Trail & Chain of Custody History")
            trail = job.get("audit_trail", [])
            if trail:
                for event in reversed(trail):
                    st.markdown(
                        f"""
                        <div class="timeline-item">
                            <div class="timeline-date">🕒 {event.get('timestamp', 'N/A')}</div>
                            <div class="timeline-actor">👤 {event.get('operator', 'System')} - <span style="color: var(--text-primary);">{event.get('action', 'Update')}</span> (Status: {event.get('status', 'N/A')})</div>
                            <div class="timeline-note">{event.get('note', 'No details specified.')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No historical audit steps recorded.")

            st.markdown("---")
            st.markdown("##### ✏️ Update Record Details")

            with st.form(f"form_update_{job_no}"):
                default_st_idx = STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0
                default_v_idx = VALVE_OPTIONS.index(v_type) if v_type in VALVE_OPTIONS else 0
                default_cat_idx = CATEGORY_OPTIONS.index(cat) if cat in CATEGORY_OPTIONS else 0

                c_u1, c_u2, c_u3 = st.columns(3)
                with c_u1:
                    new_st = st.selectbox("Update Delivery Status", STATUS_OPTIONS, index=default_st_idx)
                with c_u2:
                    new_cat = st.selectbox("Update Delivery Category", CATEGORY_OPTIONS, index=default_cat_idx)
                with c_u3:
                    new_vt = st.selectbox("Update Valve Classification", VALVE_OPTIONS, index=default_v_idx)

                new_txt = st.text_area(
                    "Append Additional Notes",
                    placeholder="e.g., Arrived with 2 missing 150mm gaskets.",
                )
                up_op = st.text_input("Your Name / Inspector Signature")

                if st.form_submit_button("Save Changes & Log Audit Entry"):
                    if not up_op.strip():
                        st.error("Please enter your name or signature to verify this update.")
                    else:
                        now_stamp = datetime.now().strftime("%d-%b-%Y %H:%M")
                        for r_job in st.session_state.jobs:
                            if r_job.get("job_no") == job_no:
                                old_st = r_job.get("delivery_status")
                                r_job["delivery_status"] = new_st
                                r_job["category"] = new_cat
                                r_job["valve_type"] = new_vt
                                r_job["operator"] = up_op.strip()
                                r_job["updated"] = now_stamp
                                
                                note_entry = new_txt.strip() if new_txt.strip() else "Status / details updated."
                                if new_txt.strip():
                                    r_job["items_logged"] = (
                                        r_job.get("items_logged", "")
                                        + f"\n[{now_stamp} - {up_op.strip()}]: "
                                        + new_txt.strip()
                                    )

                                r_job.setdefault("audit_trail", []).append(
                                    {
                                        "timestamp": now_stamp,
                                        "operator": up_op.strip(),
                                        "action": f"Changed status from '{old_st}' to '{new_st}'" if old_st != new_st else "Updated details/notes",
                                        "status": new_st,
                                        "note": note_entry,
                                    }
                                )
                                break
                        save_data(st.session_state.jobs)
                        st.success("Record updated and logged to audit trail.")
                        st.rerun()

# --- TAB 2: ARCHIVE NEW RECORD ---
with t2:
    st.markdown("### Create New Delivery Record")
    st.markdown(
        "<div style='font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem;'>Scan physical delivery papers or enter custom multi-category line items below.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="ocr-box">
            <div style="font-size: 1rem; font-weight: 700; color: #60a5fa; margin-bottom: 0.25rem;">📸 AI Delivery Docket Reader</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);">
                Take a photo of the paper delivery docket using your phone or laptop camera to instantly extract expected material line items and Job Numbers.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    scan_mode = st.radio(
        "Capture Method",
        ["📷 Use Camera", "📁 Upload Docket File/Photo"],
        horizontal=True,
        label_visibility="collapsed"
    )

    scanned_job_no = ""
    scanned_manifest = ""

    if scan_mode == "📷 Use Camera":
        img_file = st.camera_input("Take picture of Delivery Docket")
        if img_file:
            with st.spinner("AI Reading Delivery Docket..."):
                bytes_data = img_file.getvalue()
                scanned_job_no, scanned_manifest = parse_docket_image(bytes_data)
                st.success("Docket read successfully! Verify values in the form below.")
    else:
        uploaded_file = st.file_uploader("Upload Delivery Docket Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            with st.spinner("AI Reading Delivery Docket..."):
                bytes_data = uploaded_file.getvalue()
                scanned_job_no, scanned_manifest = parse_docket_image(bytes_data)
                st.success("Docket read successfully! Verify values in the form below.")

    st.markdown("<hr style='border-color: var(--border-subtle); margin: 1.5rem 0;'>", unsafe_allow_html=True)

    now_str = datetime.now().strftime("%d-%b-%Y %H:%M")

    st.markdown("#### 1. General Shipment Meta")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        j_no = st.text_input("Job / Order No. *", value=scanned_job_no, placeholder="e.g. 84920 or PO-10928")
        shipment_cat = st.selectbox("Primary Category Classification", CATEGORY_OPTIONS)
        pipe_sz = st.text_input(
            "Overall Specs / Dimensions / Tag", placeholder='e.g. 4" Sch 40 / Stainless Steel / Beam IPE200'
        )
    with col_m2:
        arr_dt = st.text_input("Date/Time Of Arrival", value=now_str)
        del_stat = st.selectbox("Delivery Status", STATUS_OPTIONS)
        v_type_input = st.selectbox("Valve System Classification (If Applicable)", VALVE_OPTIONS)

    st.markdown("---")
    st.markdown("#### 2. Detailed Itemized Manifest")
    st.markdown(
        "<div style='font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.75rem;'>Log diverse shipment records line-by-line or paste full raw manifest text below.</div>",
        unsafe_allow_html=True,
    )

    entry_method = st.radio("Manifest Style", ["📝 Freeform Text / Docket Output", "➕ Structured Custom Line-Item Builder"], horizontal=True)

    final_manifest_str = ""

    if entry_method == "📝 Freeform Text / Docket Output":
        default_manifest_val = (
            f"--- SCANNED FROM DOCKET ---\n{scanned_manifest}"
            if scanned_manifest
            else ""
        )
        final_manifest_str = st.text_area(
            "Inventory Items Log",
            value=default_manifest_val,
            placeholder="e.g.,\n- 5x IPE200 Beams 6m\n- 20x 1/2\" Stainless Steel Ball Valves\n- 2x Pallets 150mm Gaskets & Bolts",
            height=180,
        )
    else:
        st.caption("Add individual line items received on site:")
        
        c_add1, c_add2, _ = st.columns([1, 1, 3])
        with c_add1:
            if st.button("➕ Add Row"):
                st.session_state.item_count += 1
                st.rerun()
        with c_add2:
            if st.button("➖ Remove Row") and st.session_state.item_count > 1:
                st.session_state.item_count -= 1
                st.rerun()

        item_rows = []
        for i in range(st.session_state.item_count):
            c_i1, c_i2, c_i3, c_i4 = st.columns([2, 1, 1, 2])
            with c_i1:
                item_desc = st.text_input(f"Item Description #{i+1}", key=f"desc_{i}", placeholder="e.g. M16 Stainless Steel Bolts")
            with c_i2:
                item_qty = st.text_input(f"Quantity #{i+1}", key=f"qty_{i}", placeholder="e.g. 50")
            with c_i3:
                item_unit = st.selectbox(f"Unit #{i+1}", ["Units", "Box/Pack", "Meters", "Lengths", "Pallets", "Kg"], key=f"unit_{i}")
            with c_i4:
                item_notes = st.text_input(f"Condition / Spec #{i+1}", key=f"notes_{i}", placeholder="e.g. Verified, Grade 316")

            if item_desc.strip():
                item_rows.append(f"- {item_qty} {item_unit} x {item_desc} ({item_notes})" if item_notes else f"- {item_qty} {item_unit} x {item_desc}")

        final_manifest_str = "\n".join(item_rows) if item_rows else "No structured line items recorded."

    st.markdown("---")
    op_name = st.text_input("Authorizing Inspector / Site Signature *", placeholder="Enter your full name")

    if st.button("Submit Record to Registry", type="primary"):
        if j_no and pipe_sz and op_name:
            if any(j.get("job_no") == j_no.strip() for j in st.session_state.jobs):
                st.error(f"Entry duplicate: Job No. '{j_no}' is already logged in the database.")
            else:
                creation_time = datetime.now().strftime("%d-%b-%Y %H:%M")
                initial_manifest = (
                    final_manifest_str.strip()
                    if final_manifest_str.strip()
                    else "No material items listed upon entry."
                )
                
                new_entry = {
                    "job_no": j_no.strip(),
                    "category": shipment_cat,
                    "pipe_sizes": pipe_sz.strip(),
                    "arrival_datetime": arr_dt.strip(),
                    "delivery_status": del_stat,
                    "valve_type": v_type_input,
                    "items_logged": initial_manifest,
                    "operator": op_name.strip(),
                    "updated": creation_time,
                    "audit_trail": [
                        {
                            "timestamp": creation_time,
                            "operator": op_name.strip(),
                            "action": "Initial Creation (Docket Scanned)" if scanned_manifest else "Initial Creation",
                            "status": del_stat,
                            "note": f"Log created under '{shipment_cat}' category.",
                        }
                    ],
                }
                st.session_state.jobs.insert(0, new_entry)
                save_data(st.session_state.jobs)
                st.session_state.item_count = 1
                st.success("Record successfully logged to registry!")
                st.rerun()
        else:
            st.error("Please complete required fields: Job/Order No., Specs/Dimensions, and Inspector Signature.")

# --- TAB 3: TECHNICAL CALCULATOR ---
with t3:
    st.markdown("### On-Site Pipe Pressure & Volume Calculator")
    st.markdown(
        "<div style='font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;'>Rapid engineering estimation for internal pressure limits (Barlow's Formula) and hydrostatic water volumetric fill weights.</div>",
        unsafe_allow_html=True,
    )

    col_calc1, col_calc2 = st.columns(2)

    with col_calc1:
        st.markdown("#### ⚡ Pressure Rating (Barlow's Formula)")
        pipe_od_dict = {
            '2" (60.3 mm OD)': 2.375,
            '3" (88.9 mm OD)': 3.500,
            '4" (114.3 mm OD)': 4.500,
            '6" (168.3 mm OD)': 6.625,
            '8" (219.1 mm OD)': 8.625,
            '10" (273.1 mm OD)': 10.750,
            '12" (323.8 mm OD)': 12.750,
        }

        sel_pipe = st.selectbox("Nominal Pipe Size", list(pipe_od_dict.keys()))
        D = pipe_od_dict[sel_pipe]

        sched = st.selectbox("Schedule / Wall Thickness", ["Schedule 10", "Schedule 40", "Schedule 80", "Schedule 160"])
        wall_thickness_map = {
            '2" (60.3 mm OD)': {"Schedule 10": 0.109, "Schedule 40": 0.154, "Schedule 80": 0.218, "Schedule 160": 0.343},
            '3" (88.9 mm OD)': {"Schedule 10": 0.120, "Schedule 40": 0.216, "Schedule 80": 0.300, "Schedule 160": 0.438},
            '4" (114.3 mm OD)': {"Schedule 10": 0.120, "Schedule 40": 0.237, "Schedule 80": 0.337, "Schedule 160": 0.531},
            '6" (168.3 mm OD)': {"Schedule 10": 0.134, "Schedule 40": 0.280, "Schedule 80": 0.432, "Schedule 160": 0.718},
            '8" (219.1 mm OD)': {"Schedule 10": 0.148, "Schedule 40": 0.322, "Schedule 80": 0.500, "Schedule 160": 0.906},
            '10" (273.1 mm OD)': {"Schedule 10": 0.165, "Schedule 40": 0.365, "Schedule 80": 0.593, "Schedule 160": 1.125},
            '12" (323.8 mm OD)': {"Schedule 10": 0.180, "Schedule 40": 0.375, "Schedule 80": 0.687, "Schedule 160": 1.312},
        }

        t_wall = wall_thickness_map[sel_pipe][sched]

        mat_yield_dict = {
            "316L Stainless Steel (30,000 PSI Yield)": 30000,
            "304 Stainless Steel (30,000 PSI Yield)": 30000,
            "Carbon Steel A106 Grade B (35,000 PSI Yield)": 35000,
        }
        sel_mat = st.selectbox("Material Grade", list(mat_yield_dict.keys()))
        S = mat_yield_dict[sel_mat]

        safety_factor = st.slider("Safety Factor (SF)", min_value=1.5, max_value=4.0, value=2.0, step=0.1)

        burst_p = (2 * S * t_wall) / D
        mawp = burst_p / safety_factor
        mawp_bar = mawp * 0.0689476

        st.markdown(
            f"""
            <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                <div class="meta-label">Calculated MAWP (Working Pressure)</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #4ade80;">{mawp:,.0f} PSI <span style="font-size: 1rem; color: var(--text-secondary);">({mawp_bar:.1f} Bar)</span></div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem;">
                    Theoretical Burst Pressure: {burst_p:,.0f} PSI | Wall Thickness: {t_wall:.3f}"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_calc2:
        st.markdown("#### 💧 Internal Volume & Hydrostatic Fill Weight")

        pipe_len = st.number_input("Total Pipe Run Length (Meters)", min_value=1.0, max_value=1000.0, value=10.0, step=1.0)

        id_inches = D - (2 * t_wall)
        id_meters = id_inches * 0.0254

        volume_m3 = math.pi * ((id_meters / 2) ** 2) * pipe_len
        volume_liters = volume_m3 * 1000.0
        volume_gallons = volume_liters * 0.264172
        water_weight_kg = volume_liters

        st.markdown(
            f"""
            <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                <div class="meta-label">Internal Water Capacity</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #60a5fa;">{volume_liters:.1f} Liters <span style="font-size: 1rem; color: var(--text-secondary);">({volume_gallons:.1f} US Gal)</span></div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem;">
                    Hydrotest Fluid Mass: ~{water_weight_kg:.1f} kg ({water_weight_kg * 2.20462:.1f} lbs) | Internal Dia: {id_inches:.3f}"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- TAB 4: HISTORICAL ASSISTANT ---
with t4:
    st.markdown("### Search Material Archives")
    st.markdown(
        "<div style='font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;'>Lookup hardware items, movement logs, categories, and inspector tokens.</div>",
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "Search Keyword",
        placeholder="Type a component (e.g. 'beam', 'butterfly valve') or inspector name...",
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
                cat = item.get("category", "General Site Deliveries")
                v_type = item.get("valve_type", "None / Standard Fitting")
                
                category_badge = f'<span class="category-tag">📦 {cat}</span>'
                valve_badge = f'<span class="category-tag">🏷️ {v_type}</span>' if v_type and v_type != "None / Standard Fitting" else ""

                st.markdown(
                    f"""
                <div class="archive-card">
                    <div class="card-header">
                        <div>
                            <span class="card-title">Job No. #{item.get('job_no', 'N/A')}</span>
                            {category_badge}
                            {valve_badge}
                        </div>
                        <span class="status-badge st-{status_slug}">{item.get('delivery_status', 'N/A')}</span>
                    </div>
                    <div class="card-grid">
                        <div>
                            <div class="meta-label">Specification / Dimensions / Tag</div>
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

# --- TAB 5: ABOUT FABLINE & VALVE SPECIFICATIONS ---
with t5:
    st.markdown("### About Fabline Engineering")
    st.markdown(
        """
    Fabline Engineering specializes in high-purity mechanical piping, stainless steel fabrication, structural skids, and modular assembly for pharmaceutical, microelectronics, and heavy industrial sectors.

    #### Key Capabilities & Standards
    - **High-Purity Process Piping:** Orbital welding and certified cleanroom assembly.
    - **Structural Steel & Skids:** Custom frame fabrication and off-site modular skids.
    - **Fire Protection & Valve Assemblies:** Manifold integrations and certified pressure testing.
    
    *For full corporate details or official project inquiries, visit [fabline.ie](https://fabline.ie).*
    """
    )
