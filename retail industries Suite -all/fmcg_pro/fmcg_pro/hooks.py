from . import __version__ as app_version

app_name = "fmcg_pro"
app_title = "FMCG Pro"
app_publisher = "Retail Industry Suite"
app_description = "Batch/expiry tracking, distributor master, trade schemes, route/beat planning and van sales for FMCG distribution on ERPNext."
app_email = "admin@example.com"
app_license = "MIT"
required_apps = ["frappe/erpnext"]

# Includes in <head>
# ------------------
# app_include_css = "/assets/fmcg_pro/css/fmcg_pro.css"
# app_include_js = "/assets/fmcg_pro/js/fmcg_pro.js"

# Fixtures
# --------
# Exported as data via `bench --site [site] export-fixtures`
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ['FMCG Manager', 'FMCG User']]]},
	{"dt": "Notification", "filters": [["module", "=", "Fmcg Management"]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ['FMCG Scheme Promotion']]]},
	{"dt": "Print Format", "filters": [["module", "=", "Fmcg Management"]]},
	{"dt": "Number Card", "filters": [["name", "in", ['FMCG Near Expiry Batches']]]},
	{"dt": "Dashboard Chart", "filters": [["name", "in", ['FMCG Batches by Status']]]},
]

# Installation
# ------------
# before_install = "fmcg_pro.install.before_install"
# after_install = "fmcg_pro.install.after_install"

# Document Events
# ----------------
doc_events = {
	"FMCG Scheme Promotion": {
		"on_update": "fmcg_pro.fmcg_pro.utils.sync_workflow_status",
	}
}

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"fmcg_pro.fmcg_pro.tasks.daily"
	]
}
