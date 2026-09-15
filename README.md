# Retail Industry Suite for ERPNext v15+

Six independent, individually-installable **Frappe v15+ / ERPNext v15+** custom
apps, one per industry vertical. Each app is a self-contained app folder —
build, review, and deploy them one at a time, or install all six side-by-side
on the same ERPNext site.

**Apps live under [`retail industries Suite -all/`](retail%20industries%20Suite%20-all/).**

| # | Industry | App folder | Module |
|---|---|---|---|
| 1 | Apparel | [`apparel_pro/`](retail%20industries%20Suite%20-all/apparel_pro/) | Apparel Management |
| 2 | Footwear | [`footwear_pro/`](retail%20industries%20Suite%20-all/footwear_pro/) | Footwear Management |
| 3 | Accessories | [`accessories_pro/`](retail%20industries%20Suite%20-all/accessories_pro/) | Accessories Management |
| 4 | Home Makeover | [`home_makeover_pro/`](retail%20industries%20Suite%20-all/home_makeover_pro/) | Home Makeover Management |
| 5 | Lifestyle & Fashion | [`lifestyle_fashion_pro/`](retail%20industries%20Suite%20-all/lifestyle_fashion_pro/) | Lifestyle Fashion Management |
| 6 | FMCG | [`fmcg_pro/`](retail%20industries%20Suite%20-all/fmcg_pro/) | FMCG Management |

Every app follows the exact same conventions (see each app's own `README.md`
for full detail — DocType list, reports, workspace, notifications, workflow,
print format):

- **DocTypes** — module-based, file-mapped under `<app>/<module>/doctype/…`,
  each with JSON metadata + a Python controller + a client script + tests
  (parent doctypes) or just JSON + controller (child tables).
- **Reports** — a mix of Script Reports (Python) and Query Reports (SQL),
  file-mapped under `<app>/<module>/report/…`, each with a filter UI (`.js`)
  and industry-role permissions.
- **Workspace** — one v15-style workspace per app under
  `<app>/<module>/workspace/…`, with shortcuts, number cards, and dashboard
  charts.
- **Notifications** (Email Alert-style `Notification` doctype records) and
  **Workflows** — not file-mapped by Frappe by default, so they're shipped as
  **fixtures** under `<app>/<app>/fixtures/*.json` and wired into
  `hooks.py → fixtures = [...]`, which is the standard, git-friendly way to
  version them.
- **Print Format** — one Jinja print format per app, also shipped as a
  fixture.
- **Roles** — two custom roles per app (a "Manager" and a "User"/"Stylist"/
  etc.), also shipped as fixtures.

## Why six separate apps, not one

Each industry is individually installable and individually mappable to its own
git repository. Splitting them means:

- You can install only the verticals a given ERPNext instance actually needs.
- Each app can be versioned, released, and pushed to its own repo
  independently (`apparel-pro`, `footwear-pro`, etc.).
- There's no risk of one industry's customizations blocking another's
  upgrade path.

If you later want a single combined app instead, the six `<module>/` folders
can be merged under one app's package directory and listed together in one
`modules.txt` — ask and this can be restructured.

## Quick start

Requirements: a Frappe v15+ bench with **ERPNext v15+ installed** (every app
declares `required_apps = ["frappe/erpnext"]`, since all DocTypes link back to
core ERPNext DocTypes like `Item`, `Customer`, `Sales Invoice`, `Warehouse`).

Install only the sector(s) you need:

```bash
cd frappe-bench

# Option A — install straight from GitHub (installs the repo's default app
# layout; use the local path in Option B for a specific sub-app)
bench get-app https://github.com/joshent31/retail_suite.git

# Option B — clone once, then pick the app folders you want
git clone https://github.com/joshent31/retail_suite.git
bench get-app apparel_pro ./retail_suite/"retail industries Suite -all"/apparel_pro

# then, per app:
bench --site your-site.local install-app apparel_pro
bench --site your-site.local migrate
bench restart
```

You can install all six apps on the same site — they use different module
names and different custom-field fieldnames, so they don't collide.

After installing:

1. **Roles** — the fixtures create roles like `Apparel Manager`; assign them
   to users under Setup > User (System Manager sees everything).
2. **Scheduler** — daily jobs (expiry alerts, loyalty expiry sweeps, overdue
   production) need the scheduler enabled:
   `bench --site your-site.local enable-scheduler`.
3. **Workspaces** — number cards + dashboard charts appear after
   `bench migrate`.
4. **Settings** — some apps ship a Settings singleton (e.g. FMCG Pro Settings
   for the expiry threshold) — set it once from the AwesomeBar.

## Publishing each app to its own git repo

```bash
cd "retail industries Suite -all/apparel_pro"
git init && git add . && git commit -m "Initial commit: Apparel Pro"
git branch -M main
git remote add origin <empty-repo-url-for-apparel-pro>
git push -u origin main
```

Repeat for each of the other five folders with their own remotes.

## What's deliberately left for you to configure per deployment

- **Company / multi-currency specifics** — naming series prefixes, default
  warehouses, and company-wise filters are left at ERPNext defaults; adjust
  per site.
- **Role → User assignment** — the fixtures create the Roles; assigning them
  to actual users is a per-deployment step (Setup > User).
- **Buttons & integrations (built in)** — every app ships working actions
  (Create Stock Entry / Sales Invoice / Delivery Note / Material Request,
  Settle with Supplier, bundle stock checks), Settings singletons, daily
  scheduled jobs, and number cards + dashboard charts on each workspace.
  Each app's README lists exactly what it automates.
- **CI/CD (built in)** — this repository includes a GitHub Actions workflow
  (ruff lint + Python compile check + JSON validation) and a pre-commit
  config; run `pip install pre-commit && pre-commit install` to enable it
  locally.

## Full detail

Every claim in this file is expanded, per app, in that app's own
`<app_name>/README.md` — including the complete DocType field list intent,
every report's purpose, every notification's exact trigger, and the full
workflow state/transition map.
