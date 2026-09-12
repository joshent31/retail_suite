from . import __version__ as app_version

app_name = "fmcg_pro"
app_title = "FMCG Pro"
app_publisher = "Your Organization"
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
	{"dt": "Notification", "filters": [["module", "=", "FMCG Management"]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ['FMCG Scheme Promotion']]]},
	{"dt": "Print Format", "filters": [["module", "=", "FMCG Management"]]},
]

# Installation
# ------------
# before_install = "fmcg_pro.install.before_install"
# after_install = "fmcg_pro.install.after_install"

# Document Events
# ----------------
# Hook on document methods and events
#
# doc_events = {
# 	"*": {
# 		"on_update": "fmcg_pro.utils.on_doc_update"
# 	}
# }

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"fmcg_pro.tasks.daily"
	]
}
