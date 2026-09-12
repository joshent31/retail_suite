# Lifestyle & Fashion Pro

Collection planning, influencer collaborations, trend boards, lookbooks, a loyalty ledger and style-consultation bookings — on top of ERPNext.

Built for **Frappe Framework v15+** and **ERPNext v15+**. This app extends ERPNext
(Item, Customer, Supplier, Sales Invoice, Warehouse, Employee, etc.) rather than
replacing it — install it alongside a normal ERPNext v15 site.

---

## 1. Module

| | |
|---|---|
| App name (folder / `bench get-app` name) | `lifestyle_fashion_pro` |
| Module | `Lifestyle Fashion Management` |
| Depends on | `frappe`, `erpnext` |
| License | MIT |

## 2. What's included

### DocTypes
| DocType | Purpose |
|---|---|
| Fashion Collection Master / Item (child) | Season, launch date, theme and the Items in a collection. |
| Influencer Brand Collaboration | Submittable collab record with a Proposed→Completed workflow. |
| Trend Forecast Board / Reference Image (child) | Moodboard-style trend notes with reference images. |
| Lookbook / Look Detail (child) | Curated looks per collection with styling notes. |
| Loyalty Points Ledger | Submittable earn/redeem/expire ledger with auto-computed running balance. |
| Style Consultation Booking | Submittable in-store/virtual booking with status tracking. |

### Reports
| Report | Type | Purpose |
|---|---|---|
| Loyalty Points Balance Summary | Script Report | Current point balance per customer. |
| Influencer Collaboration ROI | Query Report | Agreed spend per influencer/collection. |

### Workspace
- **Lifestyle & Fashion** — shortcuts to the DocTypes above, grouped into cards
  (Collections, Customer Engagement, Reports).

### Notifications (Alerts)
| Notification | Trigger | Recipient |
|---|---|---|
| Style Consultation Reminder | 1 day before booking_date, if Scheduled | Alerts the assigned stylist. |
| Loyalty Points Expiry Alert | On Submit where transaction_type = Expired | Alerts the Fashion Manager role. |

### Workflow
**Influencer Collaboration Workflow** on `Influencer Brand Collaboration`

States: Proposed → Active → Completed (+ Cancelled)

### Print Format
**Style Consultation Confirmation** for `Style Consultation Booking`

### Automation & ERPNext integration
- **Loyalty Points Ledger** computes running balances under a row lock (race-safe), blocks negative balances on submit, and auto-creates a reversal entry when a submitted entry is cancelled.
- **Daily task** sweeps earned points past their expiry date into Expired entries.
- **Number Card + Dashboard Chart** (active collaborations / by status) wired into the Lifestyle Fashion workspace.

---

## 3. Folder structure

```
lifestyle_fashion_pro/                          <- git repo root
├── license.txt
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── .gitignore
├── README.md
└── lifestyle_fashion_pro/                      <- python package (importable)
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
    └── lifestyle_fashion_management/
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
            └── lifestyle_fashion/
                └── lifestyle_fashion.json
```

---

## 4. Installation (ERPNext v15+ / Frappe v15+)

```bash
# 1. From your bench directory, get the app (point this at your git remote
#    once you've pushed this folder to GitHub/GitLab/Gitea/etc.)
bench get-app lifestyle_fashion_pro /path/to/lifestyle_fashion_pro   # or a git URL

# 2. Install it on a site that already has erpnext installed
bench --site your-site.local install-app lifestyle_fashion_pro

# 3. Run migrations to sync DocTypes, Reports, Workspace, and fixtures
bench --site your-site.local migrate

# 4. (Fixtures such as Notification/Workflow/Role are imported automatically
#    during migrate because they are declared in hooks.py -> fixtures = [...].
#    To re-export them after making changes in the UI:)
bench --site your-site.local export-fixtures --app lifestyle_fashion_pro
```

### Publishing to git

```bash
cd lifestyle_fashion_pro
git init
git add .
git commit -m "Initial commit: Lifestyle & Fashion Pro"
git branch -M main
git remote add origin <your-empty-repo-url>
git push -u origin main
```

Each of the 6 industry apps in this delivery is an **independent git repo** —
this folder (`lifestyle_fashion_pro/`) is the repo root, so you can `git init` inside it
directly without pulling in the other five apps.

---

## 5. Roles created

- `Fashion Manager`
- `Fashion Stylist`

Assign these to users via **User > Roles** after installation. `System Manager`
always has full access to everything in this app regardless of these roles.

---

## 6. Notes & extension points

- Naming series (e.g. `APO-.YYYY.-`) can be changed per-company in
  **Setup > Naming Series** after install.
- All transactional DocTypes use ERPNext's standard `Company`/multi-currency
  conventions where relevant — add a `company` field to any DocType that
  needs company-wise reporting if you run a multi-company site.
- Script reports live under `lifestyle_fashion_management/report/<name>/<name>.py` — extend
  the `execute()` function to add filters, charts, or summary rows.
- Daily scheduled jobs in `tasks.py` (registered via `scheduler_events > daily`)
  handle expiry recomputation, ageing alerts and similar automation for this app.
