import streamlit as st
import json
import os
import csv
import io
import hmac
from datetime import datetime, date

# ============================================================
# FABLINE OPERATIONS
# Jobs • Inventory • Deliveries • Material Readiness
# ============================================================

st.set_page_config(
    page_title="Fabline Operations",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CONFIGURATION
# ============================================================

DB_FILE = "fabline_operations.json"

JOB_STATUSES = [
    "Awaiting Material",
    "Partially Received",
    "Material Ready",
    "In Fabrication",
    "Awaiting Inspection",
    "Ready for Dispatch",
    "Complete",
]

UNITS = [
    "pcs",
    "m",
    "mm",
    "kg",
    "sets",
    "boxes",
    "lengths",
]

CATEGORIES = [
    "Piping & Tubing",
    "Valves & Actuators",
    "Fittings & Flanges",
    "Structural & Support Steel",
    "Fasteners, Gaskets & Seals",
    "Consumables & Welding Supplies",
    "Instruments & Electrical",
    "Custom Equipment",
    "General",
]


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
<style>

:root {
    --navy: #111827;
    --navy2: #1f2937;
    --orange: #e56b09;
    --orange2: #f97316;
    --bg: #f4f6f8;
    --card: #ffffff;
    --border: #e5e7eb;
    --muted: #6b7280;
    --green: #16834b;
    --red: #c62828;
    --amber: #b45309;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    font-family: Inter, Arial, sans-serif;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

/* HEADER */

.fab-header {
    background:
        linear-gradient(120deg, #111827, #1f2937);
    border-radius: 16px;
    padding: 25px 30px;
    color: white;
    margin-bottom: 18px;
    border-bottom: 5px solid #e56b09;
    box-shadow: 0 8px 25px rgba(0,0,0,.12);
}

.fab-title {
    font-size: 30px;
    font-weight: 900;
    letter-spacing: -.5px;
}

.fab-subtitle {
    color: #cbd5e1;
    margin-top: 5px;
    font-size: 14px;
}

/* KPI */

.kpi {
    background: white;
    padding: 18px;
    border-radius: 13px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,.04);
    min-height: 105px;
}

.kpi-label {
    color: #6b7280;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .05em;
}

.kpi-number {
    font-size: 31px;
    font-weight: 900;
    margin-top: 4px;
    color: #111827;
}

.kpi-note {
    color: #6b7280;
    font-size: 12px;
}

/* JOB CARDS */

.job-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 13px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 2px 7px rgba(0,0,0,.04);
}

.job-title {
    font-size: 19px;
    font-weight: 900;
    color: #111827;
}

.job-client {
    color: #6b7280;
    font-size: 14px;
}

.ready {
    color: #16834b;
    font-weight: 800;
}

.missing {
    color: #c62828;
    font-weight: 800;
}

/* PROGRESS */

.progress-bg {
    background: #e5e7eb;
    border-radius: 20px;
    height: 11px;
    overflow: hidden;
    margin-top: 8px;
}

.progress-fill {
    background: linear-gradient(
        90deg,
        #e56b09,
        #f59e0b
    );
    height: 100%;
}

/* BADGES */

.badge {
    display: inline-block;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 800;
    margin-right: 5px;
}

.badge-red {
    background: #fee2e2;
    color: #991b1b;
}

.badge-green {
    background: #dcfce7;
    color: #166534;
}

.badge-orange {
    background: #ffedd5;
    color: #9a3412;
}

.badge-blue {
    background: #dbeafe;
    color: #1e40af;
}

/* INVENTORY */

.stock-card {
    background: white;
    padding: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    margin-bottom: 10px;
}

.stock-name {
    font-weight: 900;
    font-size: 16px;
}

/* STREAMLIT */

.stButton button {
    border-radius: 8px;
    font-weight: 700;
}

div[data-baseweb="tab-list"] {
    background: white;
    border-radius: 10px;
    padding: 5px;
    border: 1px solid #e5e7eb;
}

button[data-baseweb="tab"] {
    font-weight: 700;
}

hr {
    border-color: #e5e7eb;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

def blank_database():
    return {
        "jobs": [],
        "inventory": [],
        "deliveries": [],
        "notices": [],
        "audit": [],
    }


def load_database():
    if not os.path.exists(DB_FILE):
        return blank_database()

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        defaults = blank_database()

        for key in defaults:
            if key not in data:
                data[key] = defaults[key]

        return data

    except Exception:
        return blank_database()


def save_database():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(
            st.session_state.db,
            f,
            indent=4,
            ensure_ascii=False,
        )


if "db" not in st.session_state:
    st.session_state.db = load_database()


# ============================================================
# HELPERS
# ============================================================

def now():
    return datetime.now().strftime("%d-%b-%Y %H:%M")


def clean(value):
    return str(value).strip()


def inventory_by_sku(sku):

    for item in st.session_state.db["inventory"]:
        if item["sku"] == sku:
            return item

    return None


def job_by_number(job_no):

    for job in st.session_state.db["jobs"]:
        if job["job_no"] == job_no:
            return job

    return None


def total_reserved(sku, exclude_job=None):

    total = 0

    for job in st.session_state.db["jobs"]:

        if job["status"] == "Complete":
            continue

        if exclude_job and job["job_no"] == exclude_job:
            continue

        for req in job.get("requirements", []):

            if req["sku"] == sku:
                total += float(req["required"])

    return total


def available_stock(sku):

    item = inventory_by_sku(sku)

    if not item:
        return 0

    reserved = total_reserved(sku)

    return max(
        0,
        float(item["quantity"]) - reserved
    )


def requirement_available(job, req):

    item = inventory_by_sku(req["sku"])

    if not item:
        return 0

    other_reserved = total_reserved(
        req["sku"],
        exclude_job=job["job_no"],
    )

    remaining = (
        float(item["quantity"])
        - other_reserved
    )

    return max(
        0,
        min(
            float(req["required"]),
            remaining,
        ),
    )


def calculate_job(job):

    requirements = job.get(
        "requirements",
        []
    )

    if not requirements:

        return {
            "percent": 0,
            "ready": False,
            "missing": [],
        }

    required_total = 0
    supplied_total = 0
    missing = []

    for req in requirements:

        required = float(
            req["required"]
        )

        supplied = requirement_available(
            job,
            req,
        )

        required_total += required
        supplied_total += supplied

        shortage = max(
            0,
            required - supplied
        )

        if shortage > 0:

            missing.append({
                "sku": req["sku"],
                "description": req["description"],
                "missing": shortage,
                "unit": req["unit"],
            })

    if required_total:

        percent = int(
            min(
                100,
                (
                    supplied_total
                    / required_total
                ) * 100
            )
        )

    else:
        percent = 0

    return {
        "percent": percent,
        "ready": len(missing) == 0,
        "missing": missing,
    }


def automatic_material_status(job):

    result = calculate_job(job)

    if result["ready"] and job.get(
        "requirements"
    ):
        return "Material Ready"

    if result["percent"] > 0:
        return "Partially Received"

    return "Awaiting Material"


def update_automatic_statuses():

    protected = [
        "In Fabrication",
        "Awaiting Inspection",
        "Ready for Dispatch",
        "Complete",
    ]

    changed = False

    for job in st.session_state.db["jobs"]:

        if job["status"] not in protected:

            new_status = automatic_material_status(
                job
            )

            if job["status"] != new_status:

                job["status"] = new_status
                changed = True

    if changed:
        save_database()


def add_audit(
    action,
    details,
    job_no=""
):

    st.session_state.db[
        "audit"
    ].insert(
        0,
        {
            "timestamp": now(),
            "action": action,
            "details": details,
            "job_no": job_no,
        },
    )


# ============================================================
# DEMO DATA
# ============================================================

def load_demo():

    st.session_state.db = blank_database()

    st.session_state.db[
        "inventory"
    ] = [
        {
            "sku": "PIPE-DN50-316",
            "description": "DN50 316L Stainless Pipe",
            "category": "Piping & Tubing",
            "quantity": 126,
            "unit": "m",
            "location": "Rack B-04",
            "minimum": 40,
            "supplier": "Stainless Supplies",
        },
        {
            "sku": "VALVE-DN80-BF",
            "description": "DN80 Butterfly Valve",
            "category": "Valves & Actuators",
            "quantity": 3,
            "unit": "pcs",
            "location": "Valve Shelf 2",
            "minimum": 4,
            "supplier": "ABC Valves",
        },
        {
            "sku": "FLANGE-DN80-PN16",
            "description": "DN80 PN16 Flange",
            "category": "Fittings & Flanges",
            "quantity": 20,
            "unit": "pcs",
            "location": "Rack C-02",
            "minimum": 8,
            "supplier": "Pipe Components Ltd",
        },
        {
            "sku": "GASKET-DN80",
            "description": "DN80 EPDM Gasket",
            "category": "Fasteners, Gaskets & Seals",
            "quantity": 5,
            "unit": "pcs",
            "location": "Stores A-12",
            "minimum": 10,
            "supplier": "SealTech",
        },
    ]

    st.session_state.db[
        "jobs"
    ] = [
        {
            "job_no": "1052",
            "client": "Pharma Skid",
            "description": "DN80 Process Skid",
            "status": "Awaiting Material",
            "priority": "High",
            "due_date": str(date.today()),
            "created": now(),
            "requirements": [
                {
                    "sku": "VALVE-DN80-BF",
                    "description": "DN80 Butterfly Valve",
                    "required": 4,
                    "unit": "pcs",
                },
                {
                    "sku": "FLANGE-DN80-PN16",
                    "description": "DN80 PN16 Flange",
                    "required": 8,
                    "unit": "pcs",
                },
                {
                    "sku": "GASKET-DN80",
                    "description": "DN80 EPDM Gasket",
                    "required": 8,
                    "unit": "pcs",
                },
            ],
        },
        {
            "job_no": "1061",
            "client": "Process Pipework",
            "description": "DN50 Pipework Package",
            "status": "Awaiting Material",
            "priority": "Normal",
            "due_date": str(date.today()),
            "created": now(),
            "requirements": [
                {
                    "sku": "PIPE-DN50-316",
                    "description": "DN50 316L Stainless Pipe",
                    "required": 20,
                    "unit": "m",
                },
            ],
        },
    ]

    st.session_state.db[
        "deliveries"
    ] = [
        {
            "po": "PO-48127",
            "supplier": "ABC Valves",
            "job_no": "1052",
            "expected": str(date.today()),
            "status": "Expected",
            "items": "4 × DN80 Butterfly Valve",
        }
    ]

    add_audit(
        "Demo Loaded",
        "Demonstration data loaded."
    )

    save_database()

    update_automatic_statuses()


# ============================================================
# HEADER
# ============================================================

update_automatic_statuses()

st.markdown(
    """
<div class="fab-header">

<div class="fab-title">
⚙ FABLINE OPERATIONS
</div>

<div class="fab-subtitle">
Jobs • Inventory • Deliveries • Material Readiness
</div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

tabs = st.tabs([
    "🏠 Dashboard",
    "📋 Jobs",
    "📦 Inventory",
    "🚚 Deliveries",
    "🔎 Smart Search",
    "📢 Notices",
    "⚙ Admin",
])


# ============================================================
# DASHBOARD
# ============================================================

with tabs[0]:

    jobs = st.session_state.db["jobs"]
    inventory = st.session_state.db[
        "inventory"
    ]
    deliveries = st.session_state.db[
        "deliveries"
    ]

    missing_jobs = 0
    ready_jobs = 0

    for job in jobs:

        result = calculate_job(job)

        if (
            result["ready"]
            and job["status"] != "Complete"
        ):
            ready_jobs += 1

        elif (
            result["missing"]
            and job["status"] != "Complete"
        ):
            missing_jobs += 1

    low_stock = []

    for item in inventory:

        available = available_stock(
            item["sku"]
        )

        if available <= float(
            item.get("minimum", 0)
        ):
            low_stock.append(item)

    today_deliveries = [
        d for d in deliveries
        if d.get("expected")
        == str(date.today())
        and d.get("status")
        != "Received"
    ]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-label">
🔴 Jobs Missing Material
</div>
<div class="kpi-number">
{missing_jobs}
</div>
<div class="kpi-note">
Require purchasing or delivery
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-label">
🟢 Ready to Start
</div>
<div class="kpi-number">
{ready_jobs}
</div>
<div class="kpi-note">
Material available
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-label">
🚚 Deliveries Today
</div>
<div class="kpi-number">
{len(today_deliveries)}
</div>
<div class="kpi-note">
Expected today
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
<div class="kpi">
<div class="kpi-label">
⚠ Low Stock
</div>
<div class="kpi-number">
{len(low_stock)}
</div>
<div class="kpi-note">
Below minimum level
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("## Job Readiness")

    if not jobs:

        st.info(
            "No jobs yet. Create your first job "
            "under the Jobs tab."
        )

    for job in jobs:

        result = calculate_job(job)

        if result["ready"]:

            material_text = (
                '<span class="ready">'
                '✓ ALL MATERIAL AVAILABLE'
                '</span>'
            )

        elif result["missing"]:

            material_text = (
                '<span class="missing">'
                f'⚠ {len(result["missing"])} '
                'MATERIAL SHORTAGE(S)'
                '</span>'
            )

        else:

            material_text = (
                "No material requirements added"
            )

        st.markdown(
            f"""
<div class="job-card">

<div class="job-title">
JOB {job["job_no"]} — {job["client"]}
</div>

<div class="job-client">
{job["description"]}
</div>

<br>

<span class="badge badge-blue">
{job["status"]}
</span>

<span class="badge badge-orange">
{job["priority"]} Priority
</span>

<br><br>

<strong>
Material readiness:
{result["percent"]}%
</strong>

<div class="progress-bg">
<div class="progress-fill"
style="width:{result["percent"]}%">
</div>
</div>

<br>

{material_text}

</div>
""",
            unsafe_allow_html=True,
        )

        if result["missing"]:

            with st.expander(
                f"See what Job {job['job_no']} is missing"
            ):

                for shortage in result[
                    "missing"
                ]:

                    st.error(
                        f"{shortage['description']} — "
                        f"Missing "
                        f"{shortage['missing']:g} "
                        f"{shortage['unit']}"
                    )

    if low_stock:

        st.markdown("## ⚠ Low Stock")

        for item in low_stock:

            st.warning(
                f"{item['description']} — "
                f"{available_stock(item['sku']):g} "
                f"{item['unit']} available — "
                f"Location: {item['location']}"
            )


# ============================================================
# JOBS
# ============================================================

with tabs[1]:

    st.markdown("# Jobs")

    job_mode = st.radio(
        "Job Action",
        [
            "View Jobs",
            "Create Job",
            "Add Material Requirement",
            "Update Job Status",
        ],
        horizontal=True,
    )

    # --------------------------------------------------------
    # VIEW JOBS
    # --------------------------------------------------------

    if job_mode == "View Jobs":

        search = st.text_input(
            "Search jobs",
            placeholder=(
                "Job number, client, "
                "description..."
            ),
        )

        jobs = st.session_state.db["jobs"]

        if search:

            search_lower = search.lower()

            jobs = [
                j for j in jobs
                if search_lower
                in json.dumps(j).lower()
            ]

        for job in jobs:

            result = calculate_job(job)

            with st.expander(
                f"JOB {job['job_no']} — "
                f"{job['client']} — "
                f"{result['percent']}% Ready"
            ):

                a, b, c, d = st.columns(4)

                a.metric(
                    "Status",
                    job["status"]
                )

                b.metric(
                    "Material Ready",
                    f"{result['percent']}%"
                )

                c.metric(
                    "Priority",
                    job["priority"]
                )

                d.metric(
                    "Due",
                    job["due_date"]
                )

                st.write(
                    "**Description:**",
                    job["description"]
                )

                st.markdown(
                    "### Material Requirements"
                )

                if not job.get(
                    "requirements"
                ):

                    st.info(
                        "No material requirements "
                        "added."
                    )

                for req in job.get(
                    "requirements",
                    []
                ):

                    supplied = (
                        requirement_available(
                            job,
                            req,
                        )
                    )

                    missing = max(
                        0,
                        float(req["required"])
                        - supplied,
                    )

                    cols = st.columns(
                        [3, 1, 1, 1]
                    )

                    cols[0].write(
                        f"**{req['description']}**"
                    )

                    cols[1].write(
                        f"Required: "
                        f"{float(req['required']):g} "
                        f"{req['unit']}"
                    )

                    cols[2].write(
                        f"Available: "
                        f"{supplied:g}"
                    )

                    if missing > 0:

                        cols[3].error(
                            f"Missing {missing:g}"
                        )

                    else:

                        cols[3].success(
                            "Ready"
                        )

    # --------------------------------------------------------
    # CREATE JOB
    # --------------------------------------------------------

    elif job_mode == "Create Job":

        st.markdown(
            "### Create New Job"
        )

        with st.form(
            "create_job_form"
        ):

            c1, c2 = st.columns(2)

            with c1:

                job_no = st.text_input(
                    "Job Number *"
                )

                client = st.text_input(
                    "Client / Project *"
                )

                description = st.text_input(
                    "Description"
                )

            with c2:

                priority = st.selectbox(
                    "Priority",
                    [
                        "Normal",
                        "High",
                        "Urgent",
                    ],
                )

                due = st.date_input(
                    "Required Date"
                )

            submitted = (
                st.form_submit_button(
                    "CREATE JOB",
                    use_container_width=True,
                )
            )

            if submitted:

                if not clean(job_no):
                    st.error(
                        "Enter a job number."
                    )

                elif job_by_number(
                    clean(job_no)
                ):
                    st.error(
                        "That job number "
                        "already exists."
                    )

                else:

                    new_job = {
                        "job_no": clean(
                            job_no
                        ),
                        "client": clean(
                            client
                        )
                        or "N/A",
                        "description": clean(
                            description
                        ),
                        "priority": priority,
                        "due_date": str(due),
                        "status":
                            "Awaiting Material",
                        "created": now(),
                        "requirements": [],
                    }

                    st.session_state.db[
                        "jobs"
                    ].append(new_job)

                    add_audit(
                        "Job Created",
                        (
                            f"Created "
                            f"Job {job_no}"
                        ),
                        clean(job_no),
                    )

                    save_database()

                    st.success(
                        f"Job {job_no} created."
                    )

                    st.rerun()

    # --------------------------------------------------------
    # ADD REQUIREMENT
    # --------------------------------------------------------

    elif job_mode == (
        "Add Material Requirement"
    ):

        if not st.session_state.db[
            "jobs"
        ]:

            st.warning(
                "Create a job first."
            )

        elif not st.session_state.db[
            "inventory"
        ]:

            st.warning(
                "Add inventory first."
            )

        else:

            job_options = [
                j["job_no"]
                for j
                in st.session_state.db[
                    "jobs"
                ]
            ]

            selected_job = st.selectbox(
                "Job",
                job_options,
            )

            inventory_options = {
                (
                    f"{i['sku']} — "
                    f"{i['description']}"
                ): i
                for i
                in st.session_state.db[
                    "inventory"
                ]
            }

            selected_label = (
                st.selectbox(
                    "Material",
                    list(
                        inventory_options.keys()
                    ),
                )
            )

            selected_item = (
                inventory_options[
                    selected_label
                ]
            )

            quantity = st.number_input(
                (
                    f"Required Quantity "
                    f"({selected_item['unit']})"
                ),
                min_value=0.01,
                value=1.0,
            )

            if st.button(
                "ADD TO JOB",
                use_container_width=True,
            ):

                job = job_by_number(
                    selected_job
                )

                existing = None

                for req in job[
                    "requirements"
                ]:

                    if (
                        req["sku"]
                        == selected_item["sku"]
                    ):
                        existing = req

                if existing:

                    existing[
                        "required"
                    ] += quantity

                else:

                    job[
                        "requirements"
                    ].append(
                        {
                            "sku":
                                selected_item[
                                    "sku"
                                ],
                            "description":
                                selected_item[
                                    "description"
                                ],
                            "required":
                                quantity,
                            "unit":
                                selected_item[
                                    "unit"
                                ],
                        }
                    )

                add_audit(
                    "Material Added",
                    (
                        f"{quantity:g} "
                        f"{selected_item['unit']} "
                        f"{selected_item['description']}"
                    ),
                    selected_job,
                )

                save_database()

                update_automatic_statuses()

                st.success(
                    "Material requirement added."
                )

                st.rerun()

    # --------------------------------------------------------
    # UPDATE STATUS
    # --------------------------------------------------------

    else:

        if not st.session_state.db[
            "jobs"
        ]:

            st.info("No jobs available.")

        else:

            selected_job = st.selectbox(
                "Select Job",
                [
                    j["job_no"]
                    for j
                    in st.session_state.db[
                        "jobs"
                    ]
                ],
            )

            job = job_by_number(
                selected_job
            )

            status = st.selectbox(
                "New Status",
                JOB_STATUSES,
                index=(
                    JOB_STATUSES.index(
                        job["status"]
                    )
                    if job["status"]
                    in JOB_STATUSES
                    else 0
                ),
            )

            if st.button(
                "UPDATE STATUS"
            ):

                old_status = job[
                    "status"
                ]

                job["status"] = status

                add_audit(
                    "Status Updated",
                    (
                        f"{old_status} "
                        f"→ {status}"
                    ),
                    selected_job,
                )

                save_database()

                st.success(
                    "Status updated."
                )

                st.rerun()


# ============================================================
# INVENTORY
# ============================================================

with tabs[2]:

    st.markdown("# Inventory")

    inventory_mode = st.radio(
        "Inventory Action",
        [
            "View Stock",
            "Add New Item",
            "Adjust Stock",
            "Move Stock",
        ],
        horizontal=True,
    )

    # --------------------------------------------------------
    # VIEW
    # --------------------------------------------------------

    if inventory_mode == "View Stock":

        search_stock = st.text_input(
            "Search Inventory",
            placeholder=(
                "DN50, valve, flange, "
                "rack..."
            ),
        )

        items = st.session_state.db[
            "inventory"
        ]

        if search_stock:

            items = [
                i for i in items
                if search_stock.lower()
                in json.dumps(i).lower()
            ]

        for item in items:

            reserved = total_reserved(
                item["sku"]
            )

            available = max(
                0,
                float(item["quantity"])
                - reserved,
            )

            low = (
                available
                <= float(
                    item.get(
                        "minimum",
                        0
                    )
                )
            )

            st.markdown(
                f"""
<div class="stock-card">

<div class="stock-name">
{item["description"]}
</div>

<div style="
color:#6b7280;
font-size:12px;
">
{item["sku"]}
</div>

<br>

<strong>
Physical Stock:
</strong>
{float(item["quantity"]):g}
{item["unit"]}

&nbsp;&nbsp;

<strong>
Reserved:
</strong>
{reserved:g}
{item["unit"]}

&nbsp;&nbsp;

<strong>
Available:
</strong>
{available:g}
{item["unit"]}

<br><br>

📍 <strong>
{item["location"]}
</strong>

&nbsp;&nbsp;

Supplier:
{item["supplier"]}

</div>
""",
                unsafe_allow_html=True,
            )

            if low:

                st.warning(
                    "Low stock — available "
                    "quantity is at or below "
                    "the minimum stock level."
                )

    # --------------------------------------------------------
    # ADD ITEM
    # --------------------------------------------------------

    elif inventory_mode == (
        "Add New Item"
    ):

        with st.form(
            "new_inventory_item"
        ):

            c1, c2 = st.columns(2)

            with c1:

                sku = st.text_input(
                    "SKU / Stock Code *"
                )

                description = (
                    st.text_input(
                        "Description *"
                    )
                )

                category = (
                    st.selectbox(
                        "Category",
                        CATEGORIES,
                    )
                )

                unit = st.selectbox(
                    "Unit",
                    UNITS,
                )

            with c2:

                quantity = (
                    st.number_input(
                        "Starting Quantity",
                        min_value=0.0,
                    )
                )

                minimum = (
                    st.number_input(
                        "Minimum Stock",
                        min_value=0.0,
                    )
                )

                location = (
                    st.text_input(
                        "Location",
                        placeholder=(
                            "Rack B-04"
                        ),
                    )
                )

                supplier = (
                    st.text_input(
                        "Supplier"
                    )
                )

            submit = (
                st.form_submit_button(
                    "ADD INVENTORY ITEM",
                    use_container_width=True,
                )
            )

            if submit:

                if (
                    not clean(sku)
                    or not clean(description)
                ):

                    st.error(
                        "SKU and description "
                        "are required."
                    )

                elif inventory_by_sku(
                    clean(sku)
                ):

                    st.error(
                        "SKU already exists."
                    )

                else:

                    item = {
                        "sku": clean(sku),
                        "description":
                            clean(description),
                        "category": category,
                        "quantity": quantity,
                        "unit": unit,
                        "location":
                            clean(location)
                            or "Unassigned",
                        "minimum": minimum,
                        "supplier":
                            clean(supplier)
                            or "N/A",
                    }

                    st.session_state.db[
                        "inventory"
                    ].append(item)

                    add_audit(
                        "Inventory Created",
                        (
                            f"{sku}: "
                            f"{description}"
                        ),
                    )

                    save_database()

                    st.success(
                        "Inventory item added."
                    )

                    st.rerun()

    # --------------------------------------------------------
    # ADJUST
    # --------------------------------------------------------

    elif inventory_mode == (
        "Adjust Stock"
    ):

        if not st.session_state.db[
            "inventory"
        ]:

            st.info(
                "No inventory yet."
            )

        else:

            options = {
                (
                    f"{i['sku']} — "
                    f"{i['description']}"
                ): i
                for i
                in st.session_state.db[
                    "inventory"
                ]
            }

            selected = st.selectbox(
                "Inventory Item",
                list(options.keys()),
            )

            item = options[selected]

            st.metric(
                "Current Physical Stock",
                (
                    f"{float(item['quantity']):g} "
                    f"{item['unit']}"
                ),
            )

            operation = st.radio(
                "Action",
                [
                    "Add Stock",
                    "Use / Remove Stock",
                ],
                horizontal=True,
            )

            amount = st.number_input(
                f"Quantity ({item['unit']})",
                min_value=0.01,
                value=1.0,
            )

            if st.button(
                "CONFIRM STOCK CHANGE"
            ):

                if operation == "Add Stock":

                    item["quantity"] += amount

                else:

                    if amount > float(
                        item["quantity"]
                    ):

                        st.error(
                            "Cannot remove more "
                            "than physical stock."
                        )

                        st.stop()

                    item["quantity"] -= amount

                add_audit(
                    "Stock Adjusted",
                    (
                        f"{operation}: "
                        f"{amount:g} "
                        f"{item['unit']} "
                        f"{item['description']}"
                    ),
                )

                save_database()

                update_automatic_statuses()

                st.success(
                    "Inventory updated."
                )

                st.rerun()

    # --------------------------------------------------------
    # MOVE
    # --------------------------------------------------------

    else:

        if not st.session_state.db[
            "inventory"
        ]:

            st.info("No inventory.")

        else:

            options = {
                (
                    f"{i['sku']} — "
                    f"{i['description']}"
                ): i
                for i
                in st.session_state.db[
                    "inventory"
                ]
            }

            selected = st.selectbox(
                "Item",
                list(options.keys()),
            )

            item = options[selected]

            st.write(
                "Current location:",
                f"**{item['location']}**",
            )

            new_location = (
                st.text_input(
                    "New Location",
                    placeholder=(
                        "Valve Shelf 3"
                    ),
                )
            )

            if st.button(
                "MOVE STOCK"
            ):

                if clean(new_location):

                    old = item["location"]

                    item["location"] = (
                        clean(new_location)
                    )

                    add_audit(
                        "Stock Moved",
                        (
                            f"{item['sku']} "
                            f"{old} → "
                            f"{new_location}"
                        ),
                    )

                    save_database()

                    st.success(
                        "Location updated."
                    )

                    st.rerun()


# ============================================================
# DELIVERIES
# ============================================================

with tabs[3]:

    st.markdown("# Deliveries & Purchase Orders")

    delivery_mode = st.radio(
        "Delivery Action",
        [
            "Expected Deliveries",
            "Add Delivery",
            "Receive Material",
        ],
        horizontal=True,
    )

    if delivery_mode == (
        "Expected Deliveries"
    ):

        deliveries = (
            st.session_state.db[
                "deliveries"
            ]
        )

        if not deliveries:

            st.info(
                "No deliveries recorded."
            )

        for delivery in deliveries:

            icon = (
                "✅"
                if delivery["status"]
                == "Received"
                else "🚚"
            )

            st.markdown(
                f"""
<div class="job-card">

<div class="job-title">
{icon} {delivery["po"]}
</div>

<strong>
Supplier:
</strong>
{delivery["supplier"]}

<br>

<strong>
Job:
</strong>
{delivery["job_no"]}

<br>

<strong>
Expected:
</strong>
{delivery["expected"]}

<br>

<strong>
Status:
</strong>
{delivery["status"]}

<br><br>

{delivery["items"]}

</div>
""",
                unsafe_allow_html=True,
            )

    elif delivery_mode == (
        "Add Delivery"
    ):

        with st.form(
            "new_delivery"
        ):

            c1, c2 = st.columns(2)

            with c1:

                po = st.text_input(
                    "PO Number"
                )

                supplier = (
                    st.text_input(
                        "Supplier"
                    )
                )

                job_no = (
                    st.text_input(
                        "Related Job Number"
                    )
                )

            with c2:

                expected = (
                    st.date_input(
                        "Expected Date"
                    )
                )

            items = st.text_area(
                "Expected Material",
                placeholder=(
                    "4 x DN80 valves\n"
                    "8 x DN80 flanges"
                ),
            )

            if st.form_submit_button(
                "ADD EXPECTED DELIVERY"
            ):

                delivery = {
                    "po": clean(po)
                        or "NO-PO",
                    "supplier":
                        clean(supplier)
                        or "N/A",
                    "job_no":
                        clean(job_no)
                        or "N/A",
                    "expected":
                        str(expected),
                    "status":
                        "Expected",
                    "items":
                        clean(items),
                }

                st.session_state.db[
                    "deliveries"
                ].append(delivery)

                add_audit(
                    "Delivery Added",
                    (
                        f"{delivery['po']} "
                        f"from "
                        f"{delivery['supplier']}"
                    ),
                    delivery["job_no"],
                )

                save_database()

                st.success(
                    "Delivery added."
                )

                st.rerun()

    else:

        if not st.session_state.db[
            "inventory"
        ]:

            st.warning(
                "Create inventory items "
                "before receiving material."
            )

        else:

            st.markdown(
                "### Receive Material"
            )

            st.info(
                "Confirming a delivery "
                "automatically increases "
                "physical inventory and "
                "recalculates affected jobs."
            )

            options = {
                (
                    f"{i['sku']} — "
                    f"{i['description']}"
                ): i
                for i
                in st.session_state.db[
                    "inventory"
                ]
            }

            selected = st.selectbox(
                "Material Received",
                list(options.keys()),
            )

            item = options[selected]

            quantity = st.number_input(
                f"Received Quantity "
                f"({item['unit']})",
                min_value=0.01,
                value=1.0,
            )

            po = st.text_input(
                "PO / Delivery Docket Number"
            )

            supplier = st.text_input(
                "Supplier",
                value=(
                    ""
                    if item["supplier"]
                    == "N/A"
                    else item["supplier"]
                ),
            )

            related_job = st.text_input(
                "Related Job Number "
                "(optional)"
            )

            if st.button(
                "CONFIRM MATERIAL RECEIVED",
                use_container_width=True,
            ):

                item["quantity"] += quantity

                matching_delivery = None

                if clean(po):

                    for delivery in (
                        st.session_state.db[
                            "deliveries"
                        ]
                    ):

                        if (
                            delivery["po"]
                            == clean(po)
                        ):
                            matching_delivery = (
                                delivery
                            )

                if matching_delivery:

                    matching_delivery[
                        "status"
                    ] = "Received"

                add_audit(
                    "Material Received",
                    (
                        f"{quantity:g} "
                        f"{item['unit']} "
                        f"{item['description']} "
                        f"received. "
                        f"PO: {po or 'N/A'}"
                    ),
                    clean(related_job),
                )

                save_database()

                update_automatic_statuses()

                st.success(
                    "Material received. "
                    "Inventory and job "
                    "readiness recalculated."
                )

                st.rerun()


# ============================================================
# SMART SEARCH
# ============================================================

with tabs[4]:

    st.markdown("# 🔎 Smart Search")

    st.caption(
        "Try: 'what is missing for job 1052', "
        "'what jobs are ready', "
        "'where are DN80 valves', "
        "or simply enter a job number."
    )

    question = st.text_input(
        "Ask about jobs or inventory"
    )

    if question:

        q = question.lower()

        # READY JOBS
        if (
            "ready" in q
            and "job" in q
        ):

            ready = []

            for job in (
                st.session_state.db[
                    "jobs"
                ]
            ):

                result = (
                    calculate_job(job)
                )

                if (
                    result["ready"]
                    and job["status"]
                    != "Complete"
                ):
                    ready.append(job)

            if ready:

                st.success(
                    f"{len(ready)} job(s) "
                    "currently have all "
                    "required material."
                )

                for job in ready:

                    st.write(
                        f"**Job "
                        f"{job['job_no']}** — "
                        f"{job['client']}"
                    )

            else:

                st.info(
                    "No jobs currently have "
                    "all required material."
                )

        # JOB NUMBER
        else:

            found_job = None

            for job in (
                st.session_state.db[
                    "jobs"
                ]
            ):

                if (
                    job["job_no"].lower()
                    in q
                ):
                    found_job = job
                    break

            if found_job:

                result = calculate_job(
                    found_job
                )

                st.markdown(
                    f"### Job "
                    f"{found_job['job_no']}"
                )

                st.write(
                    "**Client:**",
                    found_job["client"]
                )

                st.write(
                    "**Status:**",
                    found_job["status"]
                )

                st.write(
                    "**Material readiness:**",
                    f"{result['percent']}%"
                )

                if result["missing"]:

                    st.error(
                        "This job is missing "
                        "material:"
                    )

                    for missing in (
                        result["missing"]
                    ):

                        st.write(
                            f"• "
                            f"{missing['description']}"
                            f" — "
                            f"{missing['missing']:g} "
                            f"{missing['unit']}"
                        )

                elif found_job.get(
                    "requirements"
                ):

                    st.success(
                        "All required material "
                        "is available."
                    )

            else:

                matches = []

                for item in (
                    st.session_state.db[
                        "inventory"
                    ]
                ):

                    searchable = (
                        f"{item['sku']} "
                        f"{item['description']} "
                        f"{item['category']} "
                        f"{item['location']}"
                    ).lower()

                    terms = [
                        t for t
                        in q.split()
                        if len(t) > 2
                    ]

                    score = sum(
                        1
                        for term in terms
                        if term in searchable
                    )

                    if score:
                        matches.append(
                            (score, item)
                        )

                matches.sort(
                    key=lambda x: x[0],
                    reverse=True,
                )

                if matches:

                    st.markdown(
                        "### Inventory Matches"
                    )

                    for _, item in (
                        matches[:10]
                    ):

                        st.write(
                            f"**{item['description']}**"
                        )

                        st.write(
                            f"📍 "
                            f"{item['location']} | "
                            f"Physical: "
                            f"{float(item['quantity']):g} "
                            f"{item['unit']} | "
                            f"Available: "
                            f"{available_stock(item['sku']):g} "
                            f"{item['unit']}"
                        )

                        st.divider()

                else:

                    st.info(
                        "Nothing matched "
                        "that search."
                    )


# ============================================================
# NOTICEBOARD
# ============================================================

with tabs[5]:

    st.markdown("# 📢 Noticeboard")

    with st.form(
        "notice_form"
    ):

        title = st.text_input(
            "Notice"
        )

        urgency = st.selectbox(
            "Priority",
            [
                "Information",
                "Action Required",
                "Urgent",
            ],
        )

        details = st.text_area(
            "Details"
        )

        author = st.text_input(
            "Posted By"
        )

        if st.form_submit_button(
            "POST NOTICE"
        ):

            if clean(title):

                st.session_state.db[
                    "notices"
                ].insert(
                    0,
                    {
                        "title":
                            clean(title),
                        "urgency":
                            urgency,
                        "details":
                            clean(details),
                        "author":
                            clean(author)
                            or "Staff",
                        "timestamp":
                            now(),
                    },
                )

                save_database()

                st.success(
                    "Notice posted."
                )

                st.rerun()

    st.divider()

    for notice in (
        st.session_state.db[
            "notices"
        ]
    ):

        if notice["urgency"] == "Urgent":

            st.error(
                f"**{notice['title']}**\n\n"
                f"{notice['details']}\n\n"
                f"{notice['author']} — "
                f"{notice['timestamp']}"
            )

        elif (
            notice["urgency"]
            == "Action Required"
        ):

            st.warning(
                f"**{notice['title']}**\n\n"
                f"{notice['details']}\n\n"
                f"{notice['author']} — "
                f"{notice['timestamp']}"
            )

        else:

            st.info(
                f"**{notice['title']}**\n\n"
                f"{notice['details']}\n\n"
                f"{notice['author']} — "
                f"{notice['timestamp']}"
            )


# ============================================================
# ADMIN
# ============================================================

with tabs[6]:

    st.markdown("# ⚙ Admin & Backup")

    st.markdown(
        "### Demo"
    )

    if st.button(
        "LOAD DEMO DATA"
    ):

        load_demo()

        st.success(
            "Demo data loaded."
        )

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # JOB CSV
    # --------------------------------------------------------

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Job Number",
        "Client",
        "Description",
        "Status",
        "Priority",
        "Due Date",
        "Material Readiness",
    ])

    for job in (
        st.session_state.db[
            "jobs"
        ]
    ):

        result = calculate_job(job)

        writer.writerow([
            job["job_no"],
            job["client"],
            job["description"],
            job["status"],
            job["priority"],
            job["due_date"],
            f"{result['percent']}%",
        ])

    st.download_button(
        "📥 DOWNLOAD JOBS CSV",
        output.getvalue(),
        file_name=(
            "fabline_jobs_"
            + datetime.now().strftime(
                "%Y%m%d"
            )
            + ".csv"
        ),
        mime="text/csv",
    )

    # --------------------------------------------------------
    # DATABASE BACKUP
    # --------------------------------------------------------

    database_json = json.dumps(
        st.session_state.db,
        indent=4,
    )

    st.download_button(
        "💾 DOWNLOAD FULL DATABASE BACKUP",
        database_json,
        file_name=(
            "fabline_backup_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M"
            )
            + ".json"
        ),
        mime="application/json",
    )

    st.divider()

    st.markdown(
        "### Audit History"
    )

    for entry in (
        st.session_state.db[
            "audit"
        ][:100]
    ):

        st.write(
            f"**{entry['timestamp']} — "
            f"{entry['action']}**"
        )

        st.caption(
            (
                f"Job {entry['job_no']} • "
                if entry["job_no"]
                else ""
            )
            + entry["details"]
        )

        st.divider()
