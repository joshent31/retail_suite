# Retail Industry Suite for ERPNext v15+

Six independent, individually-installable **Frappe v15+ / ERPNext v15+** custom
apps, one per industry vertical. Each app is a self-contained git repository —
build, review, and deploy them one at a time, or install all six side-by-side
on the same ERPNext site.

| # | Industry | App folder (git repo) | Module |
|---|---|---|---|
| 1 | Apparel | `apparel_pro/` | Apparel Management |
| 2 | Footwear | `footwear_pro/` | Footwear Management |
| 3 | Accessories | `accessories_pro/` | Accessories Management |
| 4 | Home Makeover | `home_makeover_pro/` | Home Makeover Management |
| 5 | Lifestyle & Fashion | `lifestyle_fashion_pro/` | Lifestyle Fashion Management |
| 6 | FMCG | `fmcg_pro/` | FMCG Management |

Every app follows the exact same conventions (see each app's own `README.md`
for full detail — DocType list, reports, workspace, notifications, workflow,
print format):

- **DocTypes** — module-based, file-mapped under `<app>/<module>/doctype/…`,
  each with JSON metadata + a Python controller + a client script + a test
  stub (parent doctypes) or just JSON + controller (child tables).
- **Reports** — a mix of Script Reports (Python) and Query Reports (SQL),
  file-mapped under `<app>/<module>/report/…`.
- **Workspace** — one v15-style workspace per app under
  `<app>/<module>/workspace/…`, with shortcuts to the app's DocTypes.
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

You asked for each industry to be individually installable and individually
mappable to its own git repository. Splitting them means:

- You can install only the verticals a given ERPNext instance actually needs.
- Each app can be versioned, released, and pushed to its own repo
  independently (`apparel-pro`, `footwear-pro`, etc.).
- There's no risk of one industry's customizations blocking another's
  upgrade path.

If you later want a single combined app instead, the six `<module>/` folders
can be merged under one app's package directory and listed together in one
`modules.txt` — ask and this can be restructured.

## Quick start (per app)

```bash
# repeat per app, inside your frappe-bench directory
bench get-app apparel_pro /path/to/apparel_pro        # or your git remote URL
bench --site your-site.local install-app apparel_pro
bench --site your-site.local migrate
```

`install-app` requires ERPNext to already be installed on the site, since
every DocType here links back to core ERPNext DocTypes (`Item`, `Customer`,
`Supplier`, `Sales Invoice`, `Warehouse`, `Employee`, `Territory`, `Brand`,
`UOM`, `Company`).

## Publishing each app to its own git repo

```bash
cd apparel_pro
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
- **Client-side UX polish** — each parent DocType ships a minimal `.js` form
  script (`refresh(frm) {}`) as an extension point; dashboards, custom
  buttons, and field-level scripting are intentionally left open rather than
  guessed at.
- **CI/CD** — no GitHub Actions/pre-commit config is included; add your
  bench's standard lint/test pipeline per repo if you use one.

## Full detail

Every claim in this file is expanded, per app, in that app's own
`<app_name>/README.md` — including the complete DocType field list intent,
every report's purpose, every notification's exact trigger, and the full
workflow state/transition map.
