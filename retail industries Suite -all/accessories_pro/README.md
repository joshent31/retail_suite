# Accessories Pro

Accessory category masters, combo/kit bundles, consignment stock tracking and returns — on top of ERPNext.

Built for **Frappe Framework v15+** and **ERPNext v15+**. This app extends ERPNext
(Item, Customer, Supplier, Sales Invoice, Warehouse, Employee, etc.) rather than
replacing it — install it alongside a normal ERPNext v15 site.

---

## 1. Module

| | |
|---|---|
| App name (folder / `bench get-app` name) | `accessories_pro` |
| Module | `Accessories Management` |
| Depends on | `frappe`, `erpnext` |
| License | MIT |

## 2. What's included

### DocTypes
| DocType | Purpose |
|---|---|
| Accessory Category Master | Hierarchical category tree mapped to Item Group. |
| Accessory Item Bundle / Component (child) | Combo/kit pricing with a validity window. |
| Accessory Material Composition / Detail (child) | Material percentage breakdown per item. |
| Accessory Consignment Stock | Submittable consignment-in record with a Received→Settled workflow. |
| Accessory Return Request | Customer return with condition (New/Used/Damaged) tracking. |

### Reports
| Report | Type | Purpose |
|---|---|---|
| Accessory Consignment Ageing | Script Report | Open consignments sorted by age in days. |
| Bundle Sales Performance | Query Report | Units sold per bundle, joined from Sales Invoice Item. |

### Workspace
- **Accessories** — shortcuts to the DocTypes above, grouped into cards
  (Masters, Consignment, Reports).

### Notifications (Alerts)
| Notification | Trigger | Recipient |
|---|---|---|
| Consignment Settlement Due | 30 days after consignment_date, unsettled | Alerts the Accessories Manager role. |
| Bundle Expiry Reminder | 7 days before valid_upto | Alerts the Accessories Manager role. |

### Workflow
**Accessory Consignment Workflow** on `Accessory Consignment Stock`

States: Received → Partially Sold → Settled / Returned

### Print Format
**Consignment Note** for `Accessory Consignment Stock`

---

## 3. Folder structure

```
accessories_pro/                          <- git repo root
├── license.txt
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── .gitignore
├── README.md
└── accessories_pro/                      <- python package (importable)
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
    └── accessories_management/
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
            └── accessories/
                └── accessories.json
```

---

## 4. Installation (ERPNext v15+ / Frappe v15+)

```bash
# 1. From your bench directory, get the app (point this at your git remote
#    once you've pushed this folder to GitHub/GitLab/Gitea/etc.)
bench get-app accessories_pro /path/to/accessories_pro   # or a git URL

# 2. Install it on a site that already has erpnext installed
bench --site your-site.local install-app accessories_pro

# 3. Run migrations to sync DocTypes, Reports, Workspace, and fixtures
bench --site your-site.local migrate

# 4. (Fixtures such as Notification/Workflow/Role are imported automatically
#    during migrate because they are declared in hooks.py -> fixtures = [...].
#    To re-export them after making changes in the UI:)
bench --site your-site.local export-fixtures --app accessories_pro
```

### Publishing to git

```bash
cd accessories_pro
git init
git add .
git commit -m "Initial commit: Accessories Pro"
git branch -M main
git remote add origin <your-empty-repo-url>
git push -u origin main
```

Each of the 6 industry apps in this delivery is an **independent git repo** —
this folder (`accessories_pro/`) is the repo root, so you can `git init` inside it
directly without pulling in the other five apps.

---

## 5. Roles created

- `Accessories Manager`
- `Accessories User`

Assign these to users via **User > Roles** after installation. `System Manager`
always has full access to everything in this app regardless of these roles.

---

## 6. Notes & extension points

- Naming series (e.g. `APO-.YYYY.-`) can be changed per-company in
  **Setup > Naming Series** after install.
- All transactional DocTypes use ERPNext's standard `Company`/multi-currency
  conventions where relevant — add a `company` field to any DocType that
  needs company-wise reporting if you run a multi-company site.
- Script reports live under `accessories_management/report/<name>/<name>.py` — extend
  the `execute()` function to add filters, charts, or summary rows.
- The scheduled task stub in `tasks.py` (`scheduler_events > daily`) is a good
  place to add automated jobs, e.g. re-computing expiry status or ageing.
