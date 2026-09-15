# Retail Industry Suite for ERPNext v15+

A single, installable **Frappe v15+ / ERPNext v15+** app containing **six
retail industry verticals**. Install once — then use any or all sectors;
each one lives in its own module with its own workspace, roles, reports,
and dashboards.

| # | Industry | Module |
|---|---|---|
| 1 | Apparel | Apparel Management |
| 2 | Footwear | Footwear Management |
| 3 | Accessories | Accessories Management |
| 4 | Home Makeover | Home Makeover Management |
| 5 | Lifestyle & Fashion | Lifestyle Fashion Management |
| 6 | FMCG | FMCG Management |

Each sector is documented in detail under [`docs/`](docs/) — DocType list,
reports, notifications, workflow, print format, and its automation features.

## What's inside each sector

Every module follows the same conventions:

- **DocTypes** — under `retail_suite/<module>/doctype/…`, each with JSON
  metadata, a Python controller, a client script, and tests.
- **Reports** — Script Reports (Python) and Query Reports (SQL) under
  `retail_suite/<module>/report/…`, each with a filter UI (`.js`) and
  industry-role permissions.
- **Workspace** — one workspace per module with shortcuts, number cards,
  and dashboard charts.
- **Fixtures** — Roles, Notifications, Workflows, Print Formats, Number
  Cards, and Dashboard Charts are versioned under
  `retail_suite/fixtures/` and wired through `hooks.py`.
- **Daily jobs** — one scheduler entry dispatches to each sector's daily
  task (expiry alerts, loyalty expiry sweeps, overdue production, ageing
  consignments, milestone reminders, stale warranty claims).
- **ERPNext integrations (built in)** — Create Stock Entry (Apparel
  production), Create Sales Invoice (FMCG van sales, Home Makeover
  milestones), Create Delivery Note (Footwear warranty replacements),
  Create Material Request (Home Makeover estimations), Settle with
  Supplier (Accessories consignment), bundle stock checks (Accessories).

## Install

Requirements: a Frappe v15+ bench with **ERPNext v15+ installed** on the
site (`required_apps = ["frappe/erpnext"]`).

```bash
cd frappe-bench

bench get-app https://github.com/joshent31/retail_suite.git
bench --site your-site.local install-app retail_suite
bench --site your-site.local migrate
bench restart
```

After installing:

1. **Roles** — fixtures create roles like `Apparel Manager`, `FMCG
   Manager`; assign them to users under Setup > User (System Manager sees
   everything).
2. **Scheduler** — enable it so the daily jobs run:
   `bench --site your-site.local enable-scheduler`.
3. **Workspaces** — number cards + dashboard charts appear after
   `bench migrate`.
4. **Settings** — some sectors ship a Settings singleton (e.g. FMCG Pro
   Settings for the near-expiry threshold) — set it once from the
   AwesomeBar.

## Development

```bash
# lint + checks (same as CI)
pip install ruff
ruff check .
python -m compileall -q retail_suite

# pre-commit
pip install pre-commit && pre-commit install
```

## License

MIT — see [license.txt](license.txt).
