# Apparel Pro

Style-to-shelf apparel operations: style masters, size charts, cut-make-trim production tracking, quality inspection and returns/exchange — on top of ERPNext.

Built for **Frappe Framework v15+** and **ERPNext v15+**. This app extends ERPNext
(Item, Customer, Supplier, Sales Invoice, Warehouse, Employee, etc.) rather than
replacing it — install it alongside a normal ERPNext v15 site.

---

## 1. Module

| | |
|---|---|
| App name (folder / `bench get-app` name) | `apparel_pro` |
| Module | `Apparel Management` |
| Depends on | `frappe`, `erpnext` |
| License | MIT |

## 2. What's included

### DocTypes
| DocType | Purpose |
|---|---|
| Apparel Style Master | Style code, season, collection, fabric, fit, linked Item & size chart. |
| Apparel Size Chart / Size Chart Detail | Reusable size grids (chest/waist/hip/length) per category. |
| Apparel Production Order | Submittable cut-make-trim order with fabric consumption, wastage %, and a Draft→Completed workflow. |
| Apparel Quality Inspection / Defect (child) | Submittable QC record against a Production Order; auto-totals defects. |
| Apparel Return Exchange Request | Customer return/exchange against a Sales Invoice, with refund tracking. |

### Reports
| Report | Type | Purpose |
|---|---|---|
| Apparel Production Status | Script Report | Live status of all production orders with cutting/packing dates. |
| Apparel Style Wise Sales | Query Report | Sales qty/amount per style, joined from Sales Invoice Item. |

### Workspace
- **Apparel** — shortcuts to the DocTypes above, grouped into cards
  (Masters, Production, Reports).

### Notifications (Alerts)
| Notification | Trigger | Recipient |
|---|---|---|
| Apparel Production Completed | Value Change on workflow_state = Completed | Alerts the assigned employee. |
| Apparel QC Failed Alert | On Submit where result = Fail | Alerts the Apparel Manager role. |

### Workflow
**Apparel Production Workflow** on `Apparel Production Order`

States: Draft → Cutting → Sewing → Finishing → Packed → Completed (+ Cancelled)

### Print Format
**Apparel Production Order Slip** for `Apparel Production Order`

---

## 3. Folder structure

```
apparel_pro/                          <- git repo root
├── license.txt
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── .gitignore
├── README.md
└── apparel_pro/                      <- python package (importable)
    ├── __init__.py
    ├── hooks.py
    ├── modules.txt
    ├── patches.txt
    ├── tasks.py
    ├── config/
    │   ├── __init__.py
    │   └── desktop.py
    ├── fixtures/
    │   ├── role.json
    │   ├── notification.json
    │   ├── workflow.json
    │   └── print_format.json
    └── apparel_management/
        ├── __init__.py
        ├── doctype/
        │   └── <doctype_name>/
        │       ├── __init__.py
        │       ├── <doctype_name>.json
        │       ├── <doctype_name>.py
        │       ├── <doctype_name>.js       (parent doctypes only)
        │       └── test_<doctype_name>.py  (parent doctypes only)
        ├── report/
        │   └── <report_name>/
        │       ├── __init__.py
        │       ├── <report_name>.json
        │       └── <report_name>.py        (script reports only)
        └── workspace/
            └── apparel/
                └── apparel.json
```

---

## 4. Installation (ERPNext v15+ / Frappe v15+)

```bash
# 1. From your bench directory, get the app (point this at your git remote
#    once you've pushed this folder to GitHub/GitLab/Gitea/etc.)
bench get-app apparel_pro /path/to/apparel_pro   # or a git URL

# 2. Install it on a site that already has erpnext installed
bench --site your-site.local install-app apparel_pro

# 3. Run migrations to sync DocTypes, Reports, Workspace, and fixtures
bench --site your-site.local migrate

# 4. (Fixtures such as Notification/Workflow/Role are imported automatically
#    during migrate because they are declared in hooks.py -> fixtures = [...].
#    To re-export them after making changes in the UI:)
bench --site your-site.local export-fixtures --app apparel_pro
```

### Publishing to git

```bash
cd apparel_pro
git init
git add .
git commit -m "Initial commit: Apparel Pro"
git branch -M main
git remote add origin <your-empty-repo-url>
git push -u origin main
```

Each of the 6 industry apps in this delivery is an **independent git repo** —
this folder (`apparel_pro/`) is the repo root, so you can `git init` inside it
directly without pulling in the other five apps.

---

## 5. Roles created

- `Apparel Manager`
- `Apparel User`

Assign these to users via **User > Roles** after installation. `System Manager`
always has full access to everything in this app regardless of these roles.

---

## 6. Notes & extension points

- Naming series (e.g. `APO-.YYYY.-`) can be changed per-company in
  **Setup > Naming Series** after install.
- All transactional DocTypes use ERPNext's standard `Company`/multi-currency
  conventions where relevant — add a `company` field to any DocType that
  needs company-wise reporting if you run a multi-company site.
- Script reports live under `apparel_management/report/<name>/<name>.py` — extend
  the `execute()` function to add filters, charts, or summary rows.
- The scheduled task stub in `tasks.py` (`scheduler_events > daily`) is a good
  place to add automated jobs, e.g. re-computing expiry status or ageing.
