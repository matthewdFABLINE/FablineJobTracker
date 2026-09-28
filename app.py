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
    page_title="Fabline Internal Operations & Technical Registry",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Design System: Professional Industrial Engineering Palette (Navy, Steel, Red, White)
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --navy-dark: #0F1B2D;
        --navy-surface: #1E293B;
        --navy-subtle: #0f172a;
        
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

    * { box-sizing: border-box !important; }

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

    /* INDUSTRIAL GEOMETRIC HEADINGS */
    h1, h2, h3, .heading-industrial {
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        font-weight: 800 !important;
    }

    /* 🏛️ NAVY HERO HEADER */
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
        margin-bottom: 1.5rem;
    }

    .hero-cta-group {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        align-items: center;
    }

    .btn-cta-primary {
        background-color: var(--crimson-red) !important;
        color: var(--pure-white) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 0.85rem !important;
        padding: 0.7rem 1.4rem !important;
        border-radius: 6px !important;
        border: none !important;
        cursor: pointer;
        transition: all 0.2s ease !important;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .btn-cta-primary:hover {
        background-color: var(--crimson-hover) !important;
        box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4) !important;
    }

    .btn-cta-secondary {
        background-color: transparent !important;
        color: var(--pure-white) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 0.85rem !important;
        padding: 0.7rem 1.4rem !important;
        border-radius: 6px !important;
        border: 2px solid var(--pure-white) !important;
        cursor: pointer;
        transition: all 0.2s ease !important;
    }

    .btn-cta-secondary:hover {
        background-color: var(--pure-white) !important;
        color: var(--navy-dark) !important;
    }

    /* 📊 CREDIBILITY & STATS BAR */
    .stats-bar {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        background: var(--pure-white);
        border: 1px solid var(--steel-border);
        border-left: 4px solid var(--navy-dark);
        border-radius: 8px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    }

    .stat-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--steel-gray);
        margin-bottom: 0.25rem;
    }

    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--navy-dark);
    }

    /* STREAMLIT NATIVE METRIC OVERRIDES */
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

    /* 🏷️ BADGES & CARDS */
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

    /* FORM & TAB CONTROLS */
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

    input, textarea, select, div[data-baseweb="select"] {
        background-color: var(--pure-white) !important;
        color: var(--navy-dark) !important;
        border: 1px solid var(--steel-border) !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
    }

    input:focus, textarea:focus {
        border-color: var(--navy-dark) !important;
        box-shadow: 0 0 0 2px rgba(15, 27, 45, 0.15) !important;
    }

    /* BUTTON STYLING */
    button, 
    div[data-testid="stDownloadButton"] button, 
    div[data-testid="stFormSubmitButton"] button {
        background-color: var(--navy-dark) !important;
        color: var(--pure-white) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        font-size: 0.85rem !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    button:hover, 
    div[data-testid="stDownloadButton"] button:hover, 
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: var(--crimson-red) !important;
        color: var(--pure-white) !important;
        box-shadow: 0 4px 10px rgba(211, 47, 47, 0.3) !important;
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

    /* AI CHAT ENHANCEMENTS */
    .chat-bubble-user {
        background-color: #E2E8F0;
        border: 1px solid var(--steel-border);
        border-radius: 8px;
        padding: 0.85rem 1.1rem;
        margin-bottom: 0.75rem;
        color: var(--navy-dark);
        max-width: 85%;
        margin-left: auto;
        font-size: 0.925rem;
    }

    .chat-bubble-agent {
        background-color: var(--pure-white);
        border: 1px solid var(--steel-border);
        border-left: 4px solid var(--navy-dark);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.25rem;
        color: var(--navy-dark);
        max-width: 90%;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }

    .chat-agent-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 800;
        color: var(--crimson-red);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
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


def fabline_ai_response(user_query, jobs_data):
    query_lower = user_query.lower()
    matched_records = [j for j in jobs_data if query_lower in str(j).lower()]
    
    response_text = ""
    if "pressure" in query_lower or "barlow" in query_lower or "mawp" in query_lower:
        response_text += "💡 **Technical Guidance:** Standard MAWP values are derived via Barlow's Formula ($P = \\frac{2St}{D}$). Refer to the **𝜟 Technical Calculator** tab to compute verified code pressures for high-purity assemblies.\n\n"
    elif "valve" in query_lower or "skid" in query_lower:
        response_text += "🏷️ **Modular Systems Reference:** Fabline standard skids include *Wet Pipe*, *Dry Pipe*, *Pre-Action*, and *Deluge* configurations compliant with NFPA guidelines.\n\n"

    if matched_records:
        response_text += f"🔍 **Found {len(matched_records)} matching record(s) in the Fabline Registry:**\n\n"
        for idx, rec in enumerate(matched_records[:5], 1):
            response_text += (
                f"**{idx}. Job No. #{rec.get('job_no')}** ({rec.get('category')})\n"
                f"- **Status:** {rec.get('delivery_status')}\n"
                f"- **Specs/Tag:** {rec.get('pipe_sizes')}\n"
                f"- **Arrival:** {rec.get('arrival_datetime')}\n"
                f"- **Inspector:** {rec.get('operator')}\n"
                f"- **Manifest:** {rec.get('items_logged')[:120]}...\n\n"
            )
        if len(matched_records) > 5:
            response_text += f"*...and {len(matched_records) - 5} additional record(s).* Refine query for specific job numbers."
    else:
        if not response_text:
            response_text = f"I searched the registry for **\"{user_query}\"** but found no direct matches.\n\nYou can query by **Job Number**, **Material Type** (e.g. *Stainless Steel*, *Flange*, *Beam*), **Inspector Name**, or **Status**."

    return response_text, matched_records


if "jobs" not in st.session_state:
    st.session_state.jobs = load_data()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "agent",
            "content": "👋 **Fabline Internal Operations Assistant.** Ready to look up jobs, cross-reference material manifests, or check modular valve skid specs. How can I assist your shift today?"
        }
    ]


def get_status_slug(status_str):
    return str(status_str).lower().replace(" ", "-")


# 5. HERO HEADER SECTION (Navy Blue + Modern Operational Focus)
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">FABLINE INTERNAL TECHNICAL REGISTRY & WORKFLOW PORTAL</div>
        <div class="hero-subtitle">
            Central operational hub for high-purity piping logs, modular skid fabrication tracking, and on-site material intake. 
            Use this portal to register deliveries, verify pressure specs, and audit compliance logs.
        </div>
        <div class="hero-cta-group">
            <button class="btn-cta-primary" onclick="window.location.href='#new-shipment';">
                ➕ LOG NEW SHIPMENT
            </button>
            <button class="btn-cta-secondary" onclick="window.location.href='#modular-systems';">
                📋 MODULAR SYSTEM SPECS
            </button>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 6. STATS / CREDIBILITY BAR
total_rec = len(st.session_state.jobs)
comp_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Complete")
incomp_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Incomplete")
expected_cnt = sum(1 for j in st.session_state.jobs if j.get("delivery_status") == "Expected")

s1, s2, s3, s4 = st.columns(4)
s1.metric("VERIFIED SKIDS", f"{comp_cnt} COMPLETED")
s2.metric("TOTAL REGISTRY JOBS", total_rec)
s3.metric("INCOMPLETE / ISSUES", incomp_cnt)
s4.metric("INBOUND DELIVERIES", expected_cnt)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
t1, t2, t3, t4, t5 = st.tabs([
    "📋 MASTER REGISTRY",
    "➕ LOG NEW DELIVERY",
    "𝜟 TECHNICAL CALCULATOR",
    "🤖 FABLINE AI ASSISTANT",
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
            placeholder="Search Job No., Spec, Inspector, or Manifest...",
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

        with st.expander(f"⚙️ Manage & Audit Trail — #{job_no}"):
            st.markdown("##### 📜 CHAIN OF CUSTODY AUDIT LOG")
            trail = job.get("audit_trail", [])
            if trail:
                for event in reversed(trail):
                    st.markdown(
                        f"""
                        <div style="border-left: 3px solid #0F1B2D; padding-left: 0.85rem; margin-bottom: 0.75rem;">
                            <div style="font-size: 0.75rem; color: #64748B; font-weight: 700;">🕒 {event.get('timestamp', 'N/A')}</div>
                            <div style="font-size: 0.85rem; color: #0F1B2D; font-weight: 700;">👤 {event.get('operator', 'System')} - {event.get('action', 'Update')} <span class="status-badge st-{get_status_slug(event.get('status'))}" style="font-size: 0.65rem;">{event.get('status')}</span></div>
                            <div style="font-size: 0.85rem; color: #475569; margin-top: 0.15rem;">{event.get('note', 'No notes.')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No historical audit steps recorded.")

            st.markdown("---")
            st.markdown("##### ✏️ UPDATE RECORD DETAILS")

            with st.form(f"form_update_{job_no}"):
                default_st_idx = STATUS_OPTIONS.index(status) if status in STATUS_OPTIONS else 0
                default_v_idx = VALVE_OPTIONS.index(v_type) if v_type in VALVE_OPTIONS else 0
                default_cat_idx = CATEGORY_OPTIONS.index(cat) if cat in CATEGORY_OPTIONS else 0

                c_u1, c_u2, c_u3 = st.columns(3)
                with c_u1:
                    new_st = st.selectbox("Delivery Status", STATUS_OPTIONS, index=default_st_idx)
                with c_u2:
                    new_cat = st.selectbox("Category", CATEGORY_OPTIONS, index=default_cat_idx)
                with c_u3:
                    new_vt = st.selectbox("Valve System", VALVE_OPTIONS, index=default_v_idx)

                new_txt = st.text_area(
                    "Append Field Inspection Notes",
                    placeholder="e.g., Hydrostatic pressure test passed at 300 PSI.",
                )
                up_op = st.text_input("Inspector Name / ID Signature")

                if st.form_submit_button("SAVE CHANGES & UPDATE AUDIT LOG"):
                    if not up_op.strip():
                        st.error("Inspector signature is required to verify changes.")
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
                                
                                action_msg = f"Status changed from '{old_st}' to '{new_st}'" if old_st != new_st else "Updated record specs"
                                note_entry = new_txt.strip() if new_txt.strip() else "Inspection details updated."
                                
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
                                        "action": action_msg,
                                        "status": new_st,
                                        "note": note_entry,
                                    }
                                )
                                break
                        save_data(st.session_state.jobs)
                        st.success("Record updated successfully!")
                        st.rerun()

# --- TAB 2: ARCHIVE NEW RECORD ---
with t2:
    st.markdown("<h3 class='heading-industrial' id='new-shipment'>➕ REGISTER NEW SHIPMENT OR FABRICATION JOB</h3>", unsafe_allow_html=True)
    st.write("Scan physical packing slips using AI OCR or manually enter material details into the database.")

    if HAS_OCR:
        st.markdown('<div style="background-color: #FFFFFF; border: 1px dashed #64748B; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
        st.markdown("<h5 class='heading-industrial' style='font-size: 0.9rem;'>📷 OCR DELIVERY DOCKET SCANNER</h5>", unsafe_allow_html=True)
        uploaded_img = st.file_uploader("Upload Docket / Packing Slip Photo", type=["png", "jpg", "jpeg"])
        
        ocr_job_no, ocr_manifest = "", ""
        if uploaded_img is not None:
            with st.spinner("Extracting text from docket image..."):
                img_bytes = uploaded_img.read()
                ocr_job_no, ocr_manifest = parse_docket_image(img_bytes)
                st.success("Docket Text Processed!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        ocr_job_no, ocr_manifest = "", ""

    with st.form("new_record_form"):
        c1, c2 = st.columns(2)
        with c1:
            in_job_no = st.text_input("Job / Docket Number", value=ocr_job_no, placeholder="e.g. JOB-9901")
            in_category = st.selectbox("Category", CATEGORY_OPTIONS)
            in_pipe_sizes = st.text_input("Specifications / Dimensions", placeholder="e.g. 4\" Schedule 80 316L SS Flanged")
            in_arrival = st.text_input("Arrival Date & Time", value=datetime.now().strftime("%d-%b-%Y %H:%M"))
        with c2:
            in_status = st.selectbox("Initial Delivery Status", STATUS_OPTIONS)
            in_valve = st.selectbox("Fire Safety Valve Classification", VALVE_OPTIONS)
            in_operator = st.text_input("Inspector Signature / ID", placeholder="e.g. Inspector R. Vance")

        st.markdown("##### 📦 MATERIAL MANIFEST / INVENTORY")
        in_manifest = st.text_area("Detailed Bill of Materials", value=ocr_manifest, height=120, placeholder="- 12x 4\" ANSI 150# Flanges\n- 24x High-Temp Gaskets")

        if st.form_submit_button("REGISTER JOB ENTRY", use_container_width=True):
            if not in_job_no.strip() or not in_operator.strip():
                st.error("Job Number and Inspector Signature are required.")
            else:
                now_stamp = datetime.now().strftime("%d-%b-%Y %H:%M")
                new_entry = {
                    "job_no": in_job_no.strip(),
                    "category": in_category,
                    "pipe_sizes": in_pipe_sizes.strip() or "N/A",
                    "arrival_datetime": in_arrival.strip(),
                    "delivery_status": in_status,
                    "valve_type": in_valve,
                    "items_logged": in_manifest.strip() or "No manifest documented.",
                    "operator": in_operator.strip(),
                    "updated": now_stamp,
                    "audit_trail": [
                        {
                            "timestamp": now_stamp,
                            "operator": in_operator.strip(),
                            "action": "Record Created",
                            "status": in_status,
                            "note": "Initial logging into Fabline database.",
                        }
                    ],
                }
                st.session_state.jobs.insert(0, new_entry)
                save_data(st.session_state.jobs)
                st.success(f"Job #{in_job_no} registered successfully!")
                st.rerun()

# --- TAB 3: TECHNICAL CALCULATOR ---
with t3:
    st.markdown("<h3 class='heading-industrial'>𝜟 PIPING MAWP PRESSURE CALCULATOR</h3>", unsafe_allow_html=True)
    st.write("Calculate Maximum Allowable Working Pressure (MAWP) per ASME B31.3 using Barlow's Formula.")

    c_calc1, c_calc2 = st.columns(2)
    with c_calc1:
        outer_d = st.number_input("Nominal Outside Diameter ($D$) in inches", min_value=0.1, value=2.375, step=0.1)
        wall_t = st.number_input("Nominal Wall Thickness ($t$) in inches", min_value=0.01, value=0.154, step=0.01)
        stress_s = st.number_input("Allowable Stress ($S$) in PSI", min_value=1000, value=20000, step=1000)

    with c_calc2:
        if outer_d > 0:
            mawp = (2 * stress_s * wall_t) / outer_d
            st.metric("MAX ALLOWABLE WORKING PRESSURE", f"{mawp:.2f} PSI")
            st.write(f"Equivalent Metric Pressure: **{(mawp * 0.0689476):.2f} Bar**")
            st.info("Formula applied: $P = \\frac{2St}{D}$ per ASME B31.3 Code Guidelines.")

# --- TAB 4: AI ASSISTANT ---
with t4:
    st.markdown("<h3 class='heading-industrial'>🤖 FABLINE AI SITE ASSISTANT</h3>", unsafe_allow_html=True)
    st.write("Query material records, code compliance specs, or internal modular valve skid references.")

    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="chat-bubble-agent"><div class="chat-agent-header">🤖 FABLINE SUPPORT AI</div>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )

    user_input = st.chat_input("Ask about jobs, valve systems, MAWP specs, or audit logs...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        agent_reply, _ = fabline_ai_response(user_input, st.session_state.jobs)
        st.session_state.chat_messages.append({"role": "agent", "content": agent_reply})
        st.rerun()

# --- TAB 5: MODULAR SYSTEM SPECS ---
with t5:
    st.markdown("<h3 class='heading-industrial' id='modular-systems'>🏢 PRE-FABRICATED MODULAR SKID SPECIFICATIONS</h3>", unsafe_allow_html=True)
    st.write("Internal engineering reference guides for standard pre-commissioned skid packages and NFPA valve assemblies.")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            """
            <div class="product-card">
                <div class="card-header">
                    <span class="card-title">WET PIPE VALVE SKIDS</span>
                    <span class="accent-badge-red">STANDARD PROTECTION</span>
                </div>
                <p style="font-size: 0.9rem; color: #475569;">
                    Permanently pressurized water systems designed for immediate activation. Built with high-grade ductile iron body valves and pressure switches.
                </p>
                <div class="meta-label">KEY TECHNICAL SPECIFICATIONS</div>
                <div class="meta-value" style="font-size: 0.85rem;">• Working Pressure: Up to 17.5 Bar (250 PSI)<br>• NFPA 13 Compliant<br>• Pre-wired alarm trim line</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="product-card">
                <div class="card-header">
                    <span class="card-title">DRY PIPE VALVE SKIDS</span>
                    <span class="accent-badge-red">FREEZE-PROOF DESIGN</span>
                </div>
                <p style="font-size: 0.9rem; color: #475569;">
                    Pressurized with nitrogen/air for environments subject to freezing temperatures. Includes automatic air maintenance devices.
                </p>
                <div class="meta-label">KEY TECHNICAL SPECIFICATIONS</div>
                <div class="meta-value" style="font-size: 0.85rem;">• Differential Latch Mechanism<br>• Integrated Air Compressor Port<br>• Temperature Rating: -10°C to +60°C</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with p2:
        st.markdown(
            """
            <div class="product-card">
                <div class="card-header">
                    <span class="card-title">PRE-ACTION SYSTEMS</span>
                    <span class="accent-badge-red">HIGH-VALUE HAZARD</span>
                </div>
                <p style="font-size: 0.9rem; color: #475569;">
                    Dual-interlock system combining electric detection with sprinkler activation. Ideal for data centers, cleanrooms, and archives.
                </p>
                <div class="meta-label">KEY TECHNICAL SPECIFICATIONS</div>
                <div class="meta-value" style="font-size: 0.85rem;">• Solenoid Actuated Deluge Valve<br>• Double-Interlock Safety Safeguard<br>• Pre-commissioned Control Panel</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="product-card">
                <div class="card-header">
                    <span class="card-title">DELUGE VALVE SKIDS</span>
                    <span class="accent-badge-red">HIGH-HAZARD SURGE</span>
                </div>
                <p style="font-size: 0.9rem; color: #475569;">
                    Unpressurized open-spray nozzle systems engineered for immediate, high-volume fire suppression in chemical processing plants.
                </p>
                <div class="meta-label">KEY TECHNICAL SPECIFICATIONS</div>
                <div class="meta-value" style="font-size: 0.85rem;">• Fast-opening hydraulic diaphragm<br>• High-flow capacity (Cv rated)<br>• Seawater / Stainless Steel Options</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
