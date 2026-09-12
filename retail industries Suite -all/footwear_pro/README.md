# Footwear Pro

Footwear-specific style masters, regional size runs, material BOMs, QC, warranty claims and vendor scorecards — on top of ERPNext.

Built for **Frappe Framework v15+** and **ERPNext v15+**. This app extends ERPNext
(Item, Customer, Supplier, Sales Invoice, Warehouse, Employee, etc.) rather than
replacing it — install it alongside a normal ERPNext v15 site.

---

## 1. Module

| | |
|---|---|
| App name (folder / `bench get-app` name) | `footwear_pro` |
| Module | `Footwear Management` |
| Depends on | `frappe`, `erpnext` |
| License | MIT |

## 2. What's included

### DocTypes
| DocType | Purpose |
|---|---|
| Footwear Style Master | Category, upper/sole material, gender, season, linked size run. |
| Footwear Size Run / Detail (child) | US/UK/EU/CM size grids with foot length in cm. |
| Footwear Material BOM / Detail (child) | Bill of materials per style with auto-computed cost. |
| Footwear QC Inspection | Submittable QC record with Pass/Fail/Rework result. |
| Footwear Warranty Claim | Submittable claim with Open→Resolved workflow. |
| Footwear Vendor Rating | Quality/delivery/price scorecard with auto-computed overall rating. |

### Reports
| Report | Type | Purpose |
|---|---|---|
| Footwear Warranty Claims Summary | Script Report | All claims with current workflow status. |
| Footwear Stock by Size Run | Query Report | Active styles grouped by their size run. |

### Workspace
- **Footwear** — shortcuts to the DocTypes above, grouped into cards
  (Masters, Quality & Warranty, Reports).

### Notifications (Alerts)
| Notification | Trigger | Recipient |
|---|---|---|
| Footwear Warranty Status Update | Value Change on workflow_state | Alerts the Footwear Manager role. |
| Footwear Low Rated Vendor Alert | On Save where overall_rating < 5 | Alerts the Footwear Manager role. |

### Workflow
**Footwear Warranty Claim Workflow** on `Footwear Warranty Claim`

States: Open → Under Review → Approved/Rejected → Resolved

### Print Format
**Warranty Claim Certificate** for `Footwear Warranty Claim`

---

## 3. Folder structure

```
footwear_pro/                          <- git repo root
├── license.txt
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── .gitignore
├── README.md
└── footwear_pro/                      <- python package (importable)
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
    └── footwear_management/
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
            └── footwear/
                └── footwear.json
```

---

## 4. Installation (ERPNext v15+ / Frappe v15+)

```bash
# 1. From your bench directory, get the app (point this at your git remote
#    once you've pushed this folder to GitHub/GitLab/Gitea/etc.)
bench get-app footwear_pro /path/to/footwear_pro   # or a git URL

# 2. Install it on a site that already has erpnext installed
bench --site your-site.local install-app footwear_pro

# 3. Run migrations to sync DocTypes, Reports, Workspace, and fixtures
bench --site your-site.local migrate

# 4. (Fixtures such as Notification/Workflow/Role are imported automatically
#    during migrate because they are declared in hooks.py -> fixtures = [...].
#    To re-export them after making changes in the UI:)
bench --site your-site.local export-fixtures --app footwear_pro
```

### Publishing to git

```bash
cd footwear_pro
git init
git add .
git commit -m "Initial commit: Footwear Pro"
git branch -M main
git remote add origin <your-empty-repo-url>
git push -u origin main
```

Each of the 6 industry apps in this delivery is an **independent git repo** —
this folder (`footwear_pro/`) is the repo root, so you can `git init` inside it
directly without pulling in the other five apps.

---

## 5. Roles created

- `Footwear Manager`
- `Footwear User`

Assign these to users via **User > Roles** after installation. `System Manager`
always has full access to everything in this app regardless of these roles.

---

## 6. Notes & extension points

- Naming series (e.g. `APO-.YYYY.-`) can be changed per-company in
  **Setup > Naming Series** after install.
- All transactional DocTypes use ERPNext's standard `Company`/multi-currency
  conventions where relevant — add a `company` field to any DocType that
  needs company-wise reporting if you run a multi-company site.
- Script reports live under `footwear_management/report/<name>/<name>.py` — extend
  the `execute()` function to add filters, charts, or summary rows.
- The scheduled task stub in `tasks.py` (`scheduler_events > daily`) is a good
  place to add automated jobs, e.g. re-computing expiry status or ageing.
