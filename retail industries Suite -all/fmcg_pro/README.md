# FMCG Pro

Batch & expiry tracking, distributor master, trade schemes, route/beat planning, van sales and retailer visit logs — on top of ERPNext.

Built for **Frappe Framework v15+** and **ERPNext v15+**. This app extends ERPNext
(Item, Customer, Supplier, Sales Invoice, Warehouse, Employee, etc.) rather than
replacing it — install it alongside a normal ERPNext v15 site.

---

## 1. Module

| | |
|---|---|
| App name (folder / `bench get-app` name) | `fmcg_pro` |
| Module | `FMCG Management` |
| Depends on | `frappe`, `erpnext` |
| License | MIT |

## 2. What's included

### DocTypes
| DocType | Purpose |
|---|---|
| FMCG Batch Expiry Tracker | Auto-computes days-to-expiry and Fresh/Near Expiry/Expired status. |
| FMCG Distributor Master | Territory, credit limit and outstanding amount per distributor. |
| FMCG Scheme Promotion / Applicable Distributor (child) | Submittable trade scheme with a Draft→Expired workflow. |
| FMCG Route Beat Plan / Retailer Detail (child) | Salesperson beat plan with an ordered retailer sequence. |
| FMCG Van Sales Entry / Item (child) | Submittable van-sales invoice; auto-totals line amounts. |
| FMCG Retailer Visit Log | Visit-level order capture with GPS location field. |

### Reports
| Report | Type | Purpose |
|---|---|---|
| Near Expiry Stock Alert | Script Report | All Near Expiry / Expired batches sorted by expiry date. |
| Van Sales Summary by Route | Query Report | Submitted van sales grouped by route and salesperson. |

### Workspace
- **FMCG** — shortcuts to the DocTypes above, grouped into cards
  (Inventory & Schemes, Field Sales, Reports).

### Notifications (Alerts)
| Notification | Trigger | Recipient |
|---|---|---|
| FMCG Near Expiry Alert | Value Change on status = Near Expiry | Alerts the FMCG Manager role. |
| Distributor Credit Limit Exceeded | On Save where outstanding > credit limit | Alerts the FMCG Manager role. |

### Workflow
**FMCG Scheme Promotion Workflow** on `FMCG Scheme Promotion`

States: Draft → Approved → Active → Expired

### Print Format
**Van Sales Invoice** for `FMCG Van Sales Entry`

---

## 3. Folder structure

```
fmcg_pro/                          <- git repo root
├── license.txt
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── .gitignore
├── README.md
└── fmcg_pro/                      <- python package (importable)
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
    └── fmcg_management/
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
            └── fmcg/
                └── fmcg.json
```

---

## 4. Installation (ERPNext v15+ / Frappe v15+)

```bash
# 1. From your bench directory, get the app (point this at your git remote
#    once you've pushed this folder to GitHub/GitLab/Gitea/etc.)
bench get-app fmcg_pro /path/to/fmcg_pro   # or a git URL

# 2. Install it on a site that already has erpnext installed
bench --site your-site.local install-app fmcg_pro

# 3. Run migrations to sync DocTypes, Reports, Workspace, and fixtures
bench --site your-site.local migrate

# 4. (Fixtures such as Notification/Workflow/Role are imported automatically
#    during migrate because they are declared in hooks.py -> fixtures = [...].
#    To re-export them after making changes in the UI:)
bench --site your-site.local export-fixtures --app fmcg_pro
```

### Publishing to git

```bash
cd fmcg_pro
git init
git add .
git commit -m "Initial commit: FMCG Pro"
git branch -M main
git remote add origin <your-empty-repo-url>
git push -u origin main
```

Each of the 6 industry apps in this delivery is an **independent git repo** —
this folder (`fmcg_pro/`) is the repo root, so you can `git init` inside it
directly without pulling in the other five apps.

---

## 5. Roles created

- `FMCG Manager`
- `FMCG User`

Assign these to users via **User > Roles** after installation. `System Manager`
always has full access to everything in this app regardless of these roles.

---

## 6. Notes & extension points

- Naming series (e.g. `APO-.YYYY.-`) can be changed per-company in
  **Setup > Naming Series** after install.
- All transactional DocTypes use ERPNext's standard `Company`/multi-currency
  conventions where relevant — add a `company` field to any DocType that
  needs company-wise reporting if you run a multi-company site.
- Script reports live under `fmcg_management/report/<name>/<name>.py` — extend
  the `execute()` function to add filters, charts, or summary rows.
- The scheduled task stub in `tasks.py` (`scheduler_events > daily`) is a good
  place to add automated jobs, e.g. re-computing expiry status or ageing.
