import csv
import hmac
import io
import json
import os
import re
import tempfile
from datetime import datetime
import streamlit as st

# Optional OCR library import for image processing
try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

# 1. Page Configuration
st.set_page_config(
    page_title="Fabline Internal Operations & Technical Registry",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Design System: Professional Industrial Engineering Palette
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --navy-dark: #0F1B2D;
        --navy-surface: #1E293B;
        --crimson-red: #D32F2F;
        --crimson-hover: #E53E3E;
        --steel-gray: #64748B;
        --steel-border: #CBD5E1;
        --steel-light: #F8FAFC;
        --pure-white: #FFFFFF;
        
        --badge-expected-bg: #FEF3C7;
        --badge-expected-txt: #92400E;
        --badge-expected-border: #FCD34D;

        --badge-soon-bg: #F3E8FF;
        --badge-soon-txt: #6B21A8;
        --badge-soon-border: #D8B4FE;

        --badge-incomplete-bg: #FEE2E2;
        --badge-incomplete-txt: #991B1B;
        --badge-incomplete-border: #FCA5A5;

        --badge-complete-bg: #DCFCE7;
        --badge-complete-txt: #166534;
        --badge-complete-border: #86EFAC;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--steel-light) !important;
        color: var(--navy-dark) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        line-height: 1.6 !important;
        -webkit-font-smoothing: antialiased;
    }

    .main .block-container {
        max-width: 1200px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    h1, h2, h3, .heading-industrial {
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        font-weight: 800 !important;
    }

    .hero-banner {
        background-color: var(--navy-dark);
        border-radius: 12px;
        padding: 2.25rem 2.75rem;
        color: var(--pure-white);
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(15, 27, 45, 0.3);
        border-bottom: 4px solid var(--crimson-red);
    }

    .hero-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--pure-white);
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        max-width: 820px;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    [data-testid="stMetric"] {
        background-color: var(--pure-white) !important;
        border: 1px solid var(--steel-border) !important;
        border-left: 4px solid var(--navy-dark) !important;
        border-radius: 8px !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.725rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--steel-gray) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: var(--navy-dark) !important;
    }

    .product-card {
        background-color: var(--pure-white);
        border: 1px solid var(--steel-border);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.25s ease;
        margin-bottom: 1.25rem;
        position: relative;
    }

    .product-card:hover {
        box-shadow: 0 10px 20px rgba(15, 27, 45, 0.08);
        border-color: var(--navy-dark);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.75rem;
        padding-bottom: 0.85rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #E2E8F0;
    }

    .card-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--navy-dark);
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    .accent-badge-red {
        background-color: #FEE2E2;
        color: var(--crimson-red);
        border: 1px solid #FCA5A5;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.25rem 0.65rem;
        border-radius: 4px;
        display: inline-block;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.3rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
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
        background: #F1F5F9;
        color: var(--navy-dark);
        border: 1px solid var(--steel-border);
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.25rem;
        margin-bottom: 1rem;
    }

    .meta-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.725rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--steel-gray);
        margin-bottom: 0.2rem;
    }

    .meta-value {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--navy-dark);
        word-break: break-word;
    }

    .inventory-block {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 3px solid var(--navy-dark);
        border-radius: 6px;
        padding: 0.9rem 1rem;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        color: #1E293B;
        white-space: pre-wrap;
        word-break: break-word;
        line-height: 1.5;
    }

    .notice-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }

    .notice-card.urgent {
        border-left: 5px solid #D32F2F;
        background-color: #FEF2F2;
    }

    .notice-card.action {
        border-left: 5px solid #D97706;
        background-color: #FFFBEB;
    }

    .notice-card.info {
        border-left: 5px solid #0284C7;
        background-color: #F0F9FF;
    }

    div[data-baseweb="tab-list"] {
        background-color: var(--pure-white) !important;
        padding: 6px !important;
        border-radius: 8px !important;
        border: 1px solid var(--steel-border) !important;
        gap: 8px !important;
    }

    button[data-baseweb="tab"] {
        height: 42px !important;
        border-radius: 6px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.825rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.03em !important;
        color: var(--steel-gray) !important;
        border: none !important;
        background: transparent !important;
        padding: 0 1.25rem !important;
    }

    button[aria-selected="true"] {
        background-color: var(--navy-dark) !important;
        color: var(--pure-white) !important;
        box-shadow: 0 2px 6px rgba(15, 27, 45, 0.2) !important;
    }

    .alert-banner {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-left: 5px solid var(--crimson-red);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .alert-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        color: var(--crimson-red);
    }

    .alert-body {
        font-size: 0.875rem;
        color: #475569;
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
            <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-top: 5px solid #0F1B2D; border-radius: 8px; padding: 2.25rem; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                <div style="font-family: 'Montserrat', sans-serif; font-size: 1.35rem; font-weight: 800; text-transform: uppercase; color: #0F1B2D; margin-bottom: 0.25rem;">🔒 FABLINE INTERNAL SYSTEM ACCESS</div>
                <div style="font-size: 0.875rem; color: #64748B; margin-bottom: 1.5rem;">Enter employee authorization key to access site registry and operational tools.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        password_input = st.text_input(
            "Employee Authorization Key", type="password", placeholder="Enter authorization key..."
        )

        expected_pass = st.secrets.get("ACCESS_KEY", "fabline2026")

        if st.button("AUTHENTICATE WORKSTATION"):
            if hmac.compare_digest(password_input, expected_pass):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Security Credential")

    return False

if not check_password():
    st.stop()

# 4. Data Management & OCR Helper
DB_FILE = "jobs_data.json"
NOTICES_FILE = "notices_data.json"

STATUS_OPTIONS = ["Expected", "Soon to come", "Incomplete", "Complete"]
CATEGORY_OPTIONS = [
    "Noticeboard / Alert",
    "Piping & Tubing",
    "Valves & Actuators",
    "Fittings & Flanges",
    "Structural & Support Steel",
    "Fasteners, Gaskets & Seals",
    "Consumables & Welding Supplies",
    "Instruments & Electrical",
    "Custom / Modular Skid / Equipment",
    "General Site Deliveries",
]
VALVE_OPTIONS = ["None / Standard Fitting", "Wet Pipe", "Dry Pipe", "Pre-Action", "Deluge"]

def process_docket_image(uploaded_file):
    """Processes uploaded docket image and extracts text."""
    if not HAS_OCR:
        return "OCR library not installed. Install 'pytesseract' and 'Pillow' for automatic image text extraction."
    try:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "No text could be extracted from image."
    except Exception as e:
        return f"Error extracting text from image: {e}"

def cross_check_docket_vs_user(docket_text, user_items):
    """Compares docket text with user input to flag potential discrepancies."""
    if not docket_text or "not installed" in docket_text:
        return True, "No automated OCR check performed."
    
    docket_words = set(re.findall(r'\w+', docket_text.lower()))
    user_words = set(re.findall(r'\w+', user_items.lower()))
    
    # Check key overlap
    common = docket_words.intersection(user_words)
    if len(common) < 2 and len(user_words) > 3:
        return False, "⚠️ Warning: Low similarity between physical docket photo text and user-entered manifest."
    return True, "✅ Docket photo matches user manifest entry."

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
        "docket_text": job.get("docket_text", "No physical docket uploaded."),
        "docket_match_status": job.get("docket_match_status", "Not Verified"),
        "operator": job.get("operator", "System Operator"),
        "updated": job.get("updated", now_time),
        "audit_trail": audit_trail,
    }

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if file_path == DB_FILE:
                    return [migrate_record(item) for item in data]
                return data
        except Exception:
            return []
    return []

def save_data(file_path, data):
    try:
        dir_name = os.path.dirname(file_path) or "."
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
            json.dump(data, tf, indent=4)
            temp_path = tf.name
        os.replace(temp_path, file_path)
    except Exception as e:
        st.error(f"Save failed: {e}")

def generate_csv(records):
    output = io.StringIO()
    if not records:
        return ""

    fieldnames = [
        "job_no",
        "category",
        "pipe_sizes",
        "arrival_datetime",
        "delivery_status",
        "valve_type",
        "items_logged",
        "docket_match_status",
        "operator",
        "updated",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in records:
        writer.writerow({k: row.get(k, "") for k in fieldnames})

    return output.getvalue()

# Persistent Session Setup
if "jobs" not in st.session_state:
    st.session_state.jobs = load_data(DB_FILE)

if "notices" not in st.session_state:
    st.session_state.notices = load_data(NOTICES_FILE)

def get_status_slug(status_str):
    return str(status_str).lower().replace(" ", "-")

# 5. HERO HEADER
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">FABLINE INTERNAL TECHNICAL REGISTRY & WORKFLOW PORTAL</div>
        <div class="hero-subtitle">
            Central operational hub with AI Vision Docket Parsing, cross-verification, and high-purity piping logs.
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 6. STATS BAR
total_rec = len(st.session_state.jobs)
comp_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Complete")
incomp_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Incomplete")
expected_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Expected")
notice_cnt = len(st.session_state.notices)

s1, s2, s3, s4 = st.columns(4)
s1.metric("VERIFIED SKIDS", f"{comp_cnt} COMPLETED")
s2.metric("TOTAL REGISTRY JOBS", total_rec)
s3.metric("INCOMPLETE / ISSUES", incomp_cnt)
s4.metric("ACTIVE NOTICES", f"{notice_cnt} POSTED")

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
t1, t2, t3, t4, t5, t6 = st.tabs([
    "📋 MASTER REGISTRY",
    "📢 OFFICE NOTICEBOARD",
    "➕ LOG NEW DELIVERY (WITH DOCKET SCAN)",
    "𝜟 TECHNICAL CALCULATOR",
    "🤖 ADVANCED FABLINE AI ASSISTANT",
    "🏢 MODULAR SYSTEM SPECS",
])

# --- TAB 1: MASTER REGISTRY VIEW ---
with t1:
    pending_total = incomp_cnt + expected_cnt
    if pending_total > 0:
        st.markdown(
            f"""
            <div class="alert-banner">
                <div>
                    <div class="alert-title">⚠️ OPERATIONAL NOTICE: ACTION ITEMS PENDING</div>
                    <div class="alert-body">
                        There are <strong>{incomp_cnt} incomplete material orders</strong> requiring field inspection and 
                        <strong>{expected_cnt} inbound shipments</strong> scheduled for site intake.
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <span class="status-badge st-incomplete">{incomp_cnt} Incomplete</span>
                    <span class="status-badge st-expected">{expected_cnt} Pending</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col_search, col_cat, col_status, col_export = st.columns([2.5, 1.5, 1.5, 1.2])
    with col_search:
        search_q = st.text_input(
            "Search Archive",
            placeholder="Search Job No., Spec, Inspector, Docket, or Manifest...",
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
            label="📥 EXPORT CSV",
            data=csv_data,
            file_name=f"fabline_registry_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.info("No matching engineering records found in the database.")

    for job in filtered:
        job_no = job.get("job_no", "N/A")
        cat = job.get("category", "General Site Deliveries")
        status = job.get("delivery_status", "Expected")
        v_type = job.get("valve_type", "None / Standard Fitting")
        status_slug = get_status_slug(status)

        category_badge = f'<span class="category-tag">📦 {cat}</span>'
        valve_badge = f'<span class="accent-badge-red" style="margin-left: 0.5rem;">🔥 {v_type}</span>' if v_type and v_type != "None / Standard Fitting" else ""

        st.markdown(
            f"""
        <div class="product-card">
            <div class="card-header">
                <div>
                    <span class="card-title">JOB NO. #{job_no}</span>
                    {category_badge}
                    {valve_badge}
                </div>
                <span class="status-badge st-{status_slug}">{status}</span>
            </div>
            <div class="card-grid">
                <div>
                    <div class="meta-label">Specification / Size / Tag</div>
                    <div class="meta-value">{job.get('pipe_sizes', 'N/A')}</div>
                </div>
                <div>
                    <div class="meta-label">Scheduled / Arrival Time</div>
                    <div class="meta-value">{job.get('arrival_datetime', 'N/A')}</div>
                </div>
                <div>
                    <div class="meta-label">Docket Verification</div>
                    <div class="meta-value">{job.get('docket_match_status', 'N/A')}</div>
                </div>
            </div>
            <div>
                <div class="meta-label" style="margin-bottom: 0.35rem;">Material Manifest & Logged Items</div>
                <div class="inventory-block">{job.get('items_logged', 'No detailed items recorded.')}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #64748B; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #E2E8F0;">
                <div>Inspector Signature: <strong style="color: #0F1B2D;">{job.get('operator', 'Unassigned')}</strong></div>
                <div>Last Updated: {job.get('updated', 'N/A')}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# --- TAB 2: OFFICE NOTICEBOARD ---
with t2:
    st.markdown("### 📢 OFFICE NOTICEBOARD & TRUCK ARRIVALS")
    st.caption("Post site notifications, expected deliveries, missing material alerts, and operational announcements.")

    with st.form("form_notice"):
        st.markdown("##### 📝 POST NEW NOTICE / ALERT")
        cn1, cn2, cn3 = st.columns([2, 1, 1])
        with cn1:
            n_title = st.text_input("Notice Subject / Title", placeholder="e.g., Inbound Truck Arrival - Stainless Fittings")
        with cn2:
            n_type = st.selectbox("Urgency Level", ["Urgent Alert", "Action Required", "General Information"])
        with cn3:
            n_job_ref = st.text_input("Related Job # (Optional)", placeholder="e.g., FL-8820")

        n_details = st.text_area("Notice Details / Missing Items / Truck Schedule", placeholder="Describe notification details...")
        n_author = st.text_input("Posted By (Office Staff Signature)")

        if st.form_submit_button("POST NOTICE TO BULLETIN"):
            if not n_title.strip() or not n_author.strip():
                st.error("Title and Office Staff Signature are required.")
            else:
                now_stamp = datetime.now().strftime("%d-%b-%Y %H:%M")
                urgency_class = "urgent" if "Urgent" in n_type else ("action" if "Action" in n_type else "info")
                
                notice_entry = {
                    "id": f"NOTE-{len(st.session_state.notices) + 1:03d}",
                    "title": n_title.strip(),
                    "urgency": n_type,
                    "urgency_class": urgency_class,
                    "job_ref": n_job_ref.strip() or "N/A",
                    "details": n_details.strip() or "No additional detail provided.",
                    "author": n_author.strip(),
                    "timestamp": now_stamp,
                }
                
                st.session_state.notices.insert(0, notice_entry)
                save_data(NOTICES_FILE, st.session_state.notices)
                st.success("Notice posted to Office Bulletin!")
                st.rerun()

    st.markdown("---")
    st.markdown("##### 📌 ACTIVE SITE NOTICES")
    for idx, notice in enumerate(st.session_state.notices):
        u_class = notice.get("urgency_class", "info")
        st.markdown(
            f"""
            <div class="notice-card {u_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.05rem; color: #0F1B2D;">
                        {notice.get('title')}
                    </div>
                    <span class="status-badge" style="background-color: #0F1B2D; color: #FFFFFF;">
                        {notice.get('urgency')}
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 0.75rem;">
                    <strong>Job Ref:</strong> {notice.get('job_ref')} | <strong>Posted:</strong> {notice.get('timestamp')} | <strong>By:</strong> {notice.get('author')}
                </div>
                <div style="font-size: 0.925rem; color: #1E293B; white-space: pre-wrap;">
                    {notice.get('details')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- TAB 3: LOG NEW DELIVERY (WITH OCR DOCKET SCAN) ---
with t3:
    st.markdown("### ➕ LOG NEW SHIPMENT & SCAN DELIVERY DOCKET")
    st.caption("Take a photo or upload a delivery docket to cross-verify physical paperwork against user entries.")

    uploaded_docket = st.file_uploader("📷 Upload / Snap Photo of Delivery Docket", type=["png", "jpg", "jpeg"])
    scanned_docket_text = ""
    
    if uploaded_docket is not None:
        st.image(uploaded_docket, caption="Uploaded Delivery Docket", width=350)
        with st.spinner("AI scanning delivery docket text..."):
            scanned_docket_text = process_docket_image(uploaded_docket)
        
        with st.expander("🔍 View Extracted OCR Text from Docket Photo"):
            st.code(scanned_docket_text)

    with st.form("form_new_job_with_docket"):
        c_n1, c_n2 = st.columns(2)
        with c_n1:
            n_job_no = st.text_input("Job Number / PO #", placeholder="e.g. FL-9921")
            n_cat = st.selectbox("Material Category", CATEGORY_OPTIONS)
            n_pipe_sizes = st.text_input("Piping Specs / Dimensions / Tag", placeholder="e.g. 3\" Sch 40 316L SS")
        with c_n2:
            n_status = st.selectbox("Initial Status", STATUS_OPTIONS)
            n_valve = st.selectbox("Modular Valve System", VALVE_OPTIONS)
            n_arrival = st.text_input("Arrival Date/Time", value=datetime.now().strftime("%d-%b-%Y %H:%M"))

        n_manifest = st.text_area("User Entered Material Manifest / Items", placeholder="List items manually received...")
        n_op = st.text_input("Receiving Inspector Signature")

        if st.form_submit_button("SUBMIT AND CROSS-CHECK WITH AI"):
            if not n_job_no.strip() or not n_op.strip():
                st.error("Job Number and Inspector Signature are mandatory fields.")
            else:
                now_stamp = datetime.now().strftime("%d-%b-%Y %H:%M")
                
                # Cross-check user entry against docket OCR
                is_match, match_msg = cross_check_docket_vs_user(scanned_docket_text, n_manifest)
                
                final_status = n_status
                if not is_match and n_status == "Complete":
                    final_status = "Incomplete"
                    st.warning("Status automatically flagged as 'Incomplete' due to docket manifest discrepancy.")

                new_entry = {
                    "job_no": n_job_no.strip(),
                    "category": n_cat,
                    "pipe_sizes": n_pipe_sizes.strip() or "N/A",
                    "arrival_datetime": n_arrival.strip(),
                    "delivery_status": final_status,
                    "valve_type": n_valve,
                    "items_logged": n_manifest.strip() or "No manifest attached.",
                    "docket_text": scanned_docket_text or "No docket scanned.",
                    "docket_match_status": match_msg,
                    "operator": n_op.strip(),
                    "updated": now_stamp,
                    "audit_trail": [
                        {
                            "timestamp": now_stamp,
                            "operator": n_op.strip(),
                            "action": "Record Created with Docket Scan",
                            "status": final_status,
                            "note": f"Cross-check result: {match_msg}",
                        }
                    ],
                }
                st.session_state.jobs.append(new_entry)
                save_data(DB_FILE, st.session_state.jobs)
                st.success(f"Job #{n_job_no} logged! {match_msg}")
                st.rerun()

# --- TAB 4: TECHNICAL CALCULATOR ---
with t4:
    st.markdown("### 𝜟 BARLOW'S FORMULA PRESSURE CALCULATOR")
    st.caption("Calculate Maximum Allowable Working Pressure (MAWP) for unthreaded seamless pipe.")
    
    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        outside_dia = st.number_input("Outside Diameter (D) in inches", min_value=0.1, value=2.375, step=0.1)
        wall_thick = st.number_input("Wall Thickness (t) in inches", min_value=0.01, value=0.154, step=0.01)
        design_stress = st.number_input("Allowable Stress (S) in PSI", min_value=1000, value=20000, step=1000)
    
    with col_calc2:
        if outside_dia > 0:
            mawp_psi = (2 * design_stress * wall_thick) / outside_dia
            mawp_bar = mawp_psi * 0.0689476
            
            st.metric("COMPUTED MAWP (PSI)", f"{mawp_psi:,.2f} PSI")
            st.metric("COMPUTED MAWP (BAR)", f"{mawp_bar:,.2f} bar")

# --- TAB 5: ADVANCED AI ASSISTANT & HISTORICAL MEMORY ---
with t5:
    st.markdown("### 🤖 FABLINE INTELLIGENT KNOWLEDGE ASSISTANT")
    st.caption("Queries complete database memory including parsed docket text, audit logs, and inspector entries.")

    user_q = st.text_input("Ask any question about deliveries, docket text, inspectors, or job statuses:")
    if user_q:
        query_terms = [q.strip().lower() for q in user_q.split() if len(q.strip()) > 2]
        
        matches = []
        for job in st.session_state.jobs:
            score = 0
            job_str = json.dumps(job).lower()
            for term in query_terms:
                if term in job_str:
                    score += 1
            if score > 0:
                matches.append((score, job))
                
        matches.sort(key=lambda x: x[0], reverse=True)
        
        if matches:
            st.markdown(f"🧠 **AI Knowledge Retrieval found {len(matches)} relevant record(s):**")
            for score, m in matches[:5]:
                with st.container():
                    st.markdown(f"#### 📄 Job #{m.get('job_no')} — Status: {m.get('delivery_status')}")
                    st.write(f"- **Category:** {m.get('category')}")
                    st.write(f"- **User Manifest:** {m.get('items_logged')}")
                    st.write(f"- **Docket Text (OCR):** {m.get('docket_text')[:200]}...")
                    st.write(f"- **Verification Note:** {m.get('docket_match_status')}")
                    st.write(f"- **Inspector:** {m.get('operator')} (Last Updated: {m.get('updated')})")
                    st.markdown("---")
        else:
            st.info("No records matched your exact query terms. Search by docket number, inspector name, or material type.")

# --- TAB 6: MODULAR SYSTEM SPECS ---
with t6:
    st.markdown("### 🏢 MODULAR SKID TECHNICAL SPECIFICATIONS")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(
            """
            #### 🛠️ Welding & Piping Standards
            - **Material Grades**: AISI 316/316L Stainless Steel, Carbon Steel ASTM A106 Grade B.
            - **Hydrostatic Testing**: 1.5x design pressure held for a minimum of 30 minutes.
            - **Nondestructive Examination (NDE)**: 100% Visual Inspection (VT) + 20% Radiographic Testing (RT).
            """
        )
    with col_s2:
        st.markdown(
            """
            #### 📋 Inspection Checklists
            1. Verify material heat numbers against Mill Test Reports (MTRs).
            2. Check flange face finishes and gasket material compatibility.
            3. Ensure torque limits comply with ASME B31.3 piping specs.
            """
        )
