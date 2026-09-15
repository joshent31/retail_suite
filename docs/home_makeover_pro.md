# Home Makeover Pro

Consultation-to-handover project tracking for interiors/home-makeover businesses: measurements, material estimates, contractors, site visits and milestone billing — on top of ERPNext.

Built for **Frappe Framework v15+** and **ERPNext v15+**. This app extends ERPNext
(Item, Customer, Supplier, Sales Invoice, Warehouse, Employee, etc.) rather than
replacing it — install it alongside a normal ERPNext v15 site.

---

## 1. Module

| | |
|---|---|
| App name (folder / `bench get-app` name) | `home_makeover_pro` |
| Module | `Home Makeover Management` |
| Depends on | `frappe`, `erpnext` |
| License | MIT |

## 2. What's included

### DocTypes
| DocType | Purpose |
|---|---|
| Home Makeover Project | Submittable project header with a Lead→Completed workflow. |
| Room Measurement Sheet / Detail (child) | Per-room wall/floor dimensions with auto-computed area. |
| Material Estimation / Item (child) | Submittable cost estimate; auto-totals from qty × rate. |
| Vendor Contractor Assignment | Contractor/work-type assignment with agreed amount. |
| Site Visit Log | Visit notes, photo attachment and next-visit date. |
| Project Milestone Payment / Detail (child) | Submittable milestone-wise billing schedule. |

### Reports
| Report | Type | Purpose |
|---|---|---|
| Project Status Dashboard | Script Report | All projects with type, status, budget and expected end date. |
| Milestone Payment Collection | Query Report | Milestone due dates and amounts across all projects. |

### Workspace
- **Home Makeover** — shortcuts to the DocTypes above, grouped into cards
  (Projects, Execution, Reports).

### Notifications (Alerts)
| Notification | Trigger | Recipient |
|---|---|---|
| Site Visit Reminder | 1 day before next_visit_date | Alerts the assigned visitor. |
| Milestone Payment Due | On new Project Milestone Payment | Alerts the Home Makeover Manager role. |

### Workflow
**Home Makeover Project Workflow** on `Home Makeover Project`

States: Lead → Consultation → Design → Approved → Execution → Completed (+ Cancelled)

### Print Format
**Project Estimate Quotation** for `Material Estimation`

### Automation & ERPNext integration
- **Create Sales Invoice** from the Pending milestones of a submitted Milestone Payment (project budget guard; milestones flip to Invoiced).
- **Create Material Request** from submitted Material Estimations.
- **Home Makeover Settings** singleton: default billing item for milestone invoices.
- **Daily task** alerts on milestones due within 3 days or already overdue.
- **Number Card + Dashboard Chart** (active projects / by status) wired into the Home Makeover workspace.
- Validations: milestone percentages cannot exceed 100%, invoiced amounts cannot exceed the project budget.

---

## 3. Folder structure

```
home_makeover_pro/                          <- git repo root
├── license.txt
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── .gitignore
├── README.md
└── home_makeover_pro/                      <- python package (importable)
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
    └── home_makeover_management/
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
            └── home_makeover/
                └── home_makeover.json
```

---

## 4. Installation (ERPNext v15+ / Frappe v15+)

```bash
# 1. From your bench directory, get the app (point this at your git remote
#    once you've pushed this folder to GitHub/GitLab/Gitea/etc.)
bench get-app home_makeover_pro /path/to/home_makeover_pro   # or a git URL

# 2. Install it on a site that already has erpnext installed
bench --site your-site.local install-app home_makeover_pro

# 3. Run migrations to sync DocTypes, Reports, Workspace, and fixtures
bench --site your-site.local migrate

# 4. (Fixtures such as Notification/Workflow/Role are imported automatically
#    during migrate because they are declared in hooks.py -> fixtures = [...].
#    To re-export them after making changes in the UI:)
bench --site your-site.local export-fixtures --app home_makeover_pro
```

### Publishing to git

```bash
cd home_makeover_pro
git init
git add .
git commit -m "Initial commit: Home Makeover Pro"
git branch -M main
git remote add origin <your-empty-repo-url>
git push -u origin main
```

Each of the 6 industry apps in this delivery is an **independent git repo** —
this folder (`home_makeover_pro/`) is the repo root, so you can `git init` inside it
directly without pulling in the other five apps.

---

## 5. Roles created

- `Home Makeover Manager`
- `Home Makeover Designer`

Assign these to users via **User > Roles** after installation. `System Manager`
always has full access to everything in this app regardless of these roles.

---

## 6. Notes & extension points

- Naming series (e.g. `APO-.YYYY.-`) can be changed per-company in
  **Setup > Naming Series** after install.
- All transactional DocTypes use ERPNext's standard `Company`/multi-currency
  conventions where relevant — add a `company` field to any DocType that
  needs company-wise reporting if you run a multi-company site.
- Script reports live under `home_makeover_management/report/<name>/<name>.py` — extend
  the `execute()` function to add filters, charts, or summary rows.
- Daily scheduled jobs in `tasks.py` (registered via `scheduler_events > daily`)
  handle expiry recomputation, ageing alerts and similar automation for this app.
