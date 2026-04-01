# VCL Job Cards - Complete Technical Breakdown

## For ERPNext Website Frontend Development

---

## 1. APP OVERVIEW

- **App Name:** `vcl_job_cards`
- **App Title:** VCL Job Card Tracking
- **Publisher:** Vimit Converters Limited
- **Email:** tanuj@vimitconverters.com
- **License:** MIT
- **Required Apps:** `erpnext`
- **Module:** `Job Card Tracking`
- **Version:** 0.0.1

---

## 2. DIRECTORY STRUCTURE

```
vcl_job_cards/
├── pyproject.toml
├── license.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
├── vcl_job_cards/
│   ├── __init__.py
│   ├── hooks.py
│   ├── modules.txt                     # Contains: "Job Card Tracking"
│   ├── patches.txt                     # Empty (no migrations yet)
│   └── job_card_tracking/
│       ├── __init__.py
│       └── doctype/
│           ├── .gitkeep
│           ├── colour_of_parts/        # CHILD TABLE
│           ├── customer_product_specification/  # PARENT DOCTYPE
│           ├── dies/                    # PARENT DOCTYPE
│           ├── dies_order/             # CHILD TABLE
│           ├── job_card_computer_paper/ # PARENT DOCTYPE (main job card)
│           ├── production_entry/       # PARENT DOCTYPE
│           ├── production_planning_line/ # CHILD TABLE
│           └── production_actual_line/  # CHILD TABLE
```

---

## 3. DOCTYPE HIERARCHY & RELATIONSHIPS

```
┌─────────────────────────────────────────────────────┐
│                    MASTER DATA                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Dies (DIE-.#####)                                  │
│  ├── Child: Dies Order (child table)                │
│  │   Fields: order_date, order_number, quantity,    │
│  │           status (Active/Discarded), notes       │
│  └── Used by: Customer Product Specification        │
│      (Label product type auto-populates from Dies)  │
│                                                     │
│  Customer Product Specification                     │
│  (CPT-SPEC/CTN-SPEC/LBL-SPEC/EXB-SPEC-.#####)     │
│  ├── Child: Colour of Parts (child table)           │
│  │   Fields: part_number, paper_type, gsm,          │
│  │           colour, purpose                        │
│  ├── Submittable: YES                               │
│  └── Used by: Job Card Computer Paper               │
│                                                     │
├─────────────────────────────────────────────────────┤
│                 TRANSACTIONAL                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Job Card Computer Paper (JC-CPT-.YYYY.-.#####)     │
│  ├── Child: Colour of Parts (child table, read-only)│
│  ├── Links to: Customer (ERPNext), Customer Product │
│  │   Specification, User (sales_rep, mgmt_approver) │
│  ├── Submittable: YES, Amendable: YES               │
│  └── Used by: Production Entry                      │
│                                                     │
│  Production Entry (PE-.YYYY.-.#####)                │
│  ├── Child: Production Planning Line                │
│  │   Links to: Job Card Computer Paper              │
│  ├── Child: Production Actual Line                  │
│  │   Links to: Job Card Computer Paper              │
│  ├── Submittable: YES, Amendable: YES               │
│  └── On submit/cancel: Updates Job Card totals      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Data Flow:
```
Customer (ERPNext) 
  → Customer Product Specification (master specs per product type)
    → Job Card Computer Paper (order-level job card, pulls spec data)
      → Production Entry (daily production sheet)
        → On Submit: Updates Job Card's production totals & status
```

---

## 4. DETAILED DOCTYPE SPECIFICATIONS

---

### 4.1 Dies (Master Data)

**Purpose:** Stores printing die master data for label products.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| naming_series | Select | Yes | `DIE-.#####` |
| die_number | Data | No | Read-only, auto-set |
| die_size | Data | Yes | In list view, filterable |
| length | Float (2dp) | Yes | mm |
| width | Float (2dp) | Yes | mm |
| shape | Select | No | SQUARE/RECTANGLE/CIRCLE/SEMI CIRCLE/IRREGULAR/OVAL/ROUND |
| across_ups | Int | No | Plate Up |
| round_ups | Int | No | Plate Round |
| teeth | Float (2dp) | No | Cylinder teeth |
| material | Select | No | PP White/PP Clear/PP Silver/Thermal/Semi-Gloss |
| orders | Table | No | Child: Dies Order |
| remark | Small Text | No | |

**Child Table - Dies Order:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| order_date | Date | No | In list view |
| order_number | Data | Yes | In list view |
| quantity | Int | Yes | In list view |
| status | Select | Yes | Active / Discarded |
| notes | Small Text | No | |

**Permissions:**
- System Manager: Full CRUD
- Sales Manager: Read only
- All: Read only

**Python Validations:**
- Length must be > 0
- Width must be > 0

---

### 4.2 Customer Product Specification (Master Data, Submittable)

**Purpose:** Reusable product specifications tied to a Customer. Supports 4 product types with conditional sections.

**Naming Series by Product Type:**
- Computer Paper → `CPT-SPEC-.#####`
- Carton → `CTN-SPEC-.#####`
- Label → `LBL-SPEC-.#####`
- Exercise Books → `EXB-SPEC-.#####`

#### Common Fields (all product types):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| product_type | Select | Yes | Computer Paper / Carton / Label / Exercise Books |
| naming_series | Select | Yes | Auto-set based on product_type |
| status | Select | Yes | Active (default) / Inactive / Discontinued |
| specification_name | Data | Yes | In list view |
| customer | Link→Customer | Yes | In list view, filterable |
| job_size | Data | Yes | |
| number_of_colours | Int | Yes | |

#### Computer Paper Section (visible when product_type == "Computer Paper"):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| pay_slip_size | Data | No | |
| number_of_parts | Int | Mandatory | |
| colour_of_parts | Table→Colour of Parts | No | Auto-synced to match number_of_parts |

#### Carton Section (visible when product_type == "Carton"):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| board_type | Select | Mandatory | KLB / MF / Test Liner |
| flute_type | Select | Mandatory | A-Flute / B-Flute / C-Flute / E-Flute |
| ply | Select | No | 3-Ply / 5-Ply / 7-Ply |
| carton_dimensions | Data | No | |

#### Label Section (visible when product_type == "Label"):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| dies | Link→Dies | No | Auto-populates fields below when selected |
| label_length | Float (2dp) | Mandatory | Read-only, from Dies |
| label_width | Float (2dp) | Mandatory | Read-only, from Dies |
| label_number_of_colours | Int | Mandatory | |
| cylinder_teeth | Data | No | Read-only, from Dies |
| plate_up | Data | No | Read-only, from Dies (across_ups) |
| plate_round | Data | No | Read-only, from Dies (round_ups) |
| packing_up | Data | No | |
| material_type | Select | Mandatory | PP White/PP Clear/PP Silver/Thermal/Semi-Gloss |
| packing_pieces | Int | No | From Dies (qty) |
| gap_between | Float (2dp) | No | |
| side_trim | Float (2dp) | No | mm |

#### Exercise Books Section (visible when product_type == "Exercise Books"):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| number_of_pages | Int | Mandatory | Must be multiple of 4 |
| ruling_type | Select | Mandatory | Single Line/Double Line/Square/Graph/Blank |
| binding_type | Select | No | Saddle Stitch/Perfect Binding/Wire-O |
| cover_type | Select | No | Same as Inner/Card Stock/Glossy Cover |

#### Packing Section (all product types):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| numbering_required | Check | No | Default: 0 |
| standard_packing | Data | No | |
| standard_weight_per_carton | Float (2dp) | No | |
| internal_notes | Small Text | No | Collapsible section |

**Child Table - Colour of Parts:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| part_number | Int | Yes | Sequential, auto-numbered |
| paper_type | Select | No | CB/CFB/CF/60 GSM Bond/70 GSM Bond |
| gsm | Int | No | Auto-set from paper_type |
| colour | Data | Yes | |
| purpose | Data | No | |

**Paper Type / GSM Rules (enforced in Python & JS):**
- Single part: 60 GSM Bond (60 GSM) or CB (55) or 70 GSM Bond (70)
- First part (multi): CB (55 GSM)
- Middle parts: CFB (50 GSM)
- Last part: CF (55 GSM)

**GSM Auto-Population Map (JS):**
```
CB → 55, CFB → 50, CF → 55, 60 GSM Bond → 60, 70 GSM Bond → 70
```

**Dies Auto-Population (JS, when dies field changes for Label type):**
```
Dies.length → label_length
Dies.width → label_width
Dies.teeth → cylinder_teeth
Dies.across_ups → plate_up
Dies.round_ups → plate_round
Dies.qty → packing_pieces
```

**Permissions:**
- System Manager: Full CRUD + submit/cancel/amend
- Sales Manager: Create, write, submit, cancel, amend (no delete)
- Sales User: Read only

**Python Validations:**
- Product type required
- Auto-set naming_series from product_type
- Computer Paper: number_of_parts required, colour_of_parts count must match, sequential part numbers, colour required, paper_type/GSM rules enforced
- Label: label_length, label_width, label_number_of_colours, material_type required
- Exercise Books: number_of_pages required and must be multiple of 4

---

### 4.3 Job Card Computer Paper (Transactional, Submittable, Amendable)

**Purpose:** The main job card document representing a customer order for computer paper production.

**Naming Series:** `JC-CPT-.YYYY.-.#####` (e.g., JC-CPT-2026-00001)

#### Section: Header

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| naming_series | Select | Yes | JC-CPT-.YYYY.-.##### |
| order_date | Date | Yes | Default: Today |
| due_date | Date | Yes | |
| customer | Link→Customer | Yes | In list view, filterable |
| lpo_number | Data | No | Local Purchase Order number |

#### Section: Product Specification

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| customer_product_spec | Link→Customer Product Specification | Yes | Filtered by customer + product_type="Computer Paper" + status="Active". Uses whitelisted query method. |
| specification_name | Data | No | Read-only, auto-populated from spec |
| job_size | Data | No | Read-only, from spec |
| pay_slip_size | Data | No | Read-only, from spec |
| number_of_colours | Int | No | Read-only, from spec |
| number_of_parts | Int | No | Read-only, from spec |
| colour_of_parts | Table→Colour of Parts | No | Read-only, rebuilt from spec |

#### Section: Job-Specific Details

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| quantity_ordered | Int | Yes | In list view. Must be > 0 |
| packing | Data | No | Auto-populated from spec.standard_packing |
| weight_per_carton | Float (2dp) | No | From spec.standard_weight_per_carton |
| order_comments | Small Text | No | |

#### Section: Numbering

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| numbering_required | Check | No | Read-only, from spec |
| numbering_prefix | Data | No | Visible when numbering_required=1 |
| numbering_start | Data | Conditional | Required when numbering_required=1 |
| numbering_end | Data | Conditional | Required when numbering_required=1 |
| numbering_format | Data | No | Visible when numbering_required=1 |

#### Section: Plate Information

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| plate_status | Select | Yes | New / Old |
| plate_code | Data | Conditional | Required when plate_status="Old", must be empty when "New" |
| plate_notes | Small Text | No | |

#### Section: Approvals

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| sales_rep | Link→User | No | Auto-set if current user has Sales User/Manager role |
| sales_rep_approval_date | Date | No | Auto-set with sales_rep |
| sales_rep_comments | Small Text | No | |
| management_approver | Link→User | No | |
| management_approval_date | Date | No | |
| management_comments | Small Text | No | |

#### Section: Production Tracking (auto-updated, read-only)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| html_production_tracking_header | HTML | No | Info banner |
| total_actual_good_qty | Int | No | Default: 0, read-only. Sum from all submitted Production Entries |
| total_waste_qty | Int | No | Default: 0, read-only. Sum of waste from Production Entries |
| balance_qty | Int | No | Default: 0, read-only. quantity_ordered - total_actual_good_qty (min 0) |
| production_status | Select | No | Not Started (default) / In Production / Completed. In list view, filterable |

**Whitelisted API Method:**
```python
@frappe.whitelist()
def get_customer_product_spec_query(doctype, txt, searchfield, start, page_len, filters):
```
- Endpoint: `vcl_job_cards.job_card_tracking.doctype.job_card_computer_paper.job_card_computer_paper.get_customer_product_spec_query`
- Filters specs by: customer match, product_type="Computer Paper", status="Active"
- Returns: name, specification_name, customer

**JS Auto-Population (when customer_product_spec changes):**
```
spec.specification_name → specification_name
spec.job_size → job_size
spec.pay_slip_size → pay_slip_size
spec.number_of_colours → number_of_colours
spec.number_of_parts → number_of_parts
spec.numbering_required → numbering_required
spec.standard_packing → packing
spec.standard_weight_per_carton → weight_per_carton
spec.colour_of_parts[] → colour_of_parts[] (table rebuilt)
```

**JS Behaviors:**
- Customer change: clears spec and all auto-filled fields, warns if no active specs found
- Order date: defaults to today on load and if cleared

**Permissions:**
- System Manager: Full CRUD + submit/cancel/amend
- Sales Manager: Create, write, submit, cancel, amend (no delete)
- Sales User: Read only
- Manufacturing Manager: Read + write
- Manufacturing User: Read only

**Python Validations:**
- customer_product_spec must belong to selected customer
- product_type must be "Computer Paper"
- spec must be "Active"
- job_size, number_of_colours, number_of_parts must exist after spec selection
- Numbering: start and end required when numbering_required is checked
- Plate: code required when Old, must be empty when New
- Quantity must be > 0
- Auto-assigns sales_rep if user has Sales role

---

### 4.4 Production Entry (Transactional, Submittable, Amendable)

**Purpose:** Daily production sheet to record planned and actual output per station/shift.

**Naming Series:** `PE-.YYYY.-.#####` (e.g., PE-2026-00001)

#### Header Fields:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| naming_series | Select | Yes | PE-.YYYY.-.##### |
| production_date | Date | Yes | Default: Today. In list view, filterable |
| station | Data | No | In list view, filterable |
| shift | Data | No | In list view |
| supervisor | Data | No | |
| remarks | Small Text | No | |

#### Planning Lines (Child Table: Production Planning Line):

| Field | Type | Required | In List View | Notes |
|-------|------|----------|-------------|-------|
| job_card | Link→Job Card Computer Paper | Yes | Yes | Only submitted JCs shown |
| order_qty | Int | No | Yes | Read-only, from JC |
| produced_qty | Int | No | No | Read-only, from JC |
| balance_qty | Int | No | No | Read-only, from JC |
| planned_qty | Int | Yes | Yes | User enters target |
| planned_date | Date | Yes | Yes | Default: Today |
| stage | Select | No | Yes | Printing/Slitting/Rewinding/Packing |
| machine | Data | No | No | |
| operator | Data | No | No | |
| shift | Data | No | No | |
| start_time | Time | No | No | |
| end_time | Time | No | No | |
| downtime_mins | Float (1dp) | No | No | |
| remarks | Small Text | No | No | |

#### Actual Lines (Child Table: Production Actual Line):

| Field | Type | Required | In List View | Notes |
|-------|------|----------|-------------|-------|
| job_card | Link→Job Card Computer Paper | Yes | Yes | Only submitted JCs shown |
| order_qty | Int | No | No | Read-only, from JC |
| produced_qty | Int | No | No | Read-only, from JC |
| balance_qty | Int | No | No | Read-only, from JC |
| good_qty | Int | Yes | Yes | Usable output |
| waste_qty | Int | No | Yes | Default: 0. Rejects/misprints |
| running_balance | Int | No | Yes | Read-only. balance_qty - good_qty |
| stage | Select | No | Yes | Printing/Slitting/Rewinding/Packing |
| machine | Data | No | No | |
| operator | Data | No | No | |
| shift | Data | No | No | |
| start_time | Time | No | No | |
| end_time | Time | No | No | |
| downtime_mins | Float (1dp) | No | No | |
| remarks | Small Text | No | No | |

#### Summary Fields:

| Field | Type | Notes |
|-------|------|-------|
| total_good_qty | Int | Read-only. Sum of good_qty from actual_lines. In list view |
| total_waste_qty | Int | Read-only. Sum of waste_qty from actual_lines. In list view |

**Permissions:**
- System Manager: Full CRUD + submit/cancel/amend
- Manufacturing Manager: Full CRUD + submit/cancel/amend
- Manufacturing User: Create, write, submit, read, report (no delete, no cancel, no amend)

**Python Logic (production_entry.py):**

1. **validate():**
   - Validates all actual_lines have a job_card
   - Checks that linked Job Cards are submitted (docstatus == 1)
   - Auto-populates order_qty, produced_qty, balance_qty from Job Card for both planning and actual lines
   - Calculates total_good_qty and total_waste_qty
   - Calculates running_balance for each actual line

2. **on_submit():**
   - Calls `update_linked_job_cards()` → aggregates all submitted Production Entries for each Job Card

3. **on_cancel():**
   - Same as on_submit (recalculates from scratch)

4. **update_job_card_totals(job_card_name):** (module-level function)
   - SQL aggregation across ALL submitted Production Actual Lines for this Job Card
   - Updates Job Card fields: total_actual_good_qty, total_waste_qty, balance_qty, production_status
   - Status logic:
     - produced == 0 → "Not Started"
     - produced >= order_qty → "Completed"
     - else → "In Production"

**JS Logic (production_entry.js):**
- Filters job_card Link fields to only show submitted JCs (docstatus: 1)
- Auto-populates order_qty, produced_qty, balance_qty when job_card selected (both planning and actual)
- Recalculates running_balance on good_qty change
- Recalculates total_good_qty and total_waste_qty on good_qty or waste_qty change

---

## 5. HOOKS CONFIGURATION

```python
app_name = "vcl_job_cards"
app_title = "VCL Job Card Tracking"
app_publisher = "Vimit Converters Limited"
app_description = "Comprehensive job card management system..."
app_email = "tanuj@vimitconverters.com"
app_license = "mit"
required_apps = ["erpnext"]
fixtures = []
hide_in_installer = []
```

**Note:** No custom hooks are defined (no doc_events, scheduler_events, override_whitelisted_methods, etc.). All logic is in DocType Python files.

---

## 6. ROLES USED

| Role | Source | Usage |
|------|--------|-------|
| System Manager | Frappe core | Full access to everything |
| Sales Manager | ERPNext | Create/manage specs and job cards |
| Sales User | ERPNext | Read-only access to specs and job cards |
| Manufacturing Manager | ERPNext | Full access to production entries, read/write job cards |
| Manufacturing User | ERPNext | Create/submit production entries, read job cards |
| All | Frappe core | Read-only Dies |

---

## 7. API ENDPOINTS

### Whitelisted Methods:
```
vcl_job_cards.job_card_tracking.doctype.job_card_computer_paper.job_card_computer_paper.get_customer_product_spec_query
```
- Used for link field query filtering
- Parameters: doctype, txt, searchfield, start, page_len, filters (must include `customer`)
- Returns: list of [name, specification_name, customer]

### Standard Frappe APIs Used:
- `frappe.client.get` - Used in JS to fetch full Customer Product Specification doc
- `frappe.db.get_value` - Used in JS to fetch Job Card fields for production lines

---

## 8. KEY BUSINESS LOGIC SUMMARY

### Spec → Job Card Flow:
1. Create Customer Product Specification with all product details
2. Create Job Card Computer Paper, select customer, select spec
3. Spec fields auto-populate into the Job Card (read-only)
4. Job Card is submitted for production

### Production Tracking Flow:
1. Create Production Entry for a day/shift/station
2. Add Planning Lines (what you plan to produce)
3. Add Actual Lines (what was actually produced)
4. On submit, Job Card totals are automatically recalculated
5. On cancel, totals are recalculated (removing this entry's contribution)

### Production Status Auto-Calculation:
```
if total_produced == 0:        → "Not Started"
if total_produced >= ordered:  → "Completed"  
else:                          → "In Production"
```

---

## 9. DATABASE TABLES CREATED

| Frappe DocType | MySQL Table Name |
|----------------|-----------------|
| Dies | `tabDies` |
| Dies Order | `tabDies Order` |
| Customer Product Specification | `tabCustomer Product Specification` |
| Colour of Parts | `tabColour of Parts` |
| Job Card Computer Paper | `tabJob Card Computer Paper` |
| Production Entry | `tabProduction Entry` |
| Production Planning Line | `tabProduction Planning Line` |
| Production Actual Line | `tabProduction Actual Line` |

---

## 10. EXTERNAL DEPENDENCIES

- **ERPNext Customer DocType:** Used as Link target for customer fields
- **Frappe User DocType:** Used as Link target for sales_rep and management_approver
- **No external APIs, no scheduled jobs, no custom web pages, no print formats, no report builders, no dashboards, no workspace files**

---

## 11. FRONTEND CONSIDERATIONS FOR ERPNEXT WEBSITE

### Forms You Need:
1. **Dies Form** - Simple master data entry
2. **Customer Product Specification Form** - Dynamic sections based on product_type, with Dies auto-population for Labels and auto-sync of Colour of Parts for Computer Paper
3. **Job Card Computer Paper Form** - Customer selection → spec filtering → auto-population cascade
4. **Production Entry Form** - Two child tables (planning + actual), real-time total calculations

### Key UI Behaviors to Replicate:
- Conditional field visibility (`depends_on` expressions)
- Link field query filtering (customer_product_spec filtered by customer)
- Auto-population cascades (Dies→Spec, Spec→Job Card)
- Child table auto-sync (number_of_parts ↔ colour_of_parts rows)
- Real-time calculation (running_balance, totals)
- Role-based field editing and form access

### Status Indicators for List Views:
- **Customer Product Specification:** Status (Active/Inactive/Discontinued)
- **Job Card Computer Paper:** Production Status (Not Started/In Production/Completed)
- **Production Entry:** Standard docstatus (Draft/Submitted/Cancelled)
